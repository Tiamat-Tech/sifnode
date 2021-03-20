import argparse
import textwrap
from dataclasses import dataclass
from typing import List

from env_utilities import SifchainCmdInput, SifchainCmdOutput


@dataclass
class EthereumInput(SifchainCmdInput):
    logfile: str
    chain_id: str
    network_id: str
    http_port: int
    ws_port: int
    ethereum_addresses: List[str]
    starting_ethereum: int = 100


@dataclass
class EthereumOutput(SifchainCmdOutput):
    """geth has no special output that we need to use"""
    pass


def ethereum_args_parser(parser) -> argparse.ArgumentParser:
    """Turn command line arguments into EthereumInput"""
    if parser is None:
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=textwrap.dedent(
                """
                start geth
                * add tokens to users in ethereum_addresses
                * don't return until geth is listening to ws and http ports
                """
            ))
    parser.add_argument('--logfile', required=True)
    parser.add_argument('--pidfile', required=True)
    parser.add_argument('--chain_id', required=True)
    parser.add_argument('--network_id', required=True)
    parser.add_argument('--ws_port', required=True)
    parser.add_argument('--http_port', required=True)
    parser.add_argument('--ethereum_addresses', required=True)
    parser.add_argument('--starting_ethereum', type=int, default=100)
    return parser
    # result = parser.parse_args()
    # print(f"tyeargs: {result}")
    # return result


def parsed_args_to_ethereum_input(args: argparse.Namespace) -> EthereumInput:
    return EthereumInput(
        logfile=args.logfile,
        chain_id=args.chain_id,
        network_id=args.network_id,
        http_port=args.http_port,
        ws_port=args.ws_port,
        ethereum_addresses=args.ethereum_addresses.split(','),
        pidfile=args.pidfile,
    )
