import argparse
import subprocess
import textwrap
from dataclasses import dataclass
from typing import List

from env_utilities import SifchainCmdInput, SifchainCmdOutput, wait_for_port


@dataclass
class GethInput(SifchainCmdInput):
    logfile: str
    chain_id: str
    network_id: str
    http_port: int
    ws_port: int
    ethereum_addresses: List[str]
    starting_ethereum: int = 100


@dataclass
class GethOutput(SifchainCmdOutput):
    """geth has no special output that we need to use"""
    pass


def geth_cmd(args: GethInput) -> str:
    apis = "personal,eth,net,web3,debug"
    cmd = " ".join([
        "nohup",
        "geth",
        f"--networkid {args.network_id}",
        f"--ws --ws.addr 0.0.0.0 --ws.port {args.ws_port} --ws.api {apis}",
        f"--http --http.addr 0.0.0.0 --http.port {args.http_port} --http.api {apis}",
        "--dev --dev.period 1",
        "--mine --miner.threads=1",
        f"> {args.logfile}",
    ])
    return cmd


def start_geth(args: GethInput) -> None:
    cmd = geth_cmd(args)
    logfile = open(args.logfile, "w")
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=logfile,
        stdin=None,
        stderr=subprocess.STDOUT,
    )
    wait_for_port("localhost", args.ws_port)
    wait_for_port("localhost", args.http_port)
    print("geth running")
    proc.wait()


def parse_geth_args() -> GethInput:
    """Turn command line arguments into GethInput"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""
    start geth
    """))
    parser.add_argument('--logfile', required=True)
    parser.add_argument('--chain_id', required=True)
    parser.add_argument('--network_id', required=True)
    parser.add_argument('--ws_port', required=True)
    parser.add_argument('--http_port', required=True)
    parser.add_argument('--ethereum_addresses', required=True)
    parser.add_argument('--starting_ethereum', type=int, default=100)
    result = parser.parse_args()
    print(f"tyeargs: {result}")
    return result


def parsed_args_to_geth_input(args: argparse.Namespace) -> GethInput:
    return GethInput(
        logfile=args.logfile,
        chain_id=args.chain_id,
        network_id=args.network_id,
        http_port=args.http_port,
        ws_port=args.ws_port,
        ethereum_addresses=args.ethereum_addresses,
    )


geth_input = parsed_args_to_geth_input(parse_geth_args())
print(f"gethtinput: {geth_input}")
assert False

geth_opts = GethInput(
    logfile="/tmp/gethlog.txt",
    chain_id=3,
    network_id=3,
    http_port=7545,
    ws_port=8646,
    ethereum_addresses=["a", "b"],
    starting_ethereum=100
)
start_geth(geth_opts)
