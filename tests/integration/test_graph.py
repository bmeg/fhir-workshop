import os
import tempfile
from collections import namedtuple, defaultdict
import logging

from fhir_workshop.graph import load_graph, draw_graph, summarize_graph, find_by_resource_type, find_nearest

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


def test_ncpi(ncpi_file_paths, tmp_dir, manual_inspect):
    """Ensure that NCPI examples are marshalled into FHIR resources"""

    # details
    graph = load_graph('ncpi', ncpi_file_paths, expected_resource_count=12)
    path = os.path.join(tmp_dir, 'ncpi.png')
    draw_graph(graph, path=path)
    assert os.path.isfile(path)
    if not manual_inspect:
        os.unlink(path)

    # summary
    path = os.path.join(tmp_dir, 'ncpi-summary.png')
    summary_graph = summarize_graph(graph)
    draw_graph(summary_graph, path=path)
    assert os.path.isfile(path)
    if not manual_inspect:
        os.unlink(path)

    # ensure we can navigate using fhir to resolved references
    research_study = graph.nodes['ResearchStudy/research-study-example-1']['resource']
    assert research_study.__class__.__name__ == 'ResearchStudy'
    assert research_study.resource_type == 'ResearchStudy'
    assert research_study.id == 'research-study-example-1'

    principal_investigator = research_study.principalInvestigator.resolved()
    assert principal_investigator
    assert principal_investigator.__class__.__name__ == 'PractitionerRole'
    assert principal_investigator.resource_type == 'PractitionerRole'
    assert principal_investigator.id == 'practitioner-role-example-1'

    # ensure that bidirectional edge drawn
    edges = graph.edges('ResearchStudy/research-study-example-1')
    assert 'ResearchSubject/research-subject-example-3' in [destination for source, destination in edges]

    # make sure we can navigate, returns tuple of id and attribute ids
    patients = find_by_resource_type(graph, 'Patient')
    assert len(patients) == 2, "should have 2 patients"
    assert len([dict_ for name, dict_ in patients if dict_]) == 2, "should return dicts as well"

    #
    research_studies = find_nearest(graph, 'Patient/patient-example-1', 'ResearchStudy')
    assert len(research_studies) > 0, "Should traverse Patient to ResearchStudy"

    # ensure extensions mapped
    # "retrieve" the patient
    patient_example_3 = graph.nodes['Patient/patient-example-3']['resource']
    simplified_js, simplified_schema = patient_example_3.as_simplified_json()
    from flatten_json import flatten
    flattened = flatten(simplified_js)
    assert flattened['extension_us-core-race'], 'extension_us-core-race null?'
    assert flattened['extension_us-core-ethnicity'], 'extension_us-core-race null?'


def test_kf(kf_file_paths, tmp_dir, manual_inspect):
    """Ensure that Kids first examples are marshalled into FHIR resources"""

    # details
    graph = load_graph('kf', kf_file_paths, expected_resource_count=44000)
    # There are too many nodes to create a detailed graph, but if you wanted to ...
    # path = os.path.join(tmp_dir, 'kf.png')
    # _draw_graph(graph, path=path)
    # assert os.path.isfile(path)
    # if not manual_inspect:
    #     os.unlink(path)

    # summary
    path = os.path.join(tmp_dir, 'kf-summary.png')
    summary_graph = summarize_graph(graph)
    draw_graph(summary_graph, path=path)
    assert os.path.isfile(path)
    if not manual_inspect:
        os.unlink(path)

    # ensure we can navigate using fhir to resolved references
    research_study = graph.nodes['ResearchStudy/100031']['resource']
    assert research_study.__class__.__name__ == 'ResearchStudy'
    assert research_study.resource_type == 'ResearchStudy'
    assert research_study.id == '100031'

    principal_investigator = research_study.principalInvestigator.resolved()
    assert principal_investigator
    assert principal_investigator.__class__.__name__ == 'PractitionerRole'
    assert principal_investigator.resource_type == 'PractitionerRole'
    assert principal_investigator.id == '96500'


def test_genomics_reporting(genomic_reporting_file_paths, tmp_dir, manual_inspect):
    """Ensure that genomics_reporting examples are marshalled into FHIR resources"""
    manual_inspect = True
    if manual_inspect:
        tmp_dir = '/tmp'
    else:
        tmp_dir = tempfile.mkdtemp()

    # details
    graph = load_graph('genomic_reporting', genomic_reporting_file_paths, expected_resource_count=10)
    path = os.path.join(tmp_dir, 'genomic_reporting.png')
    draw_graph(graph, path=path, layout='spring_layout')
    assert os.path.isfile(path)
    if not manual_inspect:
        os.unlink(path)
    else:
        logger.info(path)

    # summary
    path = os.path.join(tmp_dir, 'genomic_reporting-summary.png')
    summary_graph = summarize_graph(graph)
    draw_graph(summary_graph, path=path)
    assert os.path.isfile(path)
    if not manual_inspect:
        os.unlink(path)
    else:
        logger.info(path)

    # ensure we can navigate using fhir to resolved references
    observation = graph.nodes['Observation/Inline-Instance-for-oncologyexamples-r4-14']['resource']
    assert observation.__class__.__name__ == 'Observation'
    assert observation.resource_type == 'Observation'
    assert observation.id == 'Inline-Instance-for-oncologyexamples-r4-14'
    # validate that references in extensions are navigable
    for extension in observation.extension:
        if extension.valueReference:
            variable_name = extension.url.split('/')[-1]
            resolved_resource = extension.valueReference.resolved()
            assert resolved_resource, f"{variable_name} cannot resolve reference"
            if variable_name == 'therapy-assessed':
                plan_definition = resolved_resource
                assert plan_definition.__class__.__name__ == 'PlanDefinition'
                assert plan_definition.resource_type == 'PlanDefinition'
                assert plan_definition.id == 'PlanDefRuxolitinib'


def test_synthea(synthea_file_paths, tmp_dir, manual_inspect):
    """Ensure that genomics_reporting examples are marshalled into FHIR resources"""
    manual_inspect = True
    if manual_inspect:
        tmp_dir = '/tmp'
    else:
        tmp_dir = tempfile.mkdtemp()

    # details
    graph = load_graph('synthea', synthea_file_paths, expected_resource_count=104000, strict=False)
    # path = os.path.join(tmp_dir, 'synthea.png')
    # draw_graph(graph, path=path, layout='spring_layout')
    # assert os.path.isfile(path)
    # if not manual_inspect:
    #     os.unlink(path)
    # else:
    #     logger.info(path)

    # summary
    path = os.path.join(tmp_dir, 'synthea-summary.png')
    summary_graph = summarize_graph(graph)
    draw_graph(summary_graph, path=path)
    assert os.path.isfile(path)
    if not manual_inspect:
        os.unlink(path)
    else:
        logger.info(path)
