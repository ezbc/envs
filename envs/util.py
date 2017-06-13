import importlib
import sys
import ast
import os
import json

from click._compat import raw_input

from . import Env

VAR_TYPES = Env.valid_types.keys()

def import_util(imp):
    '''
    Lazily imports a utils (class,
    function,or variable) from a module) from
    a string.
    @param imp:
    '''

    mod_name, obj_name = imp.rsplit('.', 1)
    mod = importlib.import_module(mod_name)
    return getattr(mod, obj_name)

def convert_module(module):
    attr_list = []
    for k, v in module.__dict__.items():
        if k.isupper():
            convert = bool(int(raw_input('Convert {}? (1=True,0=False): '.format(k))))
            attr_dict = {'name': k, 'convert': convert}

            var_type = raw_input('Variable Type Choices (ex. boolean,string,list,tuple,integer,float,dict): ')
            if not var_type in VAR_TYPES:
                raise ValueError('{} not in {}'.format(var_type,VAR_TYPES))
            attr_dict['var_type'] = var_type

            default_val = raw_input('Default Value? (default: {}): '.format(v))
            if default_val:
                default_val = ast.literal_eval(default_val)
            if not default_val:
                default_val = v
            attr_dict['default_val'] = default_val
            attr_list.append(attr_dict)
    return attr_list

def import_mod(module):
    if sys.version_info.major == 3:
        try:
            m = importlib.import_module(module)
        except ModuleNotFoundError:
            sys.path.insert(0,os.getcwd())
            m = importlib.import_module(module)
    else:
        try:
            m = importlib.import_module(module)
        except ImportError:
            sys.path.insert(0,os.getcwd())
            m = importlib.import_module(module)
    return m

def list_envs_module(module):
    with open('.envs_result','w+') as f:
        f.write('[')
    import_mod(module)
    with open('.envs_result', 'a') as f:
        f.write('{}]')
    with open('.envs_result','r') as f:
        envs_result = json.load(f)
        envs_result.pop()
    return envs_result
