from .utils import get_params_str


class Material:
    def __init__(self, index:int, composition:list, mt:list=None, **kwargs) -> None:
        assert len(composition) % 2 == 0
        self.index = index
        self.zaid = composition[0::2]
        self.farction = composition[1::2]
        self.data = kwargs

        self.mt = mt

    def add_composition(self, *composition):
        assert len(composition) % 2 == 0
        self.zaid.append(composition[0::2])
        self.farction.append(composition[1::2])

    def update(self, **kwargs):
        self.data.update(kwargs)

    def __repr__(self) -> str:
        material_list = [f'{zzzaaa} {fraction}\n' for zzzaaa, fraction in zip(self.zaid, self.farction)]
        for data_name, value in self.data.items():
            material_list.append(f"{data_name}={value}\n")
        material_str = '      ' + '      '.join(material_list)
        mt_str = f"MT{self.index}  {get_params_str(self.mt)}\n" if self.mt is not None else ''
        return f'M{self.index}\n{material_str}' + mt_str