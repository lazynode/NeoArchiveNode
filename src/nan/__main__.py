from . import cmd
from . import nan

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
