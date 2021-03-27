from typing import List
import yaml
import subprocess
from dataclasses import dataclass

import env_ethereum
import env_utilities
from env_utilities import wait_for_port
import env_ethereum


@dataclass
class SmartContractDeployInput(env_utilities.SifchainCmdInput):
    ws_port: int
    truffle_network: str
    validator_addresses: List[str]


def smartcontractrunner_docker_compose(args: env_ethereum.EthereumInput):
    name = "smartcontractrunner"
    network = "sifchaintest"
    volumes = [
        "../..:/sifnode"
    ]
    image = "sifdocker:latest"
    return {
        name: {
            "image": image,
            "networks": [network],
            "volumes": volumes,
            "working_dir": "/sifnode/test/integration",
            "container_name": name,
            "command": env_utilities.docker_compose_command(name)
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
