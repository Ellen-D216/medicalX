from typing import Union

from .surface import Surface
from .utils import get_dict_params_str


class Cell:
    def __init__(self, index:int, material:int, 
                 density:float, geom:Union[Surface, str], **kwargs) -> None:
        self.index = index
        self.material = material
        self.density = density
        self.geom = geom if isinstance(geom, str) else geom.index
        self.data = kwargs

    def __repr__(self) -> str:
        data_str = get_dict_params_str(self.data)
        return f"{self.index}  {self.material}  {self.density}  {self.geom}\n{data_str}"

