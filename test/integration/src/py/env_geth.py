import json
import logging
import os
import subprocess
import time
from dataclasses import dataclass
from functools import lru_cache

@dataclass
class GethInput:
    chain_id: str = ""
    network_id: str = ""


@dataclass
class GethOutput:
    input: GethInput
    chain_id: str = ""
    network_id: str = ""
