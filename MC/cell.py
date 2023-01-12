from typing import Union

from .surface import Surface


class Cell:
    def __init__(self, index:int, material:int, 
                 density:float, geom:Union[Surface, str], **kwargs) -> None:
        self.index = index
        self.material = material
        self.density = density
        self.geom = geom if isinstance(geom, str) else geom.index
        self.data = kwargs

    def __repr__(self) -> str:
        data_list = [f'{key}={value}\n' for key, value in self.data.items()]
        data_str = '      ' + '      '.join(data_list)
        return f"{self.index}  {self.material}  {self.density}  {self.geom}\n{data_str}"

