namespace Neo.Plugins;

using Neo;
using Neo.Wallets;
using System;

class walletaccount : WalletAccount
{
    string WIF;
    public walletaccount(string wif, ProtocolSettings settings) : base(wif.UInt160ByWif(), settings)
    {
        WIF = wif;
        Contract = wif.ContractByWif();
    }
    public override bool HasKey => true;
    public override KeyPair GetKey() => WIF.KeyPairByWif();
}