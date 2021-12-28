namespace Neo.Plugins;
using Neo.SmartContract.Native;
using Neo.Wallets.NEP6;

public partial class plugin
{
    string get_address_by_nep6(string path)
    {
        NEP6Wallet wallet = new(path, system!.Settings);
        return wallet.GetDefaultAccount().Address;
    }
}