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

def accessible(dataset_id: str) -> float:
    logger.info(f"accessible() started for {dataset_id}")
    metadata = __get_metadata(dataset_id)
    score = [
        __is_published(metadata),
        __no_error(metadata),
        __has_antibodies(metadata),
        __has_uuid(metadata),
        __is_dataset_entity(metadata),
    ]
    result = np.mean(score)
    logger.info(f"accessible() completed for {dataset_id} with score {result}")
    return result

# ─────────────────────────────────────────────────────────────
# Helper Methods Section
# Add any additional helper methods below this block.
# These should be utility functions to support the main logic.
# ─────────────────────────────────────────────────────────────

def __is_link_accessible(url: str, timeout: int = 5) -> bool:
    logger.info(f"__is_link_accessible() checking URL: {url}")
    try:
        response = requests.head(url, allow_redirects=True, timeout=timeout)
        success = response.status_code == 200
        logger.info(f"URL {url} is {'accessible' if success else 'not accessible'}")
        return success
    except requests.RequestException:
        logger.warning(f"URL check failed: {url}")
        return False
    

