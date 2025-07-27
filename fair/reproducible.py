import json
import os
import random
import requests
import numpy as np
from tqdm import tqdm
from datetime import datetime
from typing import Dict
from findable import __get_metadata

def reproducible(dataset_id: str) -> float:
    metadata = __get_metadata(dataset_id)
    score = [
        __average_metadata_success(hubmap_id: str)
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
    
def __average_metadata_success(hubmap_id: str) -> float:
    num_trials = random.randint(3, 10)
    success_count = 0

    for _ in tqdm(range(num_trials)):
        metadata = __get_metadata(hubmap_id)
        if metadata and isinstance(metadata, dict) and "error" not in metadata and len(metadata) > 0:
            success_count += 1

    result = success_count / num_trials
    return result