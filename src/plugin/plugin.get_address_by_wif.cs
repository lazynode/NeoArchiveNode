namespace Neo.Plugins;
using Neo.SmartContract;
using Neo.Wallets;

public partial class plugin
{
    string get_address_by_wif(string wif) => wif.UInt160ByWif().ToAddress(system!.Settings.AddressVersion);
}