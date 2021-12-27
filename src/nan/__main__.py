import code
import readline
import rlcompleter
readline.parse_and_bind("tab: complete")
code.interact(
    banner='''welcome to nan ''',
    local={}
)
