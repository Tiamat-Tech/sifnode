import subprocess

import env_ethereum
import env_utilities
from env_utilities import wait_for_port


def geth_cmd(args: env_ethereum.EthereumInput) -> str:
    apis = "personal,eth,net,web3,debug"
    cmd = " ".join([
        "geth",
        "--datadir /tmp/gethdata",
        f"--networkid {args.network_id}",
        f"--ws --ws.addr 0.0.0.0 --ws.port {args.ws_port} --ws.api {apis}",
        f"--http --http.addr 0.0.0.0 --http.port {args.http_port} --http.api {apis}",
        "--dev --dev.period 1",
        "--mine --miner.threads=1",
        f"> {args.logfile}",
    ])
    return cmd


def fund_initial_accounts(args: env_ethereum.EthereumInput):
    quote = '"'
    for addr in args.ethereum_addresses:
        quotedaddr = f"\\{quote}{addr}\\{quote}"
        cmd = f'geth attach /tmp/gethdata/geth.ipc --exec "eth.sendTransaction({{from:eth.coinbase, to:{quotedaddr}, value:{args.starting_ethereum * 10 ** 18}}})"'
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for addr in args.ethereum_addresses:
        quotedaddr = f"\\{quote}{addr}\\{quote}"
        while True:
            cmd = f'geth attach /tmp/gethdata/geth.ipc --exec "eth.getBalance({quotedaddr})"'
            balance_result = subprocess.run(
                cmd,
                check=True,
                text=True, shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=10,
            )
            balance = int(float(balance_result.stdout))
            if balance >= args.starting_ethereum:
                break;


def geth_docker_compose(args: env_ethereum.EthereumInput):
    ports = [
        f"{args.ws_port}:{args.ws_port}",
        f"{args.http_port}:{args.http_port}",
    ]
    network = "sifchaintest"
    volumes = [
        "../..:/sifnode"
    ]
    image = "sifdocker:latest"
    return {
        "services": {
            "geth": {
                "image": image,
                "ports": ports,
                "networks": [network],
                "volumes": volumes,
                "working_dir": "/sifnode/test/integration",
                "command": "python3 src/py/env_start_geth.py go"
            }
        }
    }


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
    fund_initial_accounts(args)
    env_utilities.startup_complete(args, proc.pid)
    return proc
