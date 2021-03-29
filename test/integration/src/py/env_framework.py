import dataclasses
import os
import sys
import time

import yaml

import env_ganache
import env_geth
import env_smartcontractrunner
import env_utilities
from env_geth import start_geth

configbase = "/configs"
logbase = "/logs/"

ganachename = "ganache"
gethname = "geth"
basedir = "/sifnode"


def config_file_full_path(name: str):
    return os.path.join(configbase, f"{name}.json")


def log_file_full_path(name: str):
    return os.path.join(logbase, f"{name}.log")


geth_input = env_geth.GethInput(
    basedir=basedir,
    logfile=log_file_full_path(gethname),
    chain_id=3,
    network_id=3,
    starting_ether=123,
    ws_port=8646,
    http_port=7445,
    ethereum_addresses=4,
    configoutputfile=config_file_full_path(gethname)
)

ganache_ws_port = 7545
ganache_ws_addr = f"ws://ganache:{ganache_ws_port}"
ganache_network_id = 5777

ganache_input = env_ganache.GanacheInput(
    basedir=basedir,
    logfile=log_file_full_path(ganachename),
    network_id=ganache_network_id,
    chain_id=3,
    starting_ether=123,
    port=7545,
    block_delay=None,
    mnemonic=None,
    db_dir="/tmp/ganachedb",
    configoutputfile=config_file_full_path(ganachename),
)

smartcontractrunner_input = env_smartcontractrunner.SmartContractDeployInput(
    basedir=basedir,
    network_id=ganache_network_id,
    logfile=log_file_full_path(env_smartcontractrunner.smartcontractrunner_name + "deploy"),
    configoutputfile=None,
    ws_addr=ganache_ws_addr,
    truffle_network="dynamic",
    operator_private_key=None,
    validator_addresses=["a", "b"],
)

geth_docker = env_geth.geth_docker_compose(geth_input)
ganache_docker = env_ganache.ganache_docker_compose(ganache_input)
smartcontractrunner_docker = env_smartcontractrunner.smartcontractrunner_docker_compose(ganache_input)

shared_docker = {
    "version": "3.9",
    "networks": {
        "sifchaintest": {
            "name": "sifchaintest"
        }
    }
}

component = sys.argv[1] if len(sys.argv) > 1 else "dockerconfig"

if component == "dockerconfig":
    print(yaml.dump({
        **shared_docker,
        "services": {
            **ganache_docker,
            **geth_docker,
            **smartcontractrunner_docker,
        }
    }))
elif component == "geth":
    print(f"starting geth, configuration is {geth_input}")
    start_geth(geth_input).wait()
elif component == "ganache":
    print(f"starting ganache, configuration is {yaml.dump(ganache_input)}")
    env_ganache.start_ganache(ganache_input).wait()
elif component == "smartcontractrunner":
    time.sleep(100000000)
elif component == "deploy_contracts":
    ethereum_config = env_utilities.read_json_file(f"{configbase}/ethereum.json")
    for k in ethereum_config["config"]["private_keys"].keys():
        i = dataclasses.replace(smartcontractrunner_input, operator_private_key=k)
        env_smartcontractrunner.deploy_contracts(smartcontractrunner_input)
        break
elif component == "deploy_contracts":
    ethereum_config = env_utilities.read_json_file(f"{configbase}/ethereum.json")
    for k in ethereum_config["config"]["private_keys"].keys():
        i = dataclasses.replace(smartcontractrunner_input, operator_private_key=k)
        env_smartcontractrunner.deploy_contracts(smartcontractrunner_input)
        break
