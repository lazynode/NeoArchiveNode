namespace Neo.Plugins;
using Neo.VM;
using Neo.IO.Json;
using Neo.SmartContract;
using Neo.Network.P2P.Payloads;
using Neo.IO;

public partial class plugin
{
    string get_invocation(string script, string signer)
    {
        ApplicationEngine engine = ApplicationEngine.Run(script.HexToBytes(), system!.StoreView, signer.TransactionByWif(), null, system.Settings);
        Transaction transaction = signer.WalletByWif(system!.Settings).MakeTransaction(system!.StoreView, script.HexToBytes(), signer.UInt160ByWif(), new[] { signer.SignerByWif() });
        ContractParametersContext contractParametersContext = new ContractParametersContext(system!.StoreView, transaction, system.Settings.Network);
        signer.WalletByWif(system!.Settings).Sign(contractParametersContext);
        transaction.Witnesses = contractParametersContext.GetWitnesses();
        JObject json = new();
        json["state"] = engine.State;
        json["stack"] = new JArray(engine.ResultStack.Select(p => p.ToJson()));
        json["txjson"] = transaction.ToJson(system!.Settings);
        json["tx"] = transaction.ToArray().ToHexString();
        return json.ToString();
    }
}