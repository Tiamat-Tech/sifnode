import { SifUnSignedClient } from "./SifClient";

test("SifUnSignedClient can be constructed", async () => {
  const client = new SifUnSignedClient("http://localhost:1317");
  expect(client).not.toBeNull();
});
