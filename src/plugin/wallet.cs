namespace Neo.Plugins;

using Neo.Wallets;
using Neo.SmartContract;
using System;
using Neo;
using System.Collections.Generic;

class wallet : Wallet
{
    public wallet(string path, ProtocolSettings settings) : base(path, settings) => throw new NotImplementedException();
    public override string Name => throw new NotImplementedException();
    public override Version Version => throw new NotImplementedException();
    public override bool ChangePassword(string oldPassword, string newPassword) => throw new NotImplementedException();
    public override bool Contains(UInt160 scriptHash) => throw new NotImplementedException();
    public override WalletAccount CreateAccount(byte[] privateKey) => throw new NotImplementedException();
    public override WalletAccount CreateAccount(Contract contract, KeyPair? key = null) => throw new NotImplementedException();
    public override WalletAccount CreateAccount(UInt160 scriptHash) => throw new NotImplementedException();
    public override void Delete() => throw new NotImplementedException();
    public override bool DeleteAccount(UInt160 scriptHash) => throw new NotImplementedException();
    public override WalletAccount GetAccount(UInt160 scriptHash) => throw new NotImplementedException();
    public override IEnumerable<WalletAccount> GetAccounts() => throw new NotImplementedException();
    public override bool VerifyPassword(string password) => throw new NotImplementedException();
}