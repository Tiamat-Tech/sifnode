import sys

import yaml

import env_ethereum
import env_geth
from env_geth import start_geth

# parsed_args = env_ethereum.ethereum_args_parser().parse_args()
# geth_input = env_ethereum.parsed_args_to_ethereum_input(parsed_args)

geth_input = env_ethereum.EthereumInput(
    logfile="/tmp/logfile.txt",
    chain_id=3,
    network_id=3,
    ws_port=8646,
    http_port=7445,
    ethereum_addresses="0x0d1d4e623d10f9fba5db95830f7d3839406c6af2,0x0f4f2ac550a1b4e2280d04c21cea7ebd822934b5,0x2191ef87e392377ec08e7c08eb105ef5448eced5,0x2932b7a2355d6fecc4b5c0b6bd44cc31df247a2e,0x5aeda56215b167893e80b4fe645ba6d5bab767de,0x627306090abab3a6e1400e9345bc60c78a8bef57,0x6330a553fc93768f612722bb8c2ec78ac90b3bbc,0x821aea9a577a9b44299b9c15c88cf3087f3b5544,0xc5fdf4076b8f3a5357c5e395ab970b5b54098fef,0xf17f52151ebef6c7334fad080c5704d77216b732".split(
        ","),
    starting_ether=123,
    pidfile="/tmp/pidfile.txt",
    configoutputfile="/tmp/myconfig.txt"
)

dockercompose = env_geth.geth_docker_compose(geth_input)
q = {
    "version": "3.9",
    "networks": {
        "sifchaintest": {
            "name": "sifchaintest"
        }
    }
}

if len(sys.argv) > 1 and sys.argv[1] == "go":
    print(f"starting geth, configuration is {geth_input}")
    start_geth(geth_input).wait()
else:
    print(yaml.dump({**dockercompose, **q}))
