namespace Neo.Plugins;
using Neo.Wallets.NEP6;

public partial class plugin
{
    string get_address_by_nep6(string path) => path.NEP6WalletByFilename(system!.Settings).GetDefaultAccount().Address;
}