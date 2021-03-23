import sys

import yaml

import env_ethereum
import env_geth
from env_geth import start_geth

# parsed_args
if len(sys.argv) > 1 and sys.argv[1] == "go":
    print(f"starting geth, configuration is {geth_input}")
    start_geth(geth_input).wait()
else:
    print(yaml.dump({**dockercompose, **q}))
