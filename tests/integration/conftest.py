import tempfile

from pytest import fixture
from glob import glob
import os
from pathlib import Path


@fixture
def fixtures_path():
    """Fixtures path."""
    return Path(os.path.dirname(os.path.abspath(__file__)), '../fixtures')
    # return 'tests/fixtures'


@fixture
def ncpi_file_paths(fixtures_path):
    """NCPI file examples."""
    ncpi_path = f"{fixtures_path}/ncpi"
    return f"""
        {ncpi_path}/examples/DocumentReference-research-document-reference-example-1.json
        {ncpi_path}/examples/Patient-patient-example-1.json
        {ncpi_path}/examples/Patient-patient-example-3.json
        {ncpi_path}/examples/ResearchSubject-research-subject-example-3.json
        {ncpi_path}/examples/Observation-family-relationship-example-4.json
        {ncpi_path}/examples/Task-task-example-2.json
        {ncpi_path}/examples/ResearchStudy-research-study-example-1.json
        {ncpi_path}/examples/Specimen-specimen-example-1.json
        {ncpi_path}/examples/PractitionerRole-practitioner-role-example-1.json
        {ncpi_path}/examples/Practitioner-practitioner-example-1.json
        {ncpi_path}/examples/Organization-organization-example-1.json
        {ncpi_path}/examples/Observation-research-study-example-1.json
    """.split()


@fixture
def kf_file_paths(fixtures_path):
    """Kids first file examples."""
    kf_path = f"{fixtures_path}/kf"
    return glob(f"{kf_path}/examples/*.ndjson")


@fixture
def dbgap_file_paths(fixtures_path):
    """dbGAP file examples."""
    dbgap_path = f"{fixtures_path}/dbgap"
    return glob(f"{dbgap_path}/examples/*.json")


@fixture
def synthea_file_paths(fixtures_path):
    """synthea file examples."""
    synthea_path = f"{fixtures_path}/synthea"
    return glob(f"{synthea_path}/filtered/*.json") + glob(f"{synthea_path}/filtered/*.ndjson")


@fixture
def genomic_reporting_file_paths(fixtures_path):
    """genomic_reporting file examples."""
    gr_path = f"{fixtures_path}/genomics-reporting"
    return [f'{gr_path}/examples/Bundle-bundle-oncologyexamples-r4.normalized.json']


@fixture
def anvil_file_paths(fixtures_path):
    """anvil file examples."""
    anvil_path = f"{fixtures_path}/anvil"
    return glob(f"{anvil_path}/fhir/public/Public/1000G-high-coverage-2019/public/*.ndjson") + glob(f"{anvil_path}/fhir/public/Public/1000G-high-coverage-2019/protected/*.ndjson")


@fixture
def manual_inspect():
    """If true, don't delete test output files."""
    return False


@fixture
def tmp_dir(manual_inspect):
    """Where should we store any files."""
    if manual_inspect:
        return '/tmp'
    else:
        return tempfile.mkdtemp()
