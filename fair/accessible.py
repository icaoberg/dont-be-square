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
from fair.findable import __get_metadata

logger = logging.getLogger(__name__)


def accessible(dataset_id: str) -> float:
    logger.info(f"accessible() started for {dataset_id}")
    metadata = __get_metadata(dataset_id)
    score = [
        1 if "doi_url" in metadata and __is_link_accessible(metadata["doi_url"]) else 0,
             __has_group_name(metadata),
            __has_group_uuid(metadata),
            __has_hubmap_id(metadata)
             ]
    print(f'A: {score}')

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
        response = requests.get(url, allow_redirects=True, timeout=timeout)
        success = response.status_code == 200
        logger.info(f"URL {url} is {'accessible' if success else 'not accessible'}")
        return success
    except requests.RequestException:
        logger.warning(f"URL check failed: {url}")
        return False
    
def __has_group_name(metadata: dict) -> int:
    logger.info("__has_group_name() started")
    result = 1 if "group_name" in metadata else 0
    logger.info(f"__has_group_name() completed with result {result}")
    return result

def __has_group_uuid(metadata: dict) -> int:
    logger.info("__has_group_uuid() started")
    result = 1 if "group_uuid" in metadata else 0
    logger.info(f"__has_group_uuid() completed with result {result}")
    return result

def __has_hubmap_id(metadata: dict) -> int:
    logger.info("__has_hubmap_id() started")
    result = 1 if "hubmap_id" in metadata else 0
    logger.info(f"__has_hubmap_id() completed with result {result}")
    return result
