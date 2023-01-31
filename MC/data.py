from .utils import get_params_str, get_dict_params_str


class Data:
    def __init__(self, **kwargs) -> None:
        self.add(**kwargs)

    def add(self, **kwargs):
        for data_name, value in kwargs.items():
            setattr(self, data_name, value)

    def update(self, data_name:str, value):
        setattr(self, data_name, value)

    def remove(self, *args):
        for data_name, in args:
            delattr(self, data_name)

    def items(self):
        return self.__dict__.items()

    def __repr__(self) -> str:
        total_str = ''
        for data_name, value in self.items():
            if isinstance(value, list):
                data_str = data_name + ' ' + get_params_str(value) + '\n'
                total_str += data_str
            elif isinstance(value, dict):
                data_str = get_dict_params_str(value, True)
                if total_str.endswith('\n'):
                    total_str += data_name + ' ' + data_str
                else:
                    total_str += '\n' + data_name + ' ' + data_str
            else:
                total_str += str(value) + '\n'
        return total_str


class Tally:
    def __init__(self, index:int, tally_id:int, partical:str, tally_geom:str, comment:str=None,
                 de:dict=None, df:dict=None) -> None:
        assert tally_id in (1, 2, 4, 5, 6, 7, 8)
        self.index = f"{index}{tally_id}"
        self.mnemonic = f"F{index}{tally_id}:{partical}" if index else f"F{tally_id}:{partical}"
        self.geom = tally_geom
        self.comment = comment
        self.de = de
        self.df = df

    def __repr__(self) -> str:
        tally_str = f"{self.mnemonic}  {self.geom}\n"
        comment_str = f"FC{self.index}  {self.comment}\n" if self.comment is not None else ''
        de_df_str = ''
        if self.de is not None and self.df is not None:
            for de_index, df_index in zip(self.de, self.df):
                de_df_str = f'#      DE{de_index}          DF{df_index}\n'
                for de_value, df_value in zip(self.de[de_index], self.df[df_index]):
                    de_df_str += f'       {de_value}       {df_value}\n'
        return tally_str + comment_str + de_df_str


class Source:
    def __init__(self, si:dict=None, sp:dict=None, **kwargs) -> None:
        self.params = kwargs
        self.si = si
        self.sp = sp

    def __repr__(self) -> str:
        params_str = 'SDEF ' + get_dict_params_str(self.params, True)
        si_sp_str = ''
        if self.si is not None and self.sp is not None:
            for si_index, sp_index in zip(self.si, self.sp):
                si_sp_str = f'#      SI{si_index}          SP{sp_index}\n'
                for si_value, sp_value in zip(self.si[si_index], self.sp[sp_index]):
                    si_sp_str += f'       {si_value}       {sp_value}\n'
        return params_str + si_sp_str