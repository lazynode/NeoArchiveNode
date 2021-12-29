namespace Neo.Plugins;
using Neo.Wallets.NEP6;

public partial class plugin
{
    string get_wif_by_nep6(string path, string password) => path.NEP6Wallet(system!.Settings, password).GetDefaultAccount().GetKey().Export();
}