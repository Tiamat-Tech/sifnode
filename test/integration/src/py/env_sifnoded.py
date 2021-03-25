from typing import List
import yaml
import subprocess
from dataclasses import dataclass

import env_ethereum
import env_utilities
from env_utilities import wait_for_port
import env_ethereum


@dataclass
class SifnodedRunner(env_utilities.SifchainCmdInput):
    ethereum_ws_port: int
    truffle_network: str
    validator_addresses: List[str]


def smartcontractrunner_docker_compose(args: env_ethereum.EthereumInput):
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
        "geth": {
            "image": image,
            "ports": ports,
            "networks": [network],
            "volumes": volumes,
            "working_dir": "/sifnode/test/integration",
            "container_name": "geth",
            "command": env_utilities.docker_compose_command("geth")
        }
    }


def deploy_contracts_cmd(args: SmartContractDeployInput):
    return f"cd {args.basedir}/smart-contracts && npx truffle deploy --network {args.truffle_network} --reset"


def deploy_contracts(args: SmartContractDeployInput):
    cmd = deploy_contracts_cmd(args)
    return subprocess.run(
        cmd,
        shell=True,
        stdout=args.logfile,
        stdin=None,
        stderr=subprocess.STDOUT,
    )
