def main():
    import code
    import readline
    import rlcompleter
    readline.parse_and_bind("tab: complete")
    code.interact(banner="Welcome to NAN!", local=locals())
