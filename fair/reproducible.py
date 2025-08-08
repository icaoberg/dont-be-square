import json
import os
import random
import requests
import numpy as np
from tqdm import tqdm
from datetime import datetime
from typing import Dict
from fair.findable import __get_metadata

def reproducible(dataset_id: str) -> float:
    metadata = __get_metadata(dataset_id)
    score = [
        __average_metadata_success(dataset_id)
    ]
    print(f'R: {score}')
    result = np.mean(score)
    return result

# ─────────────────────────────────────────────────────────────
# Helper Methods Section
# Add any additional helper methods below this block.
# These should be utility functions to support the main logic.
# ─────────────────────────────────────────────────────────────
    
def __average_metadata_success(hubmap_id: str) -> float:
    num_trials = random.randint(3, 10)
    success_count = 0

    for _ in tqdm(range(num_trials)):
        metadata = __get_metadata(hubmap_id)
        if metadata and isinstance(metadata, dict) and "error" not in metadata and len(metadata) > 0:
            success_count += 1

    result = success_count / num_trials
    return result