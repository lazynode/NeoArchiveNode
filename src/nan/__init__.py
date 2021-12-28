from json import loads
from getpass import getpass
from telnetlib import Telnet
from subprocess import PIPE
from subprocess import DEVNULL
from subprocess import Popen
from pickle import dump
from pickle import load
from os.path import expanduser
from os.path import abspath

VERSION = '0.0.35'


def telnet(cmd: str, *args: str) -> str:
    with Telnet('localhost', 8517) as tn:
        tn.write(cmd.encode())
        tn.write(b'\n')
        for arg in args:
            tn.write(arg.encode())
            tn.write(b'\n')
        tn.write(b'\n')
        ret = tn.read_until(b'\n')[:-1]
        return ret.decode()


class Wif(str):
    pass


class Contract(str):
    pass


class Nan:
    pass


class Command:
    def __init__(self) -> None:
        self.__process = Popen(
            ['./neo-cli'],
            cwd=expanduser("~/.nan/neo-cli"),
            stdin=PIPE,
            stdout=DEVNULL,
            stderr=DEVNULL,
        )

    def AddWif(self, filename: str, name: str = None) -> None:
        wif = self.GetWifByNEP6(filename)
        address = self.GetAddressByNEP6(filename)
        name = name or address
        setattr(nan, name, Wif(wif))
        print(name, 'ADDED')

    def AddContract(self, scripthash: str, name: str = None) -> None:
        name = name or self.GetManifestByScripthash(scripthash)['name']
        setattr(nan, name, Contract(scripthash))
        print(name, 'ADDED')

    def GetWifByNEP6(self, filename: str) -> str:
        password = getpass()
        return telnet('get_wif_by_nep6', abspath(filename), password)

    def GetAddressByNEP6(self, filename: str) -> str:
        return telnet('get_address_by_nep6', abspath(filename))

    def GetManifestByScripthash(self, scripthash: str) -> dict:
        val = telnet('get_manifest_by_scripthash', scripthash)
        return loads(val)

    @property
    def exit(self):
        self.__process.terminate()
        self.__process.wait()
        with open(expanduser('~/.nan/store'), 'wb', 0o400) as f:
            dump(nan, f)
        exit()

    @property
    def blockindex(self) -> int:
        return int(telnet('get_blockindex'))

    @property
    def version(self) -> str:
        return VERSION


nan = Nan()
cmd = Command()

try:
    with open(expanduser('~/.nan/store'), 'rb') as f:
        nan = load(f)
except:
    nan = Nan()
