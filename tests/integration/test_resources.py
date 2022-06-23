from fhir_workshop.resources import read_resources
from fhirclient.models.domainresource import DomainResource


def _load_resources(file_paths, expected_resource_count, strict=True):
    """Ensure all records can be marshalled into a FHIR resource."""
    resource_count = 0
    for file_path in file_paths:
        for resource in read_resources(file_path, strict=strict):
            assert isinstance(resource,
                              DomainResource), f"Error reading {file_path}. Should be DomainResource, was {resource.__class__}"
            resource_count += 1
    assert resource_count > expected_resource_count, resource_count


def test_ncpi(ncpi_file_paths):
    """Ensure that NCPI examples are marshalled into FHIR resources"""
    _load_resources(ncpi_file_paths, expected_resource_count=10)


def test_kf(kf_file_paths):
    """Ensure that kids first study is marshalled into FHIR resources"""
    _load_resources(kf_file_paths, expected_resource_count=44000)


def test_dbgap(dbgap_file_paths):
    """Ensure that dbgap is marshalled into FHIR resources.

    Note: 'Non-optional property "status" on <fhirclient.models.observation.Observation object at 0x109e0c190> is missing'
    """
    _load_resources(dbgap_file_paths, expected_resource_count=2000, strict=False)


def test_synthea(synthea_file_paths):
    """Ensure that synthea is marshalled into FHIR resources"""
    _load_resources(synthea_file_paths, expected_resource_count=104000, strict=False)


def test_genomic_reporting(genomic_reporting_file_paths):
    """Ensure that genomic_reporting is marshalled into FHIR resources"""
    _load_resources(genomic_reporting_file_paths, expected_resource_count=10)


def test_anvil(anvil_file_paths):
    """Ensure that anvil is marshalled into FHIR resources"""
    _load_resources(anvil_file_paths, expected_resource_count=15000)


def test_phs000424(phs000424_file_paths):
    """Ensure that GTEx is marshalled into FHIR resources"""
    _load_resources(phs000424_file_paths, expected_resource_count=71494)
