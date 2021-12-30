from . import cmd
from . import nan


import os
if not os.path.exists(os.path.expanduser("~/.nan/neo-cli")):
    if __import__('platform').machine() != "x86_64":
        print("Your machine is x86 which is not supported!")
        exit(1)
    url = ""
    if __import__('platform').system() == "Linux":
        url = "https://github.com/lazynode/NeoArchiveNode/archive/refs/tags/neo-cli-linux-x64-3.1.0.tar.gz"
        dir_name = "NeoArchiveNode-neo-cli-linux-x64-3.1.0"
    else:
        print("Your system is not supported!")
        exit(1)
    print("Downloading neo-cli, pelease wait a minute......")
    import urllib.request
    import tarfile
    import shutil
    file_name, _ = urllib.request.urlretrieve(url)
    print("Decompressing {}, pelease wait a minute......".format(file_name))
    with tarfile.open(file_name) as file:
        file.extractall(file_name+"_extracted")
    shutil.move(file_name+"_extracted/"+dir_name, os.path.expanduser("~/.nan/neo-cli"))
    print("neo-cli preparation compelete, enjoy your nan")
    del urllib.request, tarfile, shutil, url, file_name
del os


__import__('rlcompleter')

try:
    __import__('readline').read_history_file(
        __import__('os').path.expanduser("~/.nan/history"),
    )
except:
    pass


__import__('atexit').register(
    lambda: __import__('readline').write_history_file(
        __import__('os').path.expanduser("~/.nan/history"),
    ),
)
__import__('atexit').register(
    lambda: __import__('pickle').dump(
        nan,
        open(__import__('os').path.expanduser('~/.nan/store'), 'wb',
             0o400,
             ),
    ),
)
__import__('atexit').register(
    (lambda p: lambda: p.terminate() or p.wait())(
        __import__('subprocess').Popen(
            ['./neo-cli'],
            cwd=__import__('os').path.expanduser("~/.nan/neo-cli"),
            stdin=__import__('subprocess').PIPE,
            stdout=open(__import__('os').path.expanduser(
                "~/.nan/neo-cli.stdout"),
                'w',
            ),
            stderr=open(__import__('os').path.expanduser(
                "~/.nan/neo-cli.stderr"),
                'w',
            ),
        )
    ),
)


__import__('readline').parse_and_bind("tab: complete")


__import__('code').interact(
    banner='''
        $$$$$$$\   $$$$$$\  $$$$$$$\  
        $$  __$$\  \____$$\ $$  __$$\ 
        $$ |  $$ | $$$$$$$ |$$ |  $$ |
        $$ |  $$ |$$  __$$ |$$ |  $$ |
        $$ |  $$ |\$$$$$$$ |$$ |  $$ |
        \__|  \__| \_______|\__|  \__|
    ''',
    local=locals(),
)
