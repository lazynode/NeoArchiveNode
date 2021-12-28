namespace Neo.Plugins;
using Neo.Wallets.NEP6;

public partial class plugin
{
    string get_manifest_by_scripthash(string scripthash)
    {
        var contract = Neo.SmartContract.Native.ContractManagement.GetContract(UInt160.Parse(scripthash));
        return contract.Manifest.ToJson().ToString();
    }
}