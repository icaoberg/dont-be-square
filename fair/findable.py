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

def findable(dataset_id: str) -> float:
    metadata = __get_metadata(dataset_id)
    score = [
        __is_published(metadata),
        __no_error(metadata),
        __has_antibodies(metadata),
        __has_uuid(metadata),
        __is_dataset_entity(metadata),
    ]
    result = np.mean(score)
    return result

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
    """
    Check whether the dataset status is 'Published'.

    Args:
        metadata (dict): Dataset metadata dictionary.

    Returns:
        bool: True if status is 'Published', False otherwise.
    """
    status = metadata.get("status", "Unknown")
    result = status == "Published"
    return result, status


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

    result = all(score)
    return result
