namespace Neo.Plugins;
using Neo.VM;
using Neo.IO.Json;
using Neo.SmartContract;

public partial class plugin
{
    string get_script(string scripthash, string method, string args)
    {
        return UInt160.Parse(scripthash).MakeScript(method, JObject.Parse(args).GetArray().Select(v => ContractParameter.FromJson(v)).ToArray()).ToHexString();
    }
}