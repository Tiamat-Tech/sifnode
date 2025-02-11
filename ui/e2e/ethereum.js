import Web3 from "web3";
const web3 = new Web3("http://localhost:7545");
import { advanceBlock } from "../core/src/test/utils/advanceBlock";

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function getEthBalance(address) {
  const ethBalance = await web3.eth.getBalance(address);
  const balance = web3.utils.fromWei(ethBalance);
  return balance;
}

export async function advanceEthBlocks() {
  await advanceBlock(50);
  await sleep(20000); // need to wait for events to cascade
}
