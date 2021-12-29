namespace Neo.Plugins;

using Neo.Wallets;
using Neo.Wallets.NEP6;
using Neo.Cryptography.ECC;
using Neo.SmartContract;
using Neo.IO.Json;

static class helper
{
    public static NEP6Wallet NEP6WalletByFilename(this string filename, ProtocolSettings settings, string? password = null)
    {
        NEP6Wallet wallet = new(filename, settings);
        if (password is not null) wallet.Unlock(password);
        return wallet;
    }
    public static KeyPair KeyPairByWif(this string wif) => new KeyPair(Wallet.GetPrivateKeyFromWIF(wif));
    public static ECPoint ECPointByWif(this string wif) => wif.KeyPairByWif().PublicKey;
    public static UInt160 UInt160ByWif(this string wif) => Contract.CreateSignatureContract(wif.KeyPairByWif().PublicKey).ScriptHash;
    public static UInt160 UInt160ByScripthash(this string scripthash) => UInt160.Parse(scripthash);
    public static ContractParameter[] ContractParametersByArgs(this string args) => JObject.Parse(args).GetArray().Select(v => ContractParameter.FromJson(v)).ToArray();
}