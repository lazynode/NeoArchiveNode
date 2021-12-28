namespace Neo.Plugins;
using Neo.SmartContract.Native;

public partial class plugin
{
    string get_blockindex()
    {
        return NativeContract.Ledger.CurrentIndex(system!.StoreView).ToString();
    }
}