namespace Neo.Plugins;
using Neo.SmartContract.Native;

public partial class plugin
{
    string get_manifest_by_scripthash(string scripthash)
    {
        return ContractManagement.GetContract(UInt160.Parse(scripthash)).Manifest.ToJson().ToString();
    }
}