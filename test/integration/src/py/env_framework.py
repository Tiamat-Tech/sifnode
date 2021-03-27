import os
import sys
import time

import yaml

import env_ganache
import env_geth
import env_smartcontractrunner
from env_geth import start_geth

configbase = "/tmp/configs"
logbase = "/tmp/logs/"

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
    ethereum_addresses="0x0d1d4e623d10f9fba5db95830f7d3839406c6af2,0x0f4f2ac550a1b4e2280d04c21cea7ebd822934b5,0x2191ef87e392377ec08e7c08eb105ef5448eced5,0x2932b7a2355d6fecc4b5c0b6bd44cc31df247a2e,0x5aeda56215b167893e80b4fe645ba6d5bab767de,0x627306090abab3a6e1400e9345bc60c78a8bef57,0x6330a553fc93768f612722bb8c2ec78ac90b3bbc,0x821aea9a577a9b44299b9c15c88cf3087f3b5544,0xc5fdf4076b8f3a5357c5e395ab970b5b54098fef,0xf17f52151ebef6c7334fad080c5704d77216b732".split(
        ","
    ),
    configoutputfile=config_file_full_path(gethname)
)

ganache_input = env_ganache.GanacheInput(
    basedir=basedir,
    logfile=log_file_full_path(ganachename),
    network_id=3,
    chain_id=3,
    starting_ether=123,
    port=7545,
    block_delay=None,
    mnemonic=None,
    db_dir="/tmp/ganachedb",
    configoutputfile=config_file_full_path(ganachename),
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
