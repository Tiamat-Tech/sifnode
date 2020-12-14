// Everything here represents services that are effectively remote data storage
export * from "./EthereumService/utils/getFakeTokens";
export * from "./EthereumService/utils/getMetamaskProvider";
export * from "./EthereumService/utils/loadAssets";

import ethereumService, { EthereumServiceContext } from "./EthereumService";
import tokenService, { TokenServiceContext } from "./TokenService";
import sifService, { SifServiceContext } from "./SifService";
import clpService, { ClpServiceContext } from "./ClpService";

export type Api = ReturnType<typeof createApi>;

export type WithApi<T extends keyof Api = keyof Api> = {
  api: Pick<Api, T>;
};

export type ApiContext = EthereumServiceContext &
  TokenServiceContext &
  SifServiceContext &
  ClpServiceContext &
  Omit<ClpServiceContext, "getPools">; // add contexts from other APIs

export function createApi(context: ApiContext) {
  const EthereumService = ethereumService(context);
  const TokenService = tokenService(context);
  const SifService = sifService(context);
  const ClpService = clpService(context);
  return {
    ClpService,
    EthereumService,
    TokenService,
    SifService,
  };
}
