namespace Neo.Plugins;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Reflection;
using System.Text;
using Neo;
using Neo.IO;
using Neo.Ledger;
using Neo.Network.P2P.Payloads;
using Neo.Persistence;

public partial class plugin : Plugin
{
    NeoSystem? system;
    IStore? store;
    TcpListener? listener;
    Thread? thread;
    public plugin()
    {
        Blockchain.Committing += OnPersist;
    }
    public override void Dispose()
    {
        Blockchain.Committing -= OnPersist;
        base.Dispose();
        listener?.Stop();
        thread?.Join();
        system?.EnsureStoped(system.LocalNode);
        store?.Dispose();
    }
    void ThreadWorker(TcpClient client)
    {
        try
        {
            NetworkStream stream = client.GetStream();
            StreamReader reader = new StreamReader(stream);
            string cmd = reader.ReadLine() ?? "";
            string[] args = ThreadReadArgs(reader);
            object? ret = GetType().InvokeMember(cmd.ToLower(), BindingFlags.InvokeMethod | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.DeclaredOnly, null, this, args);
            stream.Write(Encoding.UTF8.GetBytes(ret?.ToString()! + "\n"));
            stream.Flush();
        }
        catch (Exception e)
        {
            Console.Error.WriteLine(e);
        }
    }
    string[] ThreadReadArgs(StreamReader reader)
    {
        for (IEnumerable<string> result = Enumerable.Empty<string>(); ;)
        {
            string line = reader.ReadLine() ?? "";
            if (line.Length == 0) return result.ToArray();
            result = result.Append(line);
        }
    }

    void ThreadListener()
    {
        try
        {
            for (; ; )
            {
                ThreadWorker(listener!.AcceptTcpClient());
            }
        }
        catch
        {
        }
    }

    protected override void OnSystemLoaded(NeoSystem ns)
    {
        system = ns;
        store = system.LoadStore(String.Format("Data_Archive_{0}", system.Settings.Network.ToString("X")));
        listener = new TcpListener(IPAddress.Loopback, 8517);
        thread = new(ThreadListener);
        listener.Start();
        thread.Start();
    }
    public void OnCommit(NeoSystem system, Block block, DataCache snapshot)
    {
    }
    public void OnPersist(NeoSystem ns, Block block, DataCache snapshot, IReadOnlyList<Blockchain.ApplicationExecuted> ae) => snapshot.GetChangeSet().ToList().ForEach(v => store!.Put(CompositeKey(v.Key.ToArray(), block.Index), v.Item.ToArray().Append((byte)v.State).ToArray()));

    public byte[]? GetStorageAtHeight(byte[] key, uint height) => ExtractStorage(key, store!.Seek(CompositeKey(key, height), SeekDirection.Backward).FirstOrDefault());
    static byte[]? ExtractStorage(byte[] key, (byte[] Key, byte[] Value) kv) => kv.Key.SkipLast(4).SequenceEqual(key) ? kv.Value.Count() > 0 && kv.Value.TakeLast(1).Single() != ((byte)TrackState.Deleted) ? kv.Value.SkipLast(1).ToArray() : null : null;
    static byte[] CompositeKey(byte[] key, uint n) => key.Concat(UintToBytes(n)).ToArray();
    static IEnumerable<byte> UintToBytes(uint n) => BitConverter.IsLittleEndian ? BitConverter.GetBytes(n).Reverse() : BitConverter.GetBytes(n);

}