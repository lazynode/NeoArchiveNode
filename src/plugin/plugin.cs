namespace Neo.Plugins;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using Neo;
using Neo.IO;
using Neo.Ledger;
using Neo.Network.P2P.Payloads;
using Neo.Persistence;

public class plugin : Plugin, IPersistencePlugin
{
    NeoSystem system;
    IStore store;
    public override void Dispose()
    {
        base.Dispose();
        system?.EnsureStoped(system.LocalNode);
        store?.Dispose();
    }
    protected override void OnSystemLoaded(NeoSystem ns)
    {
        system = ns;
        store = system.LoadStore(String.Format("Data_Archive_{0}", system.Settings.Network.ToString("X")));
    }
    public void OnPersist(NeoSystem ns, Block block, DataCache snapshot, IReadOnlyList<Blockchain.ApplicationExecuted> ae)
    {
    }
    public void OnCommit(NeoSystem system, Block block, DataCache snapshot)
    {
    }
}