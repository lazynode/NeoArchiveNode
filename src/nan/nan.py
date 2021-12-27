class Nan:
    def __init__(self) -> None:
        pass

    @property
    def exit(self):
        exit()

    @property
    def version(self):
        from . import VERSION
        return VERSION


nan = Nan()
