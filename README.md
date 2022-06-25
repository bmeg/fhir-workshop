
# ncpi-fhir-code-a-thon


## server-less environment

In preparation for the workshop, we have extracted raw FHIR documents from a variety of sources and loaded them into the workspace's filesystem.  As a convience, the fhir_workshop package provides mechanism to load data model classes, visualize the resources and provide basic lookup services.


![image](https://user-images.githubusercontent.com/47808/175333024-efe2f94b-bf8a-4545-8d25-604de6f95257.png)



## use cases


We provided several demonstration datasets repurposed from our test fixtures.  We combined them using cytoscape into an aggregate view.  The relative size of the node indicates how many sources implemented the resource.  The relative thickness of the edge indicates how many sources implemented the relationship.  

Notebooks are provided for each use case.

![image](https://user-images.githubusercontent.com/47808/175310198-d519e6f7-f67e-4aba-b260-ac543a5f10d6.png)



## data frames

### nested document representation

Our first decision is how to bridge the gap between FHIR’s document model and the data frame's property approaches. 
Essentially that came down to decompose - expand the document into a set of individual graph nodes of arbitrary depth, or flatten - reshape the data to remove nesting. 
We selected flatten as it reduces complexity in the resulting graph and more naturally fits with the columnar data stores and spreadsheet like interfaces in destination systems, e.g. Terra's data tables or Gen3's data dictionary. 

### simplify
FHIR resources are heavily namespaced and verbose. As such, the resulting data frame is heavily decorated with these urls and enumeration. The simplify option is a first attempt to make the resulting nodes more `data frame friendly`.

### ad-hoc flattening
Each of the use cases has a different set of FHIR resources and associated links.  The notebooks have examples of customizing a data frame for the use case.

## setup


* Open the terra terminal, navigate to `<your-workspace-name-here>/edit/fhir-workshop`
* Clone the `git clone https://github.com/bmeg/fhir-workshop`
* Install the dependencies `pip install -e .`

## data retrieval

This script will use the `anvil_curl` command to export data from the Google Healthcare API.  The retrieves the token from the terra environment, and passes the search path to the google FHIR endpoint. It retrieves all entries by a=utomatically following `next` links.

From the fhir_workshop root directory:

```commandline

export FHIR_PROJECT=ncpi-fhir-cat-2022
export GOOGLE_LOCATION=us-central1
export GOOGLE_DATASET=GTEx_Open_Access
export GOOGLE_DATASTORES=gtex_v8

cd tests/fixtures
mkdir gtex_v8
cd gtex_v8

anvil_curl /Group?_count=1000 | jq -c '.entry[] | .resource' > Group.ndjson
anvil_curl /ResearchSubject?_count=1000 | jq -c '.entry[] | .resource' > ResearchSubject.ndjson
anvil_curl /ActivityDefinition?_count=1000 | jq -c '.entry[] | .resource' > ActivityDefinition.ndjson
anvil_curl /Organization?_count=1000 | jq -c '.entry[] | .resource' > Organization.ndjson
anvil_curl /ResearchStudy?_count=1000 | jq -c '.entry[] | .resource' > ResearchStudy.ndjson
anvil_curl /Patient?_count=1000 | jq -c '.entry[] | .resource' > Patient.ndjson
anvil_curl /DocumentReference?_count=1000 | jq -c '.entry[] | .resource' > DocumentReference.ndjson
anvil_curl /ObservationDefinition?_count=1000 | jq -c '.entry[] | .resource' > ObservationDefinition.ndjson
anvil_curl /ValueSet?_count=1000 | jq -c '.entry[] | .resource' > ValueSet.ndjson
anvil_curl /ConceptMap?_count=1000 | jq -c '.entry[] | .resource' > ConceptMap.ndjson
anvil_curl /CodeSystem?_count=1000 | jq -c '.entry[] | .resource' > CodeSystem.ndjson
anvil_curl /Observation?_count=1000 | jq -c '.entry[] | .resource' > Observation.ndjson
anvil_curl /Specimen?_count=1000 | jq -c '.entry[] | .resource' > Specimen.ndjson

```
