import code
import readline
import rlcompleter
from . import nan
from . import cmd
readline.parse_and_bind("tab: complete")
code.interact(
    banner='''welcome to nan''',
    local={
        'nan': nan,
        'cmd': cmd,
    }
)
