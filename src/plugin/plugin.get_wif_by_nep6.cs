namespace Neo.Plugins;
using Neo.SmartContract.Native;
using Neo.Wallets.NEP6;

public partial class plugin
{
    string get_wif_by_nep6(string path, string password)
    {
        NEP6Wallet wallet = new(path, system!.Settings);
        wallet.Unlock(password);
        return wallet.GetDefaultAccount().GetKey().Export();
    }
}