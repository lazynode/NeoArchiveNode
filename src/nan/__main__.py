import os
import code
import readline
import rlcompleter
import atexit
from . import nan
from . import cmd
if os.path.exists(os.path.expanduser("~/.nan/history")):
    readline.read_history_file(os.path.expanduser("~/.nan/history"))
atexit.register(
    lambda: readline.write_history_file(os.path.expanduser("~/.nan/history"))
)
readline.parse_and_bind("tab: complete")
code.interact(
    banner='''
        $$$$$$$\   $$$$$$\  $$$$$$$\  
        $$  __$$\  \____$$\ $$  __$$\ 
        $$ |  $$ | $$$$$$$ |$$ |  $$ |
        $$ |  $$ |$$  __$$ |$$ |  $$ |
        $$ |  $$ |\$$$$$$$ |$$ |  $$ |
        \__|  \__| \_______|\__|  \__|
    ''',
    local={
        'nan': nan,
        'cmd': cmd,
    }
)
