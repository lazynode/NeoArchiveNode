namespace Neo.Plugins;
using Neo.VM;
using Neo.IO.Json;
using Neo.SmartContract;

public partial class plugin
{
    string get_script(string scripthash, string method, string args) => scripthash.UInt160ByScripthash().MakeScript(method, args.ContractParametersByArgs()).ToHexString();
}