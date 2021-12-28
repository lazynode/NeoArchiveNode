import os
import code
import readline
import rlcompleter
import atexit
from . import nan
from . import cmd
historyPath = os.path.expanduser("~/.pyhistory")
def save_history(historyPath=historyPath):
    import readline
    readline.write_history_file(historyPath)
if os.path.exists(historyPath):
    readline.read_history_file(historyPath)
atexit.register(save_history)
readline.parse_and_bind("tab: complete")
del os, atexit, readline, rlcompleter, save_history, historyPath
code.interact(
    banner='''welcome to nan''',
    local={
        'nan': nan,
        'cmd': cmd,
    }
)
