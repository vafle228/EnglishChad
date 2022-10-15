class Subscribe:
    id: int = None
    chatid: int = None
    level: str = None

    def __init__(self, *args):
        attrs = ["id", "level", "chatid"]
        for i in range(min(len(args), len(attrs))):
            setattr(self, attrs[i], args[i])
