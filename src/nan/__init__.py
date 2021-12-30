import base64
from json import loads
from json import dumps
from getpass import getpass
import json
from telnetlib import Telnet
from subprocess import PIPE
from subprocess import DEVNULL
from subprocess import Popen
from pickle import load
from os.path import expanduser
from os.path import abspath
from base64 import b64decode

VERSION = '0.1'


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
    def __repr__(self) -> str:
        return 'PRIVATE KEY OF <{}>'.format(cmd.GetAddressByWif(self))

    def __str__(self) -> str:
        return super().__str__()


class NEOVM:
    class Any:
        def __init__(self, val) -> None:
            if val is None:
                self.VAL = None
            elif isinstance(val, NEOVM.Any):
                self.VAL = val.VAL
            elif isinstance(val, bool):
                self.VAL = NEOVM.Boolean(val)
            elif isinstance(val, NEOVM.Boolean):
                self.VAL = val
            elif isinstance(val, int):
                self.VAL = NEOVM.Integer(val)
            elif isinstance(val, NEOVM.Integer):
                self.VAL = val
            elif isinstance(val, bytes):
                self.VAL = NEOVM.ByteArray(val)
            elif isinstance(val, NEOVM.ByteArray):
                self.VAL = val
            elif isinstance(val, str):
                self.VAL = NEOVM.String(val)
            elif isinstance(val, NEOVM.String):
                self.VAL = val
            elif isinstance(val, NEOVM.Hash160):
                self.VAL = val
            elif isinstance(val, NEOVM.Hash256):
                self.VAL = val
            elif isinstance(val, NEOVM.PublicKey):
                self.VAL = val
            elif isinstance(val, NEOVM.Signature):
                self.VAL = val
            elif isinstance(val, list):
                self.VAL = NEOVM.Array(val)
            elif isinstance(val, NEOVM.Array):
                self.VAL = val
            elif isinstance(val, dict):
                self.VAL = NEOVM.Map(val)
            elif isinstance(val, NEOVM.Map):
                self.VAL = val
            elif isinstance(val, NEOVM.InteropInterface):
                self.VAL = val
            raise Exception()

        def __str__(self) -> str:
            if self.VAL is None:
                return dumps({'type': 'Any', 'value': None})
            return str(self.VAL)

    class Boolean:
        def __init__(self, val) -> None:
            if isinstance(val, NEOVM.Boolean):
                self.VAL = val.VAL
            elif isinstance(val, bool):
                self.VAL = val
            elif isinstance(val, str):
                self.VAL = val.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
            else:
                raise Exception()

        def __str__(self) -> str:
            return str(self.VAL)

    class Integer:
        def __init__(self, val) -> None:
            if isinstance(val, NEOVM.Integer):
                self.VAL = val.VAL
            elif isinstance(val, int):
                self.VAL = val
            elif isinstance(val, float):
                self.VAL = int(val)
            elif isinstance(val, str):
                self.VAL = int(val)
            raise Exception()

        def __repr__(self) -> str:
            return repr(self.VAL)

        def __str__(self) -> str:
            return dumps({'type': 'Integer', 'value': self.VAL})

    class ByteArray:
        def __init__(self, val) -> None:
            if isinstance(val, NEOVM.ByteArray):
                self.VAL = val.VAL
            elif isinstance(val, bytes):
                self.VAL = val
            else:
                raise Exception()

        def __str__(self) -> str:
            return dumps({'type': 'ByteArray', 'value': base64.b64encode(self.VAL)})

    class String:
        def __init__(self, val) -> None:
            if isinstance(val, NEOVM.String):
                self.VAL = val.VAL
            elif isinstance(val, str):
                self.VAL = val
            else:
                raise Exception()

        def __str__(self) -> str:
            return dumps({'type': 'String', 'value': self.VAL})

    class Hash160:
        def __init__(self, val) -> None:
            if isinstance(val, NEOVM.Hash160):
                self.VAL = val.VAL
            elif isinstance(val, str) and len(val) == 42 and val.startswith('0x'):
                self.VAL = val
            elif isinstance(val, bytes) and len(val) == 42 and val.startswith(b'0x'):
                self.VAL = val.decode()
            else:
                raise Exception()

        def __repr__(self) -> str:
            return repr(self.VAL)

        def __str__(self) -> str:
            return dumps({'type': 'Hash160', 'value': self.VAL})

    class Hash256:
        def __init__(self, val) -> None:
            if isinstance(val, NEOVM.Hash256):
                self.VAL = val.VAL
            elif isinstance(val, str) and len(val) == 66 and val.startswith('0x'):
                self.VAL = val
            elif isinstance(val, bytes) and len(val) == 66 and val.startswith(b'0x'):
                self.VAL = val.decode()
            else:
                raise Exception()

        def __repr__(self) -> str:
            return repr(self.VAL)

        def __str__(self) -> str:
            return dumps({'type': 'Hash256', 'value': self.VAL})

    class PublicKey:
        def __init__(self, val) -> None:
            if isinstance(val, NEOVM.PublicKey):
                self.VAL = val.VAL
            elif isinstance(val, str) and len(val) == 66:
                self.VAL = val
            else:
                raise Exception()

        def __str__(self) -> str:
            return dumps({'type': 'PublicKey', 'value': self.VAL})

    class Signature:
        def __init__(self, val) -> None:
            if isinstance(val, NEOVM.Signature):
                self.VAL = val.VAL
            elif isinstance(val, bytes):
                self.VAL = val
            else:
                raise Exception()

        def __str__(self) -> str:
            return dumps({'type': 'Signature', 'value': base64.b64encode(self.VAL)})

    class Array:
        def __init__(self, val) -> None:
            if isinstance(val, NEOVM.Array):
                self.VAL = val.VAL
            elif isinstance(val, list):
                self.VAL = val
            else:
                raise Exception()

        def __str__(self) -> str:
            return dumps({'type': 'Array', 'value': str(self.VAL)})

    class Map:
        def __init__(self, val) -> None:
            if isinstance(val, NEOVM.Map):
                self.VAL = val.VAL
            elif isinstance(val, dict):
                self.VAL = val
            else:
                raise Exception()

        def __str__(self) -> str:
            return dumps({'type': 'Map', 'value': str([{'key':k, 'value':v} for k, v in self.VAL.items() ])})

    class InteropInterface:
        pass

    class Void:
        def __init__(self, *args, **kwarg) -> None:
            pass


