import pandas as pd
import json
from plotly import express as px
from pprint import pprint

# Changing these pandas options would allow us to display an entire dataframe if we desired
pd.options.display.max_rows = None
pd.options.display.max_columns = None

from hubmap_sdk import SearchSdk
from hubmap_sdk import EntitySdk

#In this example, the token and service url are being retrieved from a configuration file.
url = 'https://search.api.hubmapconsortium.org/v3/'
token = None
search_instance = SearchSdk(token, url)

#In this example, the token and service url are being retrieved from a configuration file.
url = 'https://entity.api.hubmapconsortium.org/'
token = None
entity_instance = EntitySdk(token, url)

##########################
# General Functions
##########################

# ElasticSearch
# make the search query by data_type
def SearchInstance_data_type(data_type,size):
  search_query = {
    "query": {
      "match": {
        "data_types": data_type
      }
    },
      'size': size,
      "stored_fields": "_id" # For our purposes, we only need the ID of each dataset.
  }
  return search_query

# make the search query by group name
def SearchInstance_group_name(group_name,size):
  search_query = {
    "query": {
      "match": {
        'group_name': group_name
        #"data_types": data_type # "LC-MS Top Down" # Change in the data type if necessary
      }
    },
    'size': size,
      "stored_fields": "_id" # For our purposes, we only need the ID of each dataset.
  }
  return search_query

# convert de data type search results into a dic of datasets
def convert_to_dataset(search_query):
  # Make a list of the results found from the hubmap sdk, using the query
  results_dict = search_instance.search(search_query)
  list_of_hits = results_dict["hits"]["hits"]
  list_of_datasets = []

  # search all the elements that were true in the queary search
  for hit in list_of_hits:
      dataset = entity_instance.get_entity_by_id(hit["_id"])
      list_of_datasets.append(dataset)

  return list_of_datasets

##########################
# Working Functions
##########################

# search datasets by assays and specify size
# return dict of assay types, inside each assay type:
#   list of datasets
def find_datasets_by_assays(size):
  ####data_type = 'Visium (no probes)' not finded
  data_type_list =['CODEX','IMC 2D','10X Multiome','Bulk ATACseq','snATACseq','sciATACseq',
              'sciRNAseq','RNAseq (10x Genomics v3)','scRNAseq (10x Genomics v2)',
              'scRNAseq (10x Genomics v3)','snRNAseq (10x Genomics v3)',
              'snRNAseq (SNARE-seq2)','SNARE-seq2','seqFISH']#,'Visium (no probes)']
  assay_dict = {}
  #=======================
  for assay in data_type_list:
    search_query = SearchInstance_data_type(assay,size)
    assay_dict[assay] = convert_to_dataset(search_query)
  return assay_dict

# Create a list of universities names from the datasets
# return list of names for all datasets
def create_list(assay_dict):
  list_uni = []
  for assay in assay_dict.keys():
    print(f'{assay},{len(assay_dict[assay])}')
    for dataset in assay_dict[assay]:
      list_uni.append(dataset.group_name)
  return list_uni

# unique universities names with existing datasets
# return list
def unique_list_names(list_uni):
  df_list_name = pd.DataFrame(list_uni)
  df_list_name.columns = ['group_name']
  return [df_list_name['group_name'].unique()]

# search all datasets hubmap_id by universities 
# return dict
def find_by_university(unique_universities,size):
  list_datasets = {}
  for name in unique_universities:
    query = SearchInstance_group_name(name,size)
    list_datasets[name] = convert_to_dataset(query)
  return list_datasets

# ussing the list of names for universities access hubmap info
# and create a df entry with hubmap id, name and dataset type 
# repeat this part with each dataset
# return df 
def create_df(list_datasets):
    records = []  # collect rows first

    for l in list_datasets.keys():
        #print(f'{l}, {len(list_datasets[l])}')
        for dataset in list_datasets[l]:
            records.append({
                "hubmap_id": getattr(dataset, "hubmap_id", None),
                "group_name": getattr(dataset, "group_name", None),
                "dataset_type": getattr(dataset, "dataset_type", None)  # change if needed
            })

    df = pd.DataFrame(records)
    return df


##################
# main 
##################
def names_group_list():
  size = 250
  assay_dict = find_datasets_by_assays(size)
  list_uni = create_list(assay_dict)
  return unique_list_names(list_uni)

def list_of_names_df():
    size = 300
    assay_dict = find_datasets_by_assays(size)
    list_uni = create_list(assay_dict)

    unique_universities = unique_list_names(list_uni)
    list_datasets = find_by_university(unique_universities,size)
    df = create_df(list_datasets)
    #print(df.head())
    return df


def existing_names_to_df():
  size = 300
  unique_universities = ['University of Florida TMC', 'Stanford TMC',
       'TMC - University of California San Diego focusing on female reproduction',
       'California Institute of Technology TMC',
       'University of California San Diego TMC',
       'TMC - University of Connecticut and Scripps',
       'EXT - Human Cell Atlas'
       ]
  print(unique_universities)
  list_datasets = find_by_university(unique_universities,size)
  df = create_df(list_datasets)
  return df 