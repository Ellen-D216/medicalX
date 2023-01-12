


class Material:
    def __init__(self, index:int, *args, **kwargs) -> None:
        self.index = index
        self.zaid = args[0::2]
        self.farction = args[1::2]
        self.data = kwargs

    def __repr__(self) -> str:
        material_list = [f'{zzzaaa} {fraction}\n' for zzzaaa, fraction in zip(self.zaid, self.farction)]
        material_str = '      '.join(material_list)
        return f'M{self.index}\n{material_str}'