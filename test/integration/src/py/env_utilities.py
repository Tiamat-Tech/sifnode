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
    basedir: str
    logfile: str
    configoutputfile: str


@dataclass
class SifchainCmdOutput(SifchainCmdParameters):
    pass


def wait_for_port(host, port) -> bool:
    while True:
        try:
            with socket.create_connection((host, port)):
                return True
        except (ConnectionRefusedError, OSError) as e:
            time.sleep(1)
    return False


def atomic_write(s: str, filename: str):
    output = Path(filename)
    output.unlink(missing_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", dir=os.path.dirname(output)) as temp:
        temp.write(s)
        temp.flush()
        os.link(temp.name, output)


def default_cmdline_parser():
    return argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )


def sifchain_cmd_input_parser(parser = None) -> argparse.ArgumentParser:
    """Turn command line arguments into EthereumInput"""
    if parser is None:
        parser = default_cmdline_parser()
    parser.add_argument('--logfile', required=True)
    parser.add_argument('--pidfile', required=True)
    parser.add_argument('--configoutputfile', required=True)
    return parser
    # result = parser.parse_args()
    # print(f"tyeargs: {result}")
    # return result


def startup_complete(args, process_id):
    Path(args.pidfile).write_text(str(process_id))
    Path(args.configoutputfile).write_text(args.as_json())


def docker_compose_command(component: str)->str:
    return f"python3 src/py/env_framework.py {component}"
