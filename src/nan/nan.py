class KV:
    pass


class Nan:
    def __init__(self) -> None:
        from subprocess import Popen
        from subprocess import DEVNULL
        from subprocess import PIPE
        from os.path import expanduser
        from pickle import load
        self.__process = Popen(
            ['./neo-cli'],
            cwd=expanduser("~/.nan/neo-cli"),
            stdin=PIPE,
            stdout=DEVNULL,
            stderr=DEVNULL,
        )
        try:
            with open(expanduser('~/.nan/store'), 'rb') as f:
                self.__store = load(f)
        except:
            self.__store = KV()
            self.__store.wif = KV()
            self.__store.contract = KV()

    def __telnet(self, cmd: bytes | str, *args: bytes | str, dec: bool = True, enc: bool = True):
        from telnetlib import Telnet
        with Telnet('localhost', 8517) as tn:
            tn.write(cmd.encode() if dec else cmd)
            tn.write(b'\n')
            for arg in args:
                tn.write(arg.encode() if dec else arg)
                tn.write(b'\n')
            tn.write(b'\n')
            ret = tn.read_until(b'\n')[:-1]
            return ret.decode() if enc else ret

    def AddWallet(self, filename: str) -> None:
        wif = self.GetWIFByNEP6(filename)
        address = self.GetAddressByNEP6(filename)
        setattr(self.__store.wif, address, wif)
        print('OK!')

    def AddContract(self, scripthash: str, name: str) -> None:
        manifest = self.GetManifestByScripthash(scripthash)
        setattr(self.__store.contract, manifest['name'], KV())
        pass

    def GetWIFByNEP6(self, filename: str) -> str:
        from os.path import abspath
        from getpass import getpass
        password = getpass()
        return self.__telnet(
            'get_wif_by_nep6',
            abspath(filename),
            password,
        )

    def GetAddressByNEP6(self, filename: str) -> str:
        from os.path import abspath
        return self.__telnet(
            'get_address_by_nep6',
            abspath(filename),
        )

    def GetManifestByScripthash(self, scripthash: str) -> dict:
        from json import loads
        val = self.__telnet(
            'get_manifest_by_scripthash',
            scripthash,
        )
        return loads(val)

    @ property
    def wif(self) -> KV:
        return self.__store.wif

    @ property
    def exit(self) -> None:
        from pickle import dump
        from os.path import expanduser
        self.__process.terminate()
        self.__process.wait()
        with open(expanduser('~/.nan/store'), 'wb', 0o400) as f:
            dump(self.__store, f)
        exit()

    @ property
    def blockindex(self) -> int:
        return int(self.__telnet('get_blockindex'))

    @ property
    def version(self) -> str:
        from . import VERSION
        return VERSION


nan = Nan()
