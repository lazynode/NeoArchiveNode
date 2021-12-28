from os.path import abspath
from os.path import expanduser
from pickle import load
from pickle import dump
from subprocess import Popen
from subprocess import DEVNULL
from subprocess import PIPE
from telnetlib import Telnet
from getpass import getpass
from json import loads


class KV:
    pass


class Nan:
    def __init__(self) -> None:
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
        with Telnet('localhost', 8517) as tn:
            tn.write(cmd.encode() if dec else cmd)
            tn.write(b'\n')
            for arg in args:
                tn.write(arg.encode() if dec else arg)
                tn.write(b'\n')
            tn.write(b'\n')
            ret = tn.read_until(b'\n')[:-1]
            return ret.decode() if enc else ret

    def AddWallet(self, filename: str, name: str = None) -> None:
        wif = self.GetWIFByNEP6(filename)
        name = name or self.GetAddressByNEP6(filename)
        setattr(self.__store.wif, name, wif)
        print('OK!')

    def AddContract(self, scripthash: str, name: str = None) -> None:
        name = name or self.GetManifestByScripthash(scripthash)['name']
        setattr(self.__store.contract, name, scripthash)
        print('OK!')

    def GetWIFByNEP6(self, filename: str) -> str:
        password = getpass()
        return self.__telnet(
            'get_wif_by_nep6',
            abspath(filename),
            password,
        )

    def GetAddressByNEP6(self, filename: str) -> str:
        return self.__telnet(
            'get_address_by_nep6',
            abspath(filename),
        )

    def GetManifestByScripthash(self, scripthash: str) -> dict:
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
