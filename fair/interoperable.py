import json
import os
import random
import requests
import numpy as np
from tqdm import tqdm
from datetime import datetime
from typing import Dict
import logging
from fair.findable import __get_metadata
logger = logging.getLogger(__name__)


def interoperable(dataset_id: str) -> float:
    metadata = __get_metadata(dataset_id)
    score = [
        __has_genetic_sequences(metadata), #1
        __has_assay_category(metadata), # nolo estat
        __has_assay_type(metadata), #0 no esta 
        __has_contributors_path(metadata), #0 tiene
        __has_version(metadata) #1 no esta 
    ]
    print(f'I: {score}')
    result = np.mean(score)
    return result

# ─────────────────────────────────────────────────────────────
# Helper Methods Section
# Add any additional helper methods below this block.
# These should be utility functions to support the main logic.
# ─────────────────────────────────────────────────────────────
def __has_genetic_sequences(metadata: dict) -> int:
    logger.info("__has_genetic_sequences() started")
    result = 1 if "contains_human_genetic_sequences" in metadata else 0
    logger.info(f"__has_genetic_sequences() completed with result {result}")
    return result

def __has_assay_category(metadata: dict) -> int:
    logger.info("__has_assay_category() started")
    result = 1 if "assay_category" in metadata['metadata'] else 0
    logger.info(f"__has_assay_category() completed with result {result}")
    return result

def __has_assay_type(metadata: dict) -> int:
    logger.info("__has_assay_type() started")
    result = 1 if "assay_type" in metadata['metadata'] else 0
    logger.info(f"__has_assay_type() completed with result {result}")
    return result

def __has_contributors_path(metadata: dict) -> int:
    logger.info("__has_hubmap_id() started")
    result = 1 if "contributors_path" in metadata['metadata'] else 0
    logger.info(f"__has_contributors_path() completed with result {result}")
    return result

def __has_version(metadata: dict) -> int:
    logger.info("__has_version() started")
    result = 1 if "version" in metadata['metadata'] else 0
    logger.info(f"__has_version() completed with result {result}")
    return result
