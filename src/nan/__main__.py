import code
import readline
import rlcompleter
from nan.nan import nan
readline.parse_and_bind("tab: complete")
code.interact(
    banner='''welcome to nan ''',
    local={
        'nan': nan,
    }
)
