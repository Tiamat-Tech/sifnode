from env_geth import EthereumInput, start_geth

geth_opts = EthereumInput(
    logfile="/tmp/gethlog.txt",
    chain_id=3,
    network_id=3,
    http_port=7545,
    ws_port=8646,
    ethereum_addresses=["a", "b"],
    starting_ethereum=100
)
start_geth(geth_opts)
