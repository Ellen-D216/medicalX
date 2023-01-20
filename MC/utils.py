from math import isclose


def get_params_str(params:list):
    total_str = ''
    if isinstance(params[0], list):
        total_str = ' '.join([str(i) for i in params[0]]) + '\n'
    else:
        total_str = str(params[0])
    for param in params[1:]:
        if isinstance(param, list):
            if total_str.endswith('\n'):
                total_str += '     ' + ' '.join([str(i) for i in param]) + '\n'
            else:
                total_str += '\n' + '     ' + ' '.join([str(i) for i in param]) + '\n'
        else:
            if total_str.endswith('\n'):
                total_str += '     '
            total_str += ' ' + str(param)
    return total_str


def get_dict_params_str(params:dict, first_line=False):
    params_str_list = []
    for key, value in params.items():
        if isinstance(value, list):
            param_str = ' '.join([str(i) for i in value])
            params_str_list.append(f'{key}={param_str}\n')
        else:
            params_str_list.append(f'{key}={value}\n')
    return '     '.join(params_str_list) if first_line else '     ' + '     '.join(params_str_list)


def close_to_zero(*args):
    for num in args:
        if not isclose(num, 0.):
            return False
    return True


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