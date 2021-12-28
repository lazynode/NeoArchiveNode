class Nan:
    def __init__(self) -> None:
        from subprocess import Popen
        from subprocess import DEVNULL
        from subprocess import PIPE
        from os.path import expanduser
        self.__process = Popen(
            ['./neo-cli'],
            cwd=expanduser("~/.nan/neo-cli"),
            stdin=PIPE,
            stdout=DEVNULL,
            stderr=DEVNULL,
        )

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

    @property
    def exit(self) -> None:
        self.__process.terminate()
        self.__process.wait()
        exit()

    @property
    def blockindex(self) -> int:
        return int(self.__telnet(b'get_blockindex'))

    @property
    def version(self):
        from . import VERSION
        return VERSION


nan = Nan()
