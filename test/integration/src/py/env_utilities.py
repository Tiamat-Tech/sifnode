import argparse
import json
import os
import socket
import tempfile
import textwrap
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SifchainCmdParameters(dict):
    def as_json(self):
        return json.dumps(self.__dict__)


@dataclass
class SifchainCmdInput(SifchainCmdParameters):
    pidfile: str


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


def default_cmdline_parser():
    return argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """
            start geth
            * add tokens to users in ethereum_addresses
            * don't return until geth is listening to ws and http ports
            """
        )
    )


def atomic_write(s: str, filename: str):
    output = Path(filename)
    output.unlink(missing_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", dir=os.path.dirname(output), delete=False) as temp:
        temp.write(s)
        os.link(temp.name, output)
