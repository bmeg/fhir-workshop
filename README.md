
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
Our first decision is how to bridge the gap between FHIR’s document model and the data frame's property approaches. Essentially that came down to decompose - expand the document into a set of individual graph nodes of arbitrary depth, or flatten - reshape the data to remove nesting. We selected flatten as it reduces complexity in the resulting graph and more naturally fits with the columnar data stores and spreadsheet like interfaces in destination systems. 
Our design choice to flatten the FHIR resource presented an additional challenge, the readability of the resulting data frame in the target tool. By default, pfb_fhir will flatten all of these fields, supporting an “unflatten” operation to re-constitute a FHIR resource. This has a downside, the readability of the resulting data frame. For example, a typical Patient resource might have over 70 separate fields in the FHIR resource. Over half of these fields are scaffolding, supporting namespacing, vocabularies and rendering. The result is attribute names with embedded array indices e.g. “identifier_3_type_coding_0_code”. pfb_fhir’s simplify option will collapse single item arrays, extract coding attributes, collapse extensions and identifiers resulting in a data frame with roughly half the number of attributes.


### simplify
FHIR resources are heavily namespaced and verbose. As such, the resulting data frame is heavily decorated with these urls and enumeration. The simplify option is a first attempt to make the resulting nodes more `data frame friendly`.


## setup


* Open the terra terminal, navigate to `ncpi-fhir-code-a-thon/edit/fhir-workshop`
* Clone the `git clone https://github.com/bmeg/fhir-workshop`
* Install the dependencies `pip install -r fhir-workshop/requirements.txt`