namespace Neo.Plugins;
using Neo.SmartContract.Native;

public partial class plugin
{
    string get_manifest_by_scripthash(string scripthash) => NativeContract.ContractManagement.GetContract(system!.StoreView, scripthash.UInt160ByScripthash()).Manifest.ToJson().ToString();
}