class Transaction:
    def __init__(self, val) -> None:
        self.STATE = val['state']
        stacktype = [getattr(NEOVM, v['type']) for v in val['stack']]
        stackval = [v['value'] for v in val['stack']]
        for v in stacktype:
            assert type(v) == type
        self.STACK = [t(v) for t, v in zip(stacktype, stackval)]
        self.TXJSON = val['txjson']
        self.TX = bytes.fromhex(val['tx'])

    def __repr__(self) -> str:
        return repr(self.STACK) if self.STATE == 'HALT' else repr((self.STATE, self.STACK))

    @property
    def send(self) -> None:
        if input('''SCRIPT: {}\nVMHALT: {}\nSYSFEE: {}\nNETFEE: {}\nSIGNER: {}\ncontinue? [Y/n]'''.format(
            b64decode(self.TXJSON['script']).hex(),
            self.STATE == 'HALT',
            int(self.TXJSON['sysfee'])/1e8,
            int(self.TXJSON['netfee'])/1e8,
            self.TXJSON['signers'],
        )).lower() == 'y':
            cmd.SubmitTransaction(self.TX)
            return self.TXJSON['hash']


class Method:
    def __init__(self, scripthash, abi) -> None:
        self.SCRIPTHASH = scripthash
        self.NAME = abi['name']
        self.RETURN = getattr(NEOVM, abi['returntype'])
        assert type(self.RETURN) == type
        self.ARGS = [getattr(NEOVM, arg['type']) for arg in abi['parameters']]
        for arg in self.ARGS:
            assert type(arg) == type
        self.ARGNAMES = [arg['name'] for arg in abi['parameters']]

    @property
    def SPEC(self):
        return [(n, t.__name__)for n, t in zip(self.ARGNAMES, self.ARGS)], self.RETURN.__name__

    def __call__(self, *args, signer=None) -> Transaction:
        assert len(self.ARGS) == len(args)
        args = [t(v) for t, v in zip(self.ARGS, args)]
        script = cmd.GetScript(self.SCRIPTHASH, self.NAME, *args)
        ret = cmd.GetInvocationBySigner(script, signer or nan._)
        return Transaction(ret)


class Contract:
    def __init__(self, scripthash: str, manifest: dict) -> None:
        self.SCRIPTHASH = scripthash
        self.MANIFEST = manifest
        self.NAME = manifest['name']
        self.STANDARDS = manifest['supportedstandards']
        for method in manifest['abi']['methods']:
            setattr(self, method['name'], Method(scripthash, method))


class NEP17(Contract):
    pass


class Nan:
    def __init__(self) -> None:
        self._ = None
        # self.NEO = NEP17('0xef4073a0f2b305a38ec4050e4d3d28bc40ea63f5')
        # self.GAS = NEP17('0xd2a4cff31913016155e38e474a2c06d08be276cf')
        # self.bNEO = NEP17('0x48c40d4666f93408be1bef038b6722404d9a4c2a')


class Command:
    def __init__(self) -> None:
        pass

    def AddWifByNep6(self, filename: str, name: str = None) -> None:
        wif = self.GetWifByNEP6(filename)
        address = self.GetAddressByNEP6(filename)
        name = name or address
        setattr(nan, name, Wif(wif))
        print(name, 'ADDED')

    def AddContract(self, scripthash: str, name: str = None) -> None:
        manifest = self.GetManifestByScripthash(scripthash)
        name = name or manifest['name']
        setattr(nan, name, Contract(scripthash, manifest))
        print(name, 'ADDED')

    def SubmitTransaction(self, tx: bytes):
        telnet("submit_transaction", tx.hex())
        print('TX SENT')

    def GetWifByNEP6(self, filename: str) -> str:
        password = getpass()
        return telnet('get_wif_by_nep6', abspath(filename), password)

    def GetAddressByNEP6(self, filename: str) -> str:
        return telnet('get_address_by_nep6', abspath(filename))

    def GetManifestByScripthash(self, scripthash: str) -> dict:
        val = telnet('get_manifest_by_scripthash', scripthash)
        return loads(val)

    def GetScript(self, scripthash: str, method: str, *args):
        args = [str(v) for v in args]
        args = '['+','.join(args)+']'
        ret = telnet('get_script', scripthash, method, args)
        return bytes.fromhex(ret)

    def GetInvocationBySigner(self, scipt: bytes, signer: str):
        ret = telnet('get_invocation', scipt.hex(), str(signer))
        return loads(ret)

    def GetAddressByWif(self, wif: str) -> str:
        return telnet('get_address_by_wif', wif)

    @property
    def blockindex(self) -> int:
        return int(telnet('get_blockindex'))

    @property
    def version(self) -> str:
        return VERSION


cmd = Command()

try:
    with open(expanduser('~/.nan/store'), 'rb') as f:
        nan = load(f)
except:
    nan = Nan()
