namespace Neo.Plugins;
using Neo.SmartContract;
using Neo.Wallets;

public partial class plugin
{
    string get_address_by_wif(string wif)
    {
        return Contract.CreateSignatureContract(new KeyPair(Wallet.GetPrivateKeyFromWIF(wif)).PublicKey).ScriptHash.ToAddress(system!.Settings.AddressVersion);
    }
}