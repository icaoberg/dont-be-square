import os
import time
import json   # switched from yaml to json
from fair.utils import process_fair_multi_datastes
from fair.utils import names_group_list
import pandas as pd
from hubmap_sdk import SearchSdk
from hubmap_sdk import EntitySdk
from hubmap_sdk.dataset import Dataset


# Changing these pandas options would allow us to display an entire dataframe if we desired
pd.options.display.max_rows = None
pd.options.display.max_columns = None


#In this example, the token and service url are being retrieved from a configuration file.
url = 'https://search.api.hubmapconsortium.org/v3/'
token = None
search_instance = SearchSdk(token, url)

#In this example, the token and service url are being retrieved from a configuration file.
url = 'https://entity.api.hubmapconsortium.org/'
token = None
entity_instance = EntitySdk(token, url)
  
# use the hubmap search sdk to find datasets by university group name 

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

# convert search query to list of dataset objects
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

# find all the datasets by university group name
# have a list of group names
# ideal size to cover all datasetes per uni should be 1,700
# return a dict of lists of dataset objects
def find_by_university(size):
  all_groups = [
    "University of California San Diego TMC","Stanford TMC",
    "TMC - University of Pennsylvania",
    "Vanderbilt TMC",
    "TMC - University of California San Diego focusing on female reproduction",
    "University of Rochester Medical Center TMC",
    "Stanford RTI",
    "University of Florida TMC",
    "California Institute of Technology TMC",
    "Broad Institute RTI",
    "General Electric RTI",
    "Washington University Kidney TMC",
    "TMC - University of Connecticut and Scripps",
    "Stanford University Bone Marrow TMC",
    "TTD - University of San Diego and City of Hope",
    "Purdue TTD",
    "EXT - Human Cell Atlas",
    "Northwestern RTI",
    "TMC - Children's Hospital of Philadelphia",
    "TC - University of Florida",
    "TTD - Pacific Northwest National Laboratory",
    "TTD - Penn State University and Columbia University"
    ]

  list_datasets = {}
  # Iterate over the elements of the NumPy array within the list
  #for name in unique_universities[0]:
  for name in all_groups:
    query = SearchInstance_group_name(name,size)
    list_datasets[name] = convert_to_dataset(query)
    time.sleep(1) 
  return list_datasets

# create a dataset.object to a df 
def dataset_to_df(dataset):
    """
    Convert a single hubmap_sdk.dataset.Dataset object to a one-row DataFrame.
    Handles variable attributes dynamically.
    """
    attrs = {}
    for attr in dir(dataset):
        if attr.startswith("_"):
            continue  # skip private
        try:
            value = getattr(dataset, attr)
        except Exception:
            continue
        if callable(value):
            continue
        attrs[attr] = value
    return pd.DataFrame([attrs])

# take a list of objects and filter it for only dataset.objects to list of dfs
def list_objct_to_list_df(list_datasets):
    list_keys = list(list_datasets.keys())
    df_list = []

    for i, obj_list in enumerate(list_datasets.values()):
        print(f'Processing university {i+1}: {list_keys[i]} with {len(obj_list)} datasets')

        for j, dataset in enumerate(obj_list):
            if isinstance(dataset, Dataset):
                try:
                    df = dataset_to_df(dataset)
                    df_list.append(df)
                    print(f'  [{j+1}/{len(obj_list)}] Added dataset for {list_keys[i]}')
                except Exception as e:
                    continue

    print(f'\nTotal DataFrames created: {len(df_list)}')
    return df_list

  
##################
# main 
##################
if __name__ == "__main__":
    # ideal size to cover all datasetes per uni should be 1,700
    list_uni = find_by_university(1700)
    df_list = list_objct_to_list_df(list_uni)
    
    file_path = "fair/fair_results.json" 

    # check if JSON created
    #if not os.path.exists(file_path):

    # not created
    #if not os.path.exists('./fair/hubmap_data.csv'):
    list_datasets = []
    print('Creating fair_list of datasets scoring')
    for i, df in enumerate(df_list):
        print(f'Processing dataframe {i}')
        list_datasets.append(process_fair_multi_datastes(df))

        print('write to json')
        with open(file_path, 'w') as file:
            json.dump(list_datasets, file, indent=4) 
            print(f'JSON saved')
    print('json created completed')

    #############################
