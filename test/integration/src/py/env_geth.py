import json
import subprocess

import env_ethereum
import env_utilities
from env_utilities import wait_for_port
from pathlib import Path


def geth_cmd(args: env_ethereum.EthereumInput) -> str:
    apis = "personal,eth,net,web3,debug"
    cmd = " ".join([
        "geth",
        f"--networkid {args.network_id}",
        f"--ws --ws.addr 0.0.0.0 --ws.port {args.ws_port} --ws.api {apis}",
        f"--http --http.addr 0.0.0.0 --http.port {args.http_port} --http.api {apis}",
        "--dev --dev.period 1",
        "--mine --miner.threads=1",
        f"> {args.logfile}",
    ])
    return cmd


def start_geth(args: env_ethereum.EthereumInput):
    """returns an object with a wait() method"""
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
    Path(args.pidfile).write_text(str(proc.pid))
    return proc


env_utilities.atomic_write("fnord", "/tmp/fnord")
parsed_args = env_ethereum.ethereum_args_parser(env_utilities.default_cmdline_parser()).parse_args()
geth_input = env_ethereum.parsed_args_to_ethereum_input(parsed_args)
start_geth(geth_input)
print(geth_input.as_json())