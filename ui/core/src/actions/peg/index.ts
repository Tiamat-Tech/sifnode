import { ActionContext } from "..";
import { Address, Asset, AssetAmount, TransactionStatus } from "../../entities";
import notify from "../../api/utils/Notifications";
import JSBI from "jsbi";
import { subscribeToUnconfirmedPegTxs } from "./subscribeToUnconfirmedPegTxs";
import { createSubscribeToTx } from "./utils/subscribeToTx";

function isOriginallySifchainNativeToken(asset: Asset) {
  return ["erowan", "rowan"].includes(asset.symbol);
}

// listen for 50 confirmations
// Eventually this should be set on ebrelayer
// to centralize the business logic
const ETH_CONFIRMATIONS = 50;

// TODO: Subscriptions, Commands and Queries should all be their own concepts and each exist within their
//       own files to manage complexity allow for team to grow and avoid refactoring
//       subtle complexity of dependency injection to maintain testability is required passing in ctx below

export default ({
  api,
  store,
}: ActionContext<
  "SifService" | "EthbridgeService" | "EthereumService",
  "wallet" | "tx"
>) => {
  // Create the context for passing to commands, queries and subscriptions
  const ctx = { api, store, ethConfirmations: ETH_CONFIRMATIONS };

  const actions = {
    // TODO: suggestion externalize all interactors injecting ctx would look like the following
    // getSifTokens: getSifTokens(ctx),
    // getEthTokens: getEthTokens(ctx),
    // calculateUnpegFee: calculateUnpegFee(ctx),
    // unpeg: unpeg(ctx),
    // peg: peg(ctx),

    subscribeToUnconfirmedPegTxs: subscribeToUnconfirmedPegTxs(ctx),

    getSifTokens() {
      return api.SifService.getSupportedTokens();
    },

    getEthTokens() {
      return api.EthereumService.getSupportedTokens();
    },

    calculateUnpegFee(asset: Asset) {
      const feeNumber = isOriginallySifchainNativeToken(asset)
        ? "54080000000000000"
        : "58560000000000000";

      return AssetAmount(Asset.get("ceth"), JSBI.BigInt(feeNumber), {
        inBaseUnit: true,
      });
    },

    async unpeg(assetAmount: AssetAmount) {
      const lockOrBurnFn = isOriginallySifchainNativeToken(assetAmount.asset)
        ? api.EthbridgeService.lockToEthereum
        : api.EthbridgeService.burnToEthereum;

      const feeAmount = this.calculateUnpegFee(assetAmount.asset);

      const tx = await lockOrBurnFn({
        assetAmount,
        ethereumRecipient: store.wallet.eth.address,
        fromAddress: store.wallet.sif.address,
        feeAmount,
      });

      console.log(
        "unpeg",
        tx,
        assetAmount,
        store.wallet.eth.address,
        store.wallet.sif.address,
        feeAmount
      );

      const txStatus = await api.SifService.signAndBroadcast(tx.value.msg);

      if (txStatus.state !== "accepted") {
        notify({
          type: "error",
          message: txStatus.memo || "There was an error while unpegging",
        });
      }
      console.log(
        "unpeg txStatus.state",
        txStatus.state,
        txStatus.memo,
        txStatus.code,
        tx.value.msg
      );

      return txStatus;
    },

    // TODO: Move this approval command to within peg and report status via store or some other means
    //       This has been done for convenience but we should not have to know in the view that
    //       approval is required before pegging as that is very much business domain knowledge
    async approve(address: Address, assetAmount: AssetAmount) {
      return await api.EthbridgeService.approveBridgeBankSpend(
        address,
        assetAmount
      );
    },

    async peg(assetAmount: AssetAmount) {
      const subscribeToTx = createSubscribeToTx(ctx);

      const lockOrBurnFn = isOriginallySifchainNativeToken(assetAmount.asset)
        ? api.EthbridgeService.burnToSifchain
        : api.EthbridgeService.lockToSifchain;

      return await new Promise<TransactionStatus>(done => {
        const pegTx = lockOrBurnFn(
          store.wallet.sif.address,
          assetAmount,
          ETH_CONFIRMATIONS
        );

        subscribeToTx(pegTx);

        pegTx.onTxHash(hash => {
          done({
            hash: hash.txHash,
            memo: "Transaction Accepted",
            state: "accepted",
          });
        });
      });
    },
  };

  return actions;
};
