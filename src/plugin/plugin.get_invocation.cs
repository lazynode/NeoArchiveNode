namespace Neo.Plugins;
using Neo.VM;
using Neo.IO.Json;
using Neo.SmartContract;
using Neo.Network.P2P.Payloads;
using Neo.Wallets;

public partial class plugin
{
    string get_invocation(string script, string signer)
    {
        using ApplicationEngine engine = ApplicationEngine.Run(script.HexToBytes(), system!.StoreView, signer.TransactionByWif(), null, system.Settings);
        JObject json = new();
        json["script"] = script;
        json["state"] = engine.State;
        json["gasconsumed"] = engine.GasConsumed.ToString();
        // json["signers"] = new JArray(new string[] { signer });
        json["stack"] = new JArray(engine.ResultStack.Select(p => p.ToJson()));
        return json.ToString();
    }

}