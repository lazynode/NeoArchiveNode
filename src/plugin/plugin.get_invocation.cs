namespace Neo.Plugins;
using Neo.VM;
using Neo.IO.Json;
using Neo.SmartContract;
using Neo.Network.P2P.Payloads;
using Neo.Wallets;

public partial class plugin
{
    string get_invocation(string script, string signers)
    {
        JArray signer = JObject.Parse(signers).GetArray();
        UInt160[] ss = signer.Select(v => Contract.CreateSignatureContract(new KeyPair(Wallet.GetPrivateKeyFromWIF(v.AsString())).PublicKey).ScriptHash).ToArray();
        Transaction? tx = ss.Length == 0 ? null : new Transaction
        {
            Signers = ss.Select(v => new Signer { Account = v }).ToArray(),
            Attributes = System.Array.Empty<TransactionAttribute>(),
            Witnesses = null,
        };
        using ApplicationEngine engine = ApplicationEngine.Run(script.HexToBytes(), system!.StoreView, tx);
        JObject json = new();
        json["script"] = script;
        json["state"] = engine.State;
        json["gasconsumed"] = engine.GasConsumed.ToString();
        json["signers"] = JObject.Parse(signers).GetArray();
        json["stack"] = new JArray(engine.ResultStack.Select(p => p.ToJson()));
        return json.ToString();
    }

}