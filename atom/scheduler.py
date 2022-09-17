# -*- coding: utf-8 -*-
# author:shihua
# coder:shihua
# 这是一个atom管理调度类模块，主要包括注册、删除、查询、修改、加载五大操作功能，主要技术采用装饰器模式和静态方法
"""
模块介绍
-------

这是一个atom管理调度类模块，主要包括注册、删除、查询、修改、加载五大操作功能，主要技术采用装饰器模式和静态方法

设计模式：

    （1）  装饰器模式

关键点：    

    （1）装饰器技术

主要功能：            

    （1）功能接口                                   

使用示例
-------


类说明
------

"""



####### 载入程序包 ##########################################################
############################################################################



from atom.manager import *
from atom.utils import *
from atom.config import *
from functools import wraps
import os
import sys
import yaml



####### Scheduler管理调度类 #################################################
### 设计模式：                                                            ###
### （1）装饰器模式                                                       ###
### 关键点：                                                             ###
### （1）装饰器技术                                                       ###
### 主要功能：                                                            ###
### （1）功能接口                                                         ###
############################################################################


####### Scheduler管理调度类 ######################################################
#################################################################################



class AtomScheduler(object):
    '''
    类介绍：

        这是一个管理器调度类，主要功能管理Atom的整体操作，包括注册、删除、查询、修改、加载五大操作功能，主要技术采用装饰器模式和静态方法
    '''


    def __init__(self,mode='delay'):
        '''
        属性功能：

            定义一个收集配置信息初始化属性方法

        参数：
            store_host (str): 存储MinIO的host,从yaml配置中获取
            store_port (int): 存储MinIO的port,从yaml配置中获取
            mode (str): 主要使用模式有即时模式in_time，延时模式delay

        返回：
            无
        '''

        ### 获取store的host和port
        ### 获取atom工作空间    
        atom_workspace = os.environ['atom_workspace']
        system_platform = sys.platform
        if system_platform == 'win32':
            atom_db_path = atom_workspace + '\\'
        elif system_platform == 'linux':
            atom_db_path  = atom_workspace + '/'
        ### 开始加载yaml配置
        atom_yaml = open(atom_db_path + 'atom_config.yaml')
        atom_config = yaml.load(stream=atom_yaml,Loader=yaml.FullLoader)
        store_host = atom_config['store_host']
        store_port = atom_config['store_port']
        ### 加载store的host和port
        self.store_host = store_host
        self.store_port = store_port
        self.mode = mode
        print('==============================================================>>>>>> Atom scheduler create well done!')
        print('==============================================================>>>>>> Atom mode is {}'.format(self.mode))


    def data_register(self,tag,belong,object_name,data_object,remarks='no remark'):
        '''
        方法功能：

            定义一个数据注册方法，主要功能存储数据元信息和数据对象

        参数：
            tag (str): 数据标签
            belong (str): 数据所属项目名称
            object_name (str): 对象名称
            data_object (object): 数据对象
            remarks (str): 备注

        返回：
            无
        '''

        print('==============================================================>>>>>> {} data register start!'.format(tag))
        ### datamodel信息管理环境构建
        with dbconnection() as db:
            ### 创建操作对象
            datamodel = ManagerFactory.create_data_model(connection=db)
            ### datamodel执行信息注册操作
            datamodel.register(tag=tag,
                               belong=belong,
                               object_name=object_name,
                               remarks=remarks)
        ### storemodel存储管理环境构建
        with minioconnection(host=self.store_host,port=self.store_port) as client:
            ### 创建操作对象
            storemodel = ManagerFactory.create_store_model(connection=client)
            ### 序列化文件
            bytes_obj = storemodel.transform_to_bytes(obj=data_object)
            ### 上传文件
            storemodel.put(bucket_name='atom',object_name=object_name,bytes_obj=bytes_obj)
        print('==============================================================>>>>>> {} data register well done!'.format(tag))


    def operator_register(self,tag,belong,object_name,operator_object=None,remarks='no remark'):
        '''
        方法功能：

            定义一个算子注册方法，主要功能存储算子元信息和算子对象，主要技术装饰器技术

        参数：
            tag (str): 算子标签
            belong (str): 算子所属数据项目名称
            object_name (str): 对象名称
            operator_object (object): 算子对象
            remarks (str): 备注

        返回：
            无
        '''
        
        if self.mode == 'in_time':
            def decorator(func):
                @wraps(func)
                def wrapper(*args,**kwargs):
                    print('==============================================================>>>>>> {} operator register start!'.format(tag))
                    ### operatormodel信息管理环境构建
                    with dbconnection() as db:
                        ### 创建操作对象
                        operatormodel = ManagerFactory.create_operator_model(connection=db)
                        ### operatormodel执行信息注册操作
                        operatormodel.register(tag=tag,
                                            belong=belong,
                                            object_name=object_name,
                                            remarks=remarks)
                        ### storemodel存储管理环境构建
                        with minioconnection(host=self.store_host,port=self.store_port) as client:
                            ### 创建操作对象
                            storemodel = ManagerFactory.create_store_model(connection=client)
                            ### 序列化文件
                            bytes_obj = storemodel.transform_to_bytes(obj=func)
                            ### 上传文件
                            storemodel.put(bucket_name='atom',object_name=object_name,bytes_obj=bytes_obj)
                    print('==============================================================>>>>>> {} operator register well done!'.format(tag))
                    result = func(*args,**kwargs)
                    return result
                return wrapper
            return decorator
        elif self.mode == 'delay':
            print('==============================================================>>>>>> operator register start!')
            ### operatormodel信息管理环境构建
            with dbconnection() as db:
                ### 创建操作对象
                operatormodel = ManagerFactory.create_operator_model(connection=db)
                ### operatormodel执行信息注册操作
                operatormodel.register(tag=tag,
                                    belong=belong,
                                    object_name=object_name,
                                    remarks=remarks)
                ### storemodel存储管理环境构建
                with minioconnection(host=self.store_host,port=self.store_port) as client:
                    ### 创建操作对象
                    storemodel = ManagerFactory.create_store_model(connection=client)
                    ### 序列化文件
                    bytes_obj = storemodel.transform_to_bytes(obj=operator_object)
                    ### 上传文件
                    storemodel.put(bucket_name='atom',object_name=object_name,bytes_obj=bytes_obj)
            print('==============================================================>>>>>> operator register well done!')

            
    def data_remove(self,tag,object_name):
        '''
        方法功能：

            定义一个数据删除方法，主要根据数据标签和数据对象名称来删除对象，数据对象名称未来可用于版本控制

        参数：
            tag (str): 数据标签
            object_name (str): 对象名称，可用于版本控制

        返回：
            无
        '''

        print('==============================================================>>>>>> {} data remove start!'.format(tag))
        ### datamodel信息管理环境构建
        with dbconnection() as db:
            ### 创建操作对象
            datamodel = ManagerFactory.create_data_model(connection=db)
            ### datamodel执行删除操作
            datamodel.remove(tag=tag,
                             object_name=object_name)
        ### storemodel存储管理环境构建
        with minioconnection(host=self.store_host,port=self.store_port) as client:
            ### 创建操作对象
            storemodel = ManagerFactory.create_store_model(connection=client)
            ### datamodel执行删除操作
            storemodel.remove(bucket_name='atom',object_name=object_name)
        print('==============================================================>>>>>> {} data remove well done!'.format(tag))
    

    def operator_remove(self,tag,object_name):
        '''
        方法功能：

            定义一个算子删除方法，主要根据算子标签和算子对象名称来删除对象，算子对象名称未来可用于版本控制

        参数：
            tag (str): 算子标签
            object_name (str): 对象名称，可用于版本控制

        返回：
            无
        '''

        print('==============================================================>>>>>> {} operator remove start!'.format(tag))
        ### operatormodel信息管理环境构建
        with dbconnection() as db:
            ### 创建操作对象
            operatormodel = ManagerFactory.create_operator_model(connection=db)
            ### datamodel执行删除操作
            operatormodel.remove(tag=tag,
                                 object_name=object_name)
        ### storemodel存储管理环境构建
        with minioconnection(host=self.store_host,port=self.store_port) as client:
            ### 创建操作对象
            storemodel = ManagerFactory.create_store_model(connection=client)
            ### datamodel执行删除操作
            storemodel.remove(bucket_name='atom',object_name=object_name)
        print('==============================================================>>>>>> {} operaotr remove well done!'.format(tag))


    def data_query(self,tag):
        '''
        方法功能：

            定义一个已注册数据查询方法

        参数：
            tag (str): 数据标签

        返回：
            view_df (DataFrame): 已注册数据查询表单
        '''        

        print('==============================================================>>>>>> {} data query start!'.format(tag))
        ### datamodel信息管理环境构建
        with dbconnection() as db:
            ### 创建操作对象
            datamodel = ManagerFactory.create_data_model(connection=db)
            ### datamodel执行查询操作
            view_df = datamodel.query(tag=tag)        
        print('==============================================================>>>>>> {} data query start!'.format(tag))
        return view_df


    def operator_query(self,tag):
        '''
        方法功能：

            定义一个已注册算子查询方法

        参数：
            tag (str): 算子标签

        返回：
            view_df (DataFrame): 已注册算子查询表单
        '''        

        print('==============================================================>>>>>> {} operator query start!'.format(tag))
        ### operatormodel信息管理环境构建
        with dbconnection() as db:
            ### 创建操作对象
            operatormodel = ManagerFactory.create_operator_model(connection=db)
            ### operatormodel执行查询操作
            view_df = operatormodel.query(tag=tag)        
        print('==============================================================>>>>>> {} operator query start!'.format(tag))
        return view_df    


    def data_modify(self):
        '''
        方法功能：

            定义一个数据修改方法，未开发，敬请期待

        参数：
            无

        返回：
            无
        '''        

        print('==============================================================>>>>>> data modify developling')


    def operator_modify(self):
        '''
        方法功能：

            定义一个算子修改方法，未开发，敬请期待

        参数：
            无

        返回：
            无
        '''        

        print('==============================================================>>>>>> operator modify developling')
 

    def data_load(self,tag,object_name):
        '''
        方法功能：

            定义一个数据加载方法，主要功能从远端存储加载数据对象

        参数：
            tag (str): 数据标签
            object_name (str): 对象名称

        返回：
            data_obj (objcet): 数据对象
        '''

        print('==============================================================>>>>>> {} data load start!'.format(tag))
        ### storemodel存储管理环境构建
        with minioconnection(host=self.store_host,port=self.store_port) as client:
            ### 创建操作对象
            storemodel = ManagerFactory.create_store_model(connection=client)
            ### 下载文件
            bytes_obj = storemodel.get(bucket_name='atom',object_name=object_name)
            ### 反序列化文件
            data_obj = storemodel.inverse_transform_from_bytes(bytes_obj=bytes_obj)
        print('==============================================================>>>>>> {} data load well done!'.format(tag))
        return data_obj


    def operator_load(self,tag,object_name):
        '''
        方法功能：

            定义一个算子加载方法，主要功能从远端存储加载算子对象

        参数：
            tag (str): 数据标签
            object_name (str): 对象名称

        返回：
            operator_obj (objcet): 数据对象
        '''

        print('==============================================================>>>>>> {} operator load start!'.format(tag))
        ### storemodel存储管理环境构建
        with minioconnection(host=self.store_host,port=self.store_port) as client:
            ### 创建操作对象
            storemodel = ManagerFactory.create_store_model(connection=client)
            ### 下载文件
            bytes_obj = storemodel.get(bucket_name='atom',object_name=object_name)
            ### 反序列化文件
            operator_obj = storemodel.inverse_transform_from_bytes(bytes_obj=bytes_obj)
        print('==============================================================>>>>>> {} operator load well done!'.format(tag))
        return operator_obj



##############################################################################################################################################
##############################################################################################################################################


