from typing import Union

from .utils import close_to_zero, get_params_str


class Surface:
    def __init__(self, index:Union[int, str]) -> None:
        self.index = str(index)
        self.equation_params = None

    def __and__(self, surface):
        return Surface(f"{self.index} {surface.index}")

    def __or__(self, surface):
        return Surface(f"{self.index}:{surface.index}")

    def __sub__(self, surface):
        return Surface(f"{self.index} #{surface.index}")

    def __neg__(self):
        return Surface(f"#{self.index}")

    def __repr__(self) -> str:
        return self.index


class Geometry:
    @staticmethod
    def intersection(*surface:Surface, prior:bool=False) -> Surface:
        geom = surface[0]
        for i in range(1, len(surface)):
            geom = geom & surface[i]
        if prior:
            geom.index = f"({geom.index})"
            return geom
        else:
            return geom

    @staticmethod
    def union(*surface:Surface, prior:bool=False) -> Surface:
        geom = surface[0]
        for i in range(1, len(surface)):
            geom = geom | surface[i]
        if prior:
            geom.index = f"({geom.index})"
            return geom
        else:
            return geom

    @staticmethod
    def complement(surface:Surface, prior:bool=False) -> Surface:
        geom = Surface(surface.index)
        if prior:
            geom.index = f"({geom.index})"
            return -geom
        else:
            return -geom


class Plane(Surface):
    def __init__(self, index:int, a:float=1., b:float=0., c:float=0., d:float=1.) -> None:
        assert a or b or c
        super().__init__(index)
        self.equation_params = [a, b, c, d]

        if close_to_zero(b, c):
            self.type = 'PX'
            self.equation_params[3] = self.equation_params[3] / self.equation_params[0]
            self.equation_params[0] = 1
        elif close_to_zero(a, c):
            self.type = 'PY'
            self.equation_params[3] = self.equation_params[3] / self.equation_params[1]
            self.equation_params[1] = 1
        elif close_to_zero(a, b):
            self.type = 'PZ'
            self.equation_params[3] = self.equation_params[3] / self.equation_params[2]
            self.equation_params[2] = 1
        else:
            self.type = 'P'

    def __repr__(self) -> str:
        if self.type == 'P':
            str_eq_params = get_params_str(self.equation_params)
            return f"{self.index}  P  {str_eq_params}\n"
        else:
            return f"{self.index}  {self.type}  {self.equation_params[3]}\n"


class Sphere(Surface):
    def __init__(self, index:int, o1:float=0., o2:float=0., o3:float=0., r:float=1.) -> None:
        super().__init__(index)
        self.equation_params = [o1, o2, o3, r]

        if close_to_zero(o1, o2, o3):
            self.type = 'SO'
        elif close_to_zero(o2, o3):
            self.type = 'SX'
        elif close_to_zero(o1, o3):
            self.type = 'SY'
        elif close_to_zero(o1, o2):
            self.type = 'SZ'
        else:
            self.type = 'S'

    def __repr__(self) -> str:
        if self.type == 'SO':
            return f"{self.index}  SO  {self.equation_params[3]}\n"
        elif self.type == 'SX':
            return f"{self.index}  SX  {self.equation_params[0]}  {self.equation_params[3]}\n"
        elif self.type == 'SY':
            return f"{self.index}  SY  {self.equation_params[1]}  {self.equation_params[3]}\n"
        elif self.type == 'SZ':
            return f"{self.index}  SZ  {self.equation_params[2]}  {self.equation_params[3]}\n"
        else:
            str_eq_params = get_params_str(self.equation_params)
            return f"{self.index}  S  {str_eq_params}\n"


class Cylinder(Surface):
    def __init__(self, index:int, axis:int=0., o1:float=1., o2:float=0., r:float=1.) -> None:
        super().__init__(index)
        self.axis = axis
        self.equation_params = [o1, o2, r]

    def __repr__(self) -> str:
        if close_to_zero(*self.equation_params[:2]):
            if self.axis == 0:
                return f"{self.index}  CX  {self.equation_params[2]}\n"
            elif self.axis == 1:
                return f"{self.index}  CY  {self.equation_params[2]}\n"
            elif self.axis == 2:
                return f"{self.index}  CZ  {self.equation_params[2]}\n"
        else:
            str_eq_params = get_params_str(self.equation_params)
            if self.axis == 0:
                return f"{self.index}  C/X  {str_eq_params}\n"
            elif self.axis == 1:
                return f"{self.index}  C/Y  {str_eq_params}\n"
            elif self.axis == 2:
                return f"{self.index}  C/Z  {str_eq_params}\n"
