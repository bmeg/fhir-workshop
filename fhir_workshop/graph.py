import logging
from collections import namedtuple, defaultdict

import networkx as nx
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.resource import Resource

from fhir_workshop.resources import read_resources
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

EdgeInfo = namedtuple("EdgeInfo", "source_id destination_id name")


def _static_reference_resolved(self,  klass=None) -> Resource:
    """Replace smart on FHIR's server based resolver with our local static resolver."""
    logger.debug(f"_static_reference_resolver {self.processedReferenceIdentifier()}")
    owning_resource = self.owningResource()
    if owning_resource is None:
        raise Exception("Cannot resolve reference without having an owner (which must be a `DomainResource`)")
    ref_id = self.processedReferenceIdentifier()
    # already resolved and cached?
    resolved = owning_resource.resolvedReference(ref_id)
    if resolved is not None:
        return resolved
    logger.warning(f"Referenced resource {ref_id} not found")
    return None


FHIRReference.resolved = _static_reference_resolved


def load_graph(name, file_paths, expected_resource_count, strict=True) -> nx.Graph:
    """Inspect resource's references, load into a graph, create bidirectional links,
     resolve resource's references, including extensions."""
    graph = nx.MultiDiGraph(name=name)
    resource_count = 0
    edges = []
    for file_path in file_paths:
        resource_count = _process_fhir_file(graph, edges, file_path, resource_count, strict)
    for edge in edges:
        # the source must exist
        assert graph.nodes.get(edge.source_id)
        # warn if no destination
        if not graph.nodes.get(edge.destination_id):
            logger.warning(f"No destination {edge.name} {edge.destination_id} from {edge.source_id}")
            continue
        source_resource = graph.nodes.get(edge.source_id)['resource']
        destination_resource = graph.nodes.get(edge.destination_id)['resource']
        source_resource.didResolveReference(edge.destination_id, destination_resource)
        graph.add_edge(edge.source_id, edge.destination_id, name=edge.name)
        # add a reverse link back
        graph.add_edge(edge.destination_id, edge.source_id, name=f"{edge.name}_")
        logger.debug(f"graph add edge {edge}")
    assert graph.number_of_nodes() == resource_count
    assert resource_count >= expected_resource_count, resource_count
    assert len(graph.edges) > 0
    logger.debug(f"Graph {graph.graph['name']} nodes: {graph.number_of_nodes()} edges: {graph.number_of_edges()}")
    return graph


def _process_fhir_file(graph, edges, file_path, resource_count, strict):
    """Load file_path into graph, populate edges with EdgeInfo."""
    for resource in read_resources(file_path, strict=strict):
        # add node to graph
        node_id = f"{resource.resource_type}/{resource.id}"
        graph.add_node(node_id, resource=resource)
        logger.debug(f"graph add node {node_id} {file_path}")
        # inspect properties, look for references, xform to edges
        has_variable_reference = _find_references_in_variables(edges, node_id, resource)
        has_extension_reference = _find_references_in_extension(edges, node_id, resource)
        if not (has_variable_reference or has_extension_reference):
            logger.debug(f"No references found for node {node_id} {file_path}")
        resource_count += 1
    return resource_count


def _find_references_in_extension(edges, node_id, resource):
    """Find any reference in extensions, populate edges with EdgeInfo."""
    has_reference = False
    if resource.extension:
        for extension in resource.extension:
            if extension.valueReference:
                variable_name = extension.url.split('/')[-1]
                ref_id = extension.valueReference.processedReferenceIdentifier()
                edges.append(EdgeInfo(node_id, ref_id, variable_name))
                has_reference = True
    return has_reference


def _find_references_in_variables(edges, node_id, resource):
    """Find any reference in public variables, populate edges with EdgeInfo."""
    has_reference = False
    for variable_name, variable in vars(resource).items():
        if not variable:
            continue
        if isinstance(variable, list):
            items = variable
        else:
            items = [variable]
        for item in items:
            if not isinstance(item, FHIRReference):
                continue
            ref_id = item.processedReferenceIdentifier()
            edges.append(EdgeInfo(node_id, ref_id, variable_name))
            has_reference = True
    return has_reference


def summarize_graph(graph) -> nx.Graph:
    """Create a graph of node and edge counts"""
    summary_graph = nx.MultiDiGraph(name=f"{graph.graph['name']}-summary")
    node_counts = defaultdict(int)
    edge_counts = defaultdict(int)
    for node in graph.nodes:
        resource = graph.nodes[node]['resource']
        node_counts[resource.resource_type] += 1
    for edge in graph.edges:
        edge_counts[EdgeInfo(edge[0].split('/')[0], edge[1].split('/')[0], graph.edges[edge]['name'])] += 1
    for resource_type, count in node_counts.items():
        summary_graph.add_node(resource_type, count=count)
        logger.debug(f"summary_graph add node {resource_type} {count}")
    for edge, count in edge_counts.items():
        summary_graph.add_edge(edge.source_id, edge.destination_id, name=edge.name, count=count)
        logger.debug(f"summary_graph add edge {edge} {count}")
    logger.debug(f"SummaryGraph {summary_graph.graph['name']} nodes: {summary_graph.number_of_nodes()} edges: {summary_graph.number_of_edges()}")
    return summary_graph


def draw_graph(graph, path=None, layout='planar_layout', title=None):
    """Visualize a graph."""

    node_dict = {}
    edge_dict = {}

    if not path and 'name' in graph.graph:
        path = f"/tmp/{graph.graph['name']}.png"
    if not path:
        path = "/tmp/graph.png"
    if not title and 'name' in graph.graph:
        title = graph.graph['name']
    if not title:
        title = ''

    for node in graph.nodes:
        node_dict[node] = f"{node}\n"
        node_dict[node] += ':'.join([str(v) for v in graph.nodes[node].values() if isinstance(v, (type(None), str, int, float, bool))])

    for edge in graph.edges:
        edge_dict[edge] = ':'.join([str(v) for v in graph.nodes[node].values() if isinstance(v, (type(None), str, int, float, bool))])

    layout_func = getattr(nx, layout)
    pos = layout_func(graph)
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))
    nx.draw(graph, pos, ax=ax, with_labels=True, labels=node_dict, node_size=6000, node_color='w', alpha=0.9,
            edgecolors="black")
    # nx.draw_networkx_edge_labels(
    #     graph, pos,
    #     edge_labels=edge_dict,
    # )
    plt.title(title)
    plt.tight_layout()
    plt.axis('off')

    plt.savefig(path)
    logger.debug(f"Wrote png to {path}")
