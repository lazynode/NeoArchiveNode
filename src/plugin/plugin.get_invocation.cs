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
        var signerObjs = JObject.Parse(signers).GetArray().Select(v => Contract.CreateSignatureContract(new KeyPair(Wallet.GetPrivateKeyFromWIF(v.AsString())).PublicKey).ScriptHash).ToArray();
        Transaction? tx = signerObjs.Length == 0 ? null : new Transaction
        {
            Signers = signerObjs.Select(v => new Signer { Account = v }).ToArray(),
            Attributes = System.Array.Empty<TransactionAttribute>(),
            Witnesses = null,
        };
        using ApplicationEngine engine = ApplicationEngine.Run(script.HexToBytes(), system!.StoreView, container: tx, settings: system.Settings, gas: 20_00000000);
        JObject json = new();
        json["script"] = script;
        json["state"] = engine.State;
        json["gasconsumed"] = engine.GasConsumed.ToString();
        json["signers"] = JObject.Parse(signers).GetArray();
        try
        {
            json["stack"] = new JArray(engine.ResultStack.Select(p => p.ToJson()));
        }
        catch (InvalidOperationException)
        {
            json["stack"] = "error: invalid operation";
        }
        return json.ToString();
    }

}