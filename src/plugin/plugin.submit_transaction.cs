namespace Neo.Plugins;

using Neo.Network.P2P.Payloads;
using Neo.IO;
using Akka.Actor;

public partial class plugin
{
    string submit_transaction(string tx)
    {
        system!.Blockchain.Tell(tx.TransactionByTx());
        return "OK";
    }
}