import yaml
import subprocess
from dataclasses import dataclass

import env_ethereum
import env_utilities
from env_utilities import wait_for_port


@dataclass
class GanacheInput(env_ethereum.EthereumInput):
    ganache_keys_json: str
    block_delay: int
    mnemonic: str
    port: int
    db_dir: str


def ganache_cmd(args: GanacheInput) -> str:
    # --db ${GANACHE_DB_DIR} --account_keys_path $GANACHE_KEYS_JSON > $GANACHE_LOG 2>&1"
    block_delay = f"-b {args.block_delay}" if args.block_delay and args.block_delay > 0 else ""
    mnemonic = args.mnemonic if args.mnemonic else "candy maple cake sugar pudding cream honey rich smooth crumble sweet treat"
    cmd = " ".join([
        "ganache-cli",
        block_delay,
        "-h 0.0.0.0",
        f'-d --mnemonic "{mnemonic}"',
        f"--networkId {args.network_id}",
        f"--port {args.port}",
        f"--account_keys_path {args.ganache_keys_json}",
        f"--db {args.db_dir}",
        f"-e {args.starting_ether}"
        f"> {args.logfile}",
    ])
    return cmd


def ganache_docker_compose(args: GanacheInput):
    ports = [
        f"{args.port}:{args.port}",
    ]
    network = "sifchaintest"
    volumes = [
        "../..:/sifnode"
    ]
    image = "sifdocker:latest"
    return {
        "ganache": {
            "image": image,
            "ports": ports,
            "networks": [network],
            "volumes": volumes,
            "working_dir": "/sifnode/test/integration",
            "container_name": "ganache",
            "command": env_utilities.docker_compose_command("ganache")
        }
    }


def start_ganache(args: GanacheInput):
    """returns an object with a wait() method"""
    cmd = ganache_cmd(args)
    print(f"start ganache with {yaml.dump(args)}")
    logfile = open(args.logfile, "w")
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=logfile,
        stdin=None,
        stderr=subprocess.STDOUT,
    )
    wait_for_port("localhost", args.port)
    env_utilities.startup_complete(args, proc.pid)
    return proc
