import pandas as pd
from fair.findable import findable
from fair.accessible import accessible
from fair.interoperable import interoperable
from fair.reproducible import reproducible
import numpy as np
from datetime import datetime
import os,time,sys
import json,json_normalize
import fairhelp
import streamlit as st

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
def SearchInstance_data_type(data_type,size=None):
  size = size if size is not None else 1000
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
def find_datasets_by_assays(size=None):
  ####data_type = 'Visium (no probes)' not finded
  data_type_list =['CODEX','IMC 2D','10X Multiome']
  ''','Bulk ATACseq','snATACseq','sciATACseq',
              'sciRNAseq','RNAseq (10x Genomics v3)','scRNAseq (10x Genomics v2)',
              'scRNAseq (10x Genomics v3)','snRNAseq (10x Genomics v3)',
              'snRNAseq (SNARE-seq2)','SNARE-seq2','seqFISH']#,'Visium (no probes)']'''
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

# search all datasets using hubmap_id by universities 
# return dict
def find_by_university(unique_universities,size):
  list_datasets = {}
  size
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
    count = 0 
    for l in list_datasets.keys():
        print(f'{l}, {len(list_datasets[l])}')
        count += 1
        for dataset in list_datasets[l]:
            records.append({
                "hubmap_id": getattr(dataset, "hubmap_id", None),
                "group_name": getattr(dataset, "group_name", None),
                "dataset_type": getattr(dataset, "dataset_type", None)  # change if needed
            }) 
            print(count)

    df = pd.DataFrame(records)
    return df


##################
# main 
##################
# search actual group_names
def names_group_list():
  #size = 50
  assay_dict = find_datasets_by_assays(size=300)
  list_uni = create_list(assay_dict)
  return unique_list_names(list_uni)

def list_of_names_df():
    size = 300
    assay_dict = find_datasets_by_assays(size)
    list_uni = create_list(assay_dict)

    unique_universities = unique_list_names(list_uni)
    list_datasets = find_by_university(unique_universities,size)
    df = create_df(list_datasets)
    return df

########################
# need to use first 
# names_group_list
# display results by different things

# general function
def process_fair_multi_datastes(df):
    #fair_json = pd.read_json('fair/fair_results.json')
    all_assay_results = [] 

    for dataset in df.iloc:
        hubmap_id = str(dataset['hubmap_id'])
        
        is_findable,score_findable = findable((hubmap_id))
        is_accessible,score_accessible = accessible(hubmap_id)
        is_interoperable,score_interoperable = interoperable(hubmap_id)
        is_reproducible,score_reproducible = reproducible(hubmap_id)
    
        fair = [is_findable, is_accessible, is_interoperable, is_reproducible]
    
        #score =[score_findable, score_accessible,score_interoperable,
        #        score_reproducible]
    
        results = {
          'group_name': dataset['group_name'],
          'hubmap_id': hubmap_id,
          'dataset_type': dataset['dataset_type'],
          'fair': fair
        }
        try:
          results['data_types'] = dataset['data_types']
        except:
          results['data_types'] = None
        all_assay_results.append(results)
    return all_assay_results

def mean_fair_results(all_assay_results):
    # store only mean of all results
    f, a, i, r = [[] for _ in range(4)]
    for data in all_assay_results:
        try :
            f.append(data[0])
            a.append(data[1])
            i.append(data[2])
            r.append(data[3])
        except:
            print(f'ERROR:\n\t{data}')
    results = []
    results.append(np.mean(f))
    results.append(np.mean(a))
    results.append(np.mean(i))
    results.append(np.mean(r))
    return results

# dataset exist in the json with the fair calculations
def find_fair_results(df):
  all = []
  for record in df.iloc:
    all.append(record['fair'])
  return all

###########################
# search functions 
###########################

# Search by lab
def search_by_lab(df,name):
    df = df[df['group_name'] == name]
    all_assay_results = find_fair_results(df)
    return all_assay_results

# Search by assay
def search_by_assay(df,assay):
    df = df[df['dataset_type'] == assay]
    all_assay_results = find_fair_results(df)
    return all_assay_results

# Search by lab and assay
def search_by_lab_assay(df,name,assay):
    df = df[df['group_name'] == name]
    df = df[df['dataset_type'] == assay]
    all_assay_results = find_fair_results(df)
    return all_assay_results

# Search all datasets
def search_all_id(df):
    all_assay_results = find_fair_results(df)
    return all_assay_results

# Search by HuBMAP ID
def search_by_id(df,hubmap_id):
    df = df[df['hubmap_id'] == hubmap_id]
    all_assay_results = find_fair_results(df)
    print(f'Hubmap ID search: {all_assay_results}')
    return all_assay_results

###########################
def create_heatmap_for(result, result_for):
        # ────────────────────────────────
        # Display Individual Scores
        # result = mean_fair_results(values)
        # result for = lab name or assay name or lab/assay
        # ────────────────────────────────
        findable, accessible, interoperable, reproducible = result

        st.subheader("📊 FAIR Scores")
        st.markdown(f"- **Findable:** {findable:.2f}")
        st.markdown(f"- **Accessible:** {accessible:.2f}")
        st.markdown(f"- **Interoperable:** {interoperable:.2f}")
        st.markdown(f"- **Reproducible:** {reproducible:.2f}")

        # ────────────────────────────────
        # Create and Display FAIR Plot
        # ────────────────────────────────

        st.subheader("🖼️ FAIR Heatmap")

        output_file = f"FAIR_{result_for}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.png"
        fairhelp.create_fair_plot(
            np.array(result).reshape(2, 2),
            output_file=output_file,
            scale=100,
            dpi=100,
            curated=False,
        )

        st.image(output_file, caption=f"FAIR Heatmap {result_for}")

###########################
def read_json_fair(file=None):
    if file is None:
        file = "/fair/fair_results.json"
    
    try:
        with open(file) as f:
            data = json.load(f)
        json_list = pd.DataFrame(data)
        list_dicts = json_list[0].tolist()
        return pd.DataFrame(list_dicts)

    except Exception as e:
        print(f'Not able to read the fair results file: {e}')

def group_list(df):
  try:
    df = df.dropna(subset=['group_name'])
    return df['group_name'].unique()
  except:
    pass

def type_list(df):
  try:
    df = df.dropna(subset=['dataset_type'])
    return df['dataset_type'].unique()
  except:
    pass
###########################
  # check datasets
def check_datasets(df,json_data):
  # individually each dataset to see if it its in the json
  for dataset in json_data:
    hubmap_id = dataset['hubmap_id']
    # if exist in json
    if hubmap_id not in df['hubmap_id'].values:
      print(f'Not exist in json {hubmap_id}')
      id = search_by_id(hubmap_id)
