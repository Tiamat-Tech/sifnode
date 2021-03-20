import argparse
import json
import logging
import os
import tempfile
import textwrap
from typing import List

import sys
import time

import json
import socket
import time
from dataclasses import dataclass


@dataclass
class SifchainCmdParameters(dict):
    def as_json(self):
        return json.dumps(self.__dict__)


@dataclass
class SifchainCmdInput(SifchainCmdParameters):
    pass


@dataclass
class SifchainCmdOutput(SifchainCmdParameters):
    pass


def wait_for_port(host, port) -> bool:
    while True:
        try:
            with socket.create_connection((host, port)):
                return True
        except ConnectionRefusedError as e:
            time.sleep(1)
    return False
