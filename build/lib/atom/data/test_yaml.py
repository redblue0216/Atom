import os
import yaml
import sys


def test_func(a,b):
    c = a + b * 2
    return c

c = test_func.__call__(1,2)
print(test_func.__name__)



atom_workspace = os.environ['atom_workspace']
system_platform = sys.platform
if system_platform == 'win32':
    atom_db_path = atom_workspace + '\\'
elif system_platform == 'linux':
    atom_db_path  = atom_workspace + '/'
if not os.path.exists(atom_db_path + 'atom_config.yaml'):
    atom_config = {'store_host':'127.0.0.1','store_port':9000}
print(atom_db_path + 'atom_config.yaml')
### 开始加载yaml配置
atom_yaml = open(atom_db_path + 'atom_config.yaml')
print(atom_yaml)
atom_config = yaml.load(stream=atom_yaml,Loader=yaml.FullLoader)
print(atom_config)
import socket
res = socket.gethostbyname(socket.gethostname())
print(type(res))
import atom as at
api_path = at.__file__.replace('__init__.py','')
print(api_path)