from atom.utils import *
from atom.manager import *
# import dill

def test_func(a,b):
    c = a + b * 2
    return c

### 存储应用
with minioconnection(host = '192.168.1.18',port = 9000) as client:
    ### 上传文件
    StoreModel = ManagerFactory.create_store_model(client)
    test_func = StoreModel.transform_to_bytes(test_func)
    print(type(test_func))
    client.put_object('atom','test_func',io.BytesIO(test_func),length = -1,part_size = 10 * 1024 * 1024)
    print("function upload well done!")
    response = client.get_object('atom','test_func')
    print("function download well done!")
    tmp_func_get = StoreModel.inverse_transform_from_bytes(response.read())
    print(type(tmp_func_get))
    c = tmp_func_get(1,2)
    print(c)