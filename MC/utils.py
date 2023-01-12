class Composite:
    def __init__(self, composite:list) -> None:
        self.composite = composite

    def append(self, plugin):
        self.composite.append(plugin)

    def pop(self, index):
        self.composite.pop(index)

    def clear(self):
        self.composite.clear()

    def __len__(self):
        return len(self.composite)

    def __getitem__(self, index):
        return self.composite[index]

    def __repr__(self) -> str:
        str_composite = [str(i) for i in self.composite]
        return ''.join(str_composite)