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

    def __telnet(self, cmd: bytes, *args: bytes) -> bytes:
        from telnetlib import Telnet
        with Telnet('localhost', 8517) as tn:
            tn.write(cmd)
            tn.write(b'\n')
            for arg in args:
                tn.write(arg)
                tn.write(b'\n')
            tn.write(b'\n')
            return tn.read_until(b'\n')[:-1]

    def OpenWallet(self, filename: str):
        wif = self.GetWIFByNEP6(filename)
        address = self.GetAddressByNEP6(filename)
        setattr(self.__store.wif, address, wif)
        print('OK!')

    def GetWIFByNEP6(self, filename: str):
        from os.path import abspath
        from getpass import getpass
        password = getpass()
        wif = self.__telnet(
            b'get_wif_by_nep6',
            abspath(filename).encode(),
            password.encode()
        )
        return wif.decode()

    def GetAddressByNEP6(self, filename: str):
        from os.path import abspath
        address = self.__telnet(
            b'get_address_by_nep6',
            abspath(filename).encode(),
        )
        return address.decode()

    @ property
    def wif(self):
        return self.__store.wif

    @ property
    def exit(self) -> None:
        from pickle import dump
        from os.path import expanduser
        self.__process.terminate()
        self.__process.wait()
        with open(expanduser('~/.nan/store'), 'wb') as f:
            dump(self.__store, f)
        exit()

    @ property
    def blockindex(self) -> int:
        return int(self.__telnet(b'get_blockindex'))

    @ property
    def version(self) -> str:
        from . import VERSION
        return VERSION


nan = Nan()
