from typing import Iterator, Iterable
import json
import importlib
import logging

from fhirclient.models.domainresource import DomainResource

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


def _sniff(file_path) -> Iterator[dict]:
    """Sniff json or ndjson, yield json raw dictionary."""
    with open(file_path, "r") as fhir_resource_file:
        try:
            # see if this file, in its entirety is json
            fhir_resources = json.load(fhir_resource_file)
            if isinstance(fhir_resources, dict) and 'entry' in fhir_resources:
                # this looks like a bundle
                for entry in fhir_resources['entry']:
                    yield entry['resource']
                return
            if isinstance(fhir_resources, dict):
                # it's a single dict
                yield fhir_resources
                return
            for fhir_resource in fhir_resources:
                # it's a list
                yield fhir_resource
                return
        except json.decoder.JSONDecodeError:
            # re-try,  assume this is ndjson
            fhir_resource_file.seek(0)
            for line in fhir_resource_file:
                yield json.loads(line)


def read_resources(file_path: str, strict=True) -> Iterable[DomainResource]:
    """Read a json payload from path, marshall into fhirclient.models FHIR resource."""
    for resource_dict in _sniff(file_path):
        # dynamically import model
        assert 'resourceType' in resource_dict
        resource_type = resource_dict['resourceType']
        module_name = f"fhirclient.models.{resource_type.lower()}"
        module = importlib.import_module(module_name)
        assert module
        clazz = getattr(module, resource_type)
        assert clazz
        # create instance
        yield clazz(resource_dict, strict=strict)
