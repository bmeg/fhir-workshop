import tempfile

from pytest import fixture
import fhir_workshop.manifests


@fixture
def ncpi_file_paths():
    return fhir_workshop.manifests.ncpi_file_paths()


@fixture
def kf_file_paths():
    return fhir_workshop.manifests.kf_file_paths()


@fixture
def dbgap_file_paths():
    return fhir_workshop.manifests.dbgap_file_paths()


@fixture
def synthea_file_paths():
    return fhir_workshop.manifests.synthea_file_paths()


@fixture
def genomic_reporting_file_paths():
    return fhir_workshop.manifests.genomic_reporting_file_paths()


@fixture
def anvil_file_paths():
    return fhir_workshop.manifests.anvil_file_paths()


@fixture
def phs000424_file_paths():
    return fhir_workshop.manifests.phs000424_file_paths()


@fixture
def gtex_v8_file_paths():
    return fhir_workshop.manifests.gtex_v8_file_paths()


@fixture
def manual_inspect():
    """If true, don't delete test output files."""
    return True


@fixture
def tmp_dir(manual_inspect):
    """Where should we store any files."""
    if manual_inspect:
        return '/tmp'
    else:
        return tempfile.mkdtemp()
