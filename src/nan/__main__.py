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
 __          __  _                            _          _   _          _   _ 
 \ \        / / | |                          | |        | \ | |   /\   | \ | |
  \ \  /\  / /__| | ___ ___  _ __ ___   ___  | |_ ___   |  \| |  /  \  |  \| |
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  | . ` | / /\ \ | . ` |
    \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) | | |\  |/ ____ \| |\  |
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/  |_| \_/_/    \_\_| \_|
                                                                              ''',
    local={
        'nan': nan,
        'cmd': cmd,
    }
)
