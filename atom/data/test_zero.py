
from atom.manager import *
from atom.utils import *
from atom.config import Setup
import os
import sys
import pika 
import json
def test_func(a,b):
    c = a + b * 2
    return c



print('=====================================================================    start testing')
### 工作空间初始化(python的os管理环境变量为临时性，代码中已使用命令行自动配置环境变量，如有问题可自行手动配置环境变量)
# Setup.set_workspace(atom_workspace = r'D:\Workspace\JiYuan\Atom\Demo\test')
# Setup.initialization()
# print(os.environ)



### 信息管理环境构建，包括数据模型和算子模型
with dbconnection() as db:
    ### 创建操作对象
    datamodel = ManagerFactory.create_data_model(connection=db)
    operatormodel = ManagerFactory.create_operator_model(connection=db)
    ### datamodel操作
    datamodel.register(tag='test',belong='first',object_name='merge_data_GDTYUAN_ec_0',remarks='this is a test data!')
    datamodel.query(tag='test')
    datamodel.modify()
    view_df = datamodel.query(tag='test')
    print(view_df)
    # datamodel.remove(tag = 'test',object_name='merge_data_GDTYUAN_ec_0')
    # datamodel.query(tag = 'test')
    ### operatormodel操作
    operatormodel.register(tag='test_func',belong='first',object_name='tmp_func',remarks='this is a test function!')
    operatormodel.query(tag='test_func')
    operatormodel.modify()
    # operatormodel.remove(tag='test_func')
    # operatormodel.query(tag='test_func')
    result = operatormodel.run(func_obj=test_func,a=1,b=2)
    print(result)



### 存储管理环境构建，包括序列化操作和传输数据操作
with minioconnection(host = '192.168.1.15',port = 9000) as client:
    ### 创建操作对象
    storemodel = ManagerFactory.create_store_model(connection=client)
    ### 序列化文件
    df = pd.read_csv(r"D:\Workspace\JiYuan\WindPowerForecast\LSTM\demo\merge_data_GDTYUAN_ec.csv")
    bytes_obj = storemodel.transform_to_bytes(obj=df)
    ### 上传文件
    storemodel.put(bucket_name='atom',object_name='merge_data_GDTYUAN_ec_0',bytes_obj=bytes_obj)
    ### 下载文件
    bytes_obj = storemodel.get(bucket_name='atom',object_name='merge_data_GDTYUAN_ec_0')
    ### 反序列化文件
    data_obj = storemodel.inverse_transform_from_bytes(bytes_obj=bytes_obj)
    print(data_obj)



### 通信管理环境构建，包括生产者消费者操作
with mqconnection(host = '192.168.1.15',port = 5672) as channel:
    ### 创建操作对象
    communicationmodel = ManagerFactory.create_communication_model(channel)
    ### 生产者推送数据
    tmp_message_dict = {'a':2022,'b':9,'c':15}
    communicationmodel.produce(queue_name='test',message=tmp_message_dict)
    ### 消费者消费数据
    communicationmodel.consume(queue_name='test',commit=False)
    





