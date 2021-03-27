import os
from typing import List
import yaml
import subprocess
from dataclasses import dataclass

import env_ethereum
import env_utilities
from env_utilities import wait_for_port
import env_ethereum


smartcontractrunner_name = "smartcontractrunner"


@dataclass
class SmartContractDeployInput(env_utilities.SifchainCmdInput):
    network_id: int
    ws_addr: str
    truffle_network: str
    operator_private_key: str
    validator_addresses: List[str]


def smartcontractrunner_docker_compose(args: env_ethereum.EthereumInput):
    base = env_utilities.base_docker_compose(smartcontractrunner_name)
    network = "sifchaintest"
    return {
        smartcontractrunner_name: {
            **base,
            "networks": [network],
            "working_dir": "/sifnode/test/integration",
        }
    }


def deploy_contracts_cmd(args: SmartContractDeployInput):
    #     process.env.ETHEREUM_PRIVATE_KEY,
    # process.env.ETHEREUM_WEBSOCKET_ADDRESS
    os.environ["ETHEREUM_PRIVATE_KEY"] = args.operator_private_key
    os.environ["ETHEREUM_WEBSOCKET_ADDRESS"] = args.ws_addr
    os.environ["ETHEREUM_NETWORK_ID"] = str(args.network_id)
    return f"cd {args.basedir}/smart-contracts && npx truffle deploy --network {args.truffle_network} --reset"


def deploy_contracts(args: SmartContractDeployInput):
    cmd = deploy_contracts_cmd(args)
    print(f"cmdis: {cmd}")
    return subprocess.run(
        cmd,
        shell=True,
        stdout=None,
        stdin=None,
        stderr=subprocess.STDOUT,
    )
