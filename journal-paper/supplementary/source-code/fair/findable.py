import json
import os
import random
import requests
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
from tqdm import tqdm
from datetime import datetime
from typing import Dict
import logging
import time
import requests
import streamlit as st

logger = logging.getLogger(__name__)

def explore_json(obj, path=""):
    if isinstance(obj, dict):
        print(f"Dict found at '{path}' with keys: {list(obj.keys())}\n")
        for key, value in obj.items():
            new_path = f"{path}.{key}" if path else key
            print('\n')
            explore_json(value, new_path)
    elif isinstance(obj, list):
        print(f"List found at '{path}' with {len(obj)} items: {obj}\n")


def findable(dataset_id: str) -> float:
    metadata = __get_metadata(dataset_id)
    #explore_json(metadata)

    score = [
        __no_error(metadata),
        __has_antibodies(metadata),
        __has_uuid(metadata),
        __is_dataset_entity(metadata),
        __has_title(metadata),
        __is_published(metadata)[0],
        __has_contributors(metadata),
        __has_contacts(metadata)
    ]
    print(f'F: {score}')
    result = np.mean(score)
    return result,score

# ─────────────────────────────────────────────────────────────
# Helper Methods Section
# Add any additional helper methods below this block.
# These should be utility functions to support the main logic.
# ─────────────────────────────────────────────────────────────


def __is_link_accessible(url: str, timeout: int = 5) -> bool:
    try:
        response = requests.head(url, allow_redirects=True, timeout=timeout)
        success = response.status_code == 200
        return success
    except requests.RequestException:
        return False

def __get_metadata(dataset_id: str, api_url: str = "https://entity.api.hubmapconsortium.org/entities") -> Dict:
    try:
        response = requests.get(f"{api_url}/{dataset_id}")
        response.raise_for_status()
        metadata = response.json()
        os.makedirs("JSON", exist_ok=True)
        filepath = os.path.join("JSON", f"{dataset_id}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        return metadata
    except requests.RequestException as e:
        return {"error": str(e)}

def __is_published(metadata: dict) -> bool:
    status = metadata.get("status", "Unknown")
    result = status == "Published"
    return int(result), status


def __has_uuid(metadata: dict) -> int:
    result = 1 if "uuid" in metadata else 0
    return result


def __is_dataset_entity(metadata: dict) -> int:
    result = 1 if metadata.get("entity_type") == "Dataset" else 0
    return result


def __no_error(metadata: dict) -> int:
    result = 0 if "error" in metadata else 1
    return result

def __has_antibodies(metadata: dict) -> bool:
    logger.info("__has_antibodies() started")
    score = []
    antibodies = metadata.get("antibodies", [])
    score.append(bool(antibodies))
    
    # donnt have antibodies
    if not antibodies:
        return 1 

    progress_bar = st.progress(0)
    status_text = st.empty()

    counter = 0
    status_text.text(f"Checking antibodies against UNIPROT: {counter}%")

    for antibody in tqdm(antibodies):
        counter = counter + 1
        progress_bar.progress(counter + 1)
        status_text.text(f"Checking antibodies against UNIPROT: {counter + 1}%")
        accession = antibody.get("uniprot_accession_number")
        if accession:
            url = f"https://rest.uniprot.org/uniprotkb/{accession}"
            if not __is_link_accessible(url):
                score.append(False)

            else:
                score.append(True)
    # list of true
    result = int(all(score))
    progress_bar.empty()
    status_text.empty()
    
    return result

def __has_title(metadata: dict) -> int:
    logger.info("__has_title() started")
    result = 1 if "title" in metadata else 0
    logger.info(f"__has_title() completed with result {result}")
    return result

def check_orcid(orcid_id: str):
    base_url = "https://pub.orcid.org/v3.0"
    headers = {"Accept": "application/json"}
    url = f"{base_url}/{orcid_id}"
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return True
    elif response.status_code == 404:
        return False
    else:
        return False

def __has_contributors(metadata: dict) -> int:
    logger.info("__has_contributors() started")
    result = 1 if "contributors" in metadata else 0
    if result == 0:
        return 0
    logger.info(f"__has_contributors() completed with result {result}")

    contributors = metadata['contributors'][0]

    if 'orcid' in contributors:
        orcid_value = 1
    
    elif 'orcid_id' in contributors:
        orcid_value = 2

    else:
        orcid_value = None
    #--------------------------------------
    if orcid_value == 1:
        validate_orcid_id = check_orcid(contributors['orcid'])
    
    elif orcid_value == 2:
        validate_orcid_id = check_orcid(contributors['orcid_id'])
    else:
        validate_orcid_id = None


    if validate_orcid_id and result:
        return 1
    else:
        return 0

def __has_contacts(metadata: dict) -> int:
    logger.info("__has_contacts() started")
    result = 1 if "contacts" in metadata else 0
    if result == 0:
        return 0
    
    logger.info(f"__has_contacts() completed with result {result}")
    
    contact = metadata['contacts'][0]

    if 'orcid' in contact:
        orcid_value = 1
    
    elif 'orcid_id' in contact:
        orcid_value = 2

    else:
        orcid_value = None
#--------------------------------------
    if orcid_value == 1:
        validate_orcid_id = check_orcid(contact['orcid'])
    
    elif orcid_value == 2:
        validate_orcid_id = check_orcid(contact['orcid_id'])
    else:
        validate_orcid_id = None


    if validate_orcid_id and result:
        return 1
    else:
        return 0
    

