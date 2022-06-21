
## retrieve test fixtures

```
mkdir -p tests/fixtures
cd tests/fixtures
wget https://github.com/bmeg/pfb_fhir/releases/download/latest/fixtures.zip -O fixtures.zip
```

## library setup
```python
```python
!git clone https://github.com/bmeg/fhir-workshop
!pip install deepmerge

```


## setup notebook ncpi-fhir-ig

```python
!git clone https://github.com/bmeg/fhir-workshop

import sys
# add git repo to our path
sys.path.append('./fhir-workshop')


fixtures_path = "test/fixtures"
ncpi_path = f"{fixtures_path}/ncpi"
ncpi_file_paths = f"""
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

from fhir_workshop.graph import load_graph, draw_graph, summarize_graph

graph = load_graph('ncpi', ncpi_file_paths, expected_resource_count=12)

```
