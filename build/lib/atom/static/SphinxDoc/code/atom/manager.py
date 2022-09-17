# -*- coding: utf-8 -*-
# author:shihua
# coder:shihua
# 这是一个atom管理类，主要包括数据模型、算子模型、存储模型和通信模型的具体操作方法，主要使用类方法和内部类实现工厂模式

"""
模块介绍
-------

这是一个atom管理器工厂类，主要包括数据模型、算子模型、存储模型和通信模型的具体操作方法，主要使用类方法和内部类实现工厂模式

设计模式：

    （1）  工厂模式

关键点：    

    （1）classmethod

    （2）内部类

主要功能：            

    （1）实现数据模型、算子模型、存储模型和通信模型的具体操作方法                                  

使用示例
-------


类说明
------

"""



####### 载入程序包 ##########################################################
############################################################################



import datetime
from atom.base import *
import pandas as pd
import dill 
import io
import json



####### 管理器工厂类 ########################################################
### 设计模式：                                                            ###
### （1）工厂模式                                                         ###
### 关键点：                                                              ###
### （1）classmethod                                                      ###
### （2）内部类                                                           ###
### 主要功能：                                                            ###
### （1）实现数据模型、算子模型、存储模型和通信模型的具体操作方法              ###
############################################################################


####### 管理器工厂类 #############################################################
#################################################################################



class ManagerFactory(object):
    '''
    类介绍：

        这是一个管理各种操作方法的工厂类，主要功能提供数据模型、算子模型、存储模型和通信模型的具体操作，主要技术使用类方法和内部类实现工厂模式
    '''


    @classmethod
    def create_data_model(cls,connection):
        '''
        方法功能：

            定义一个创建数据模型实例的类方法

        参数：
            connection (Object): 数据库连接对象

        返回：
            DataModel (Object): 数据模型实例对象
        '''

        DataModel = cls.DataModel(connection = connection)
        return DataModel


    @classmethod
    def create_operator_model(cls,connection):
        '''
        方法功能：

            定义一个创建算子模型实例的类方法

        参数：
            connection (Object): 数据库连接对象

        返回：
            OperatorModel (Object): 数据模型实例对象
        '''

        OperatorModel = cls.OperatorModel(connection = connection)
        return OperatorModel


    @classmethod
    def create_store_model(cls,connection):
        '''
        方法功能：

            定义一个创建存储模型实例的类方法

        参数：
            connection (Object): 对象存储MinIO连接对象

        返回：
            OperatorModel (Object): 存储模型实例对象
        '''

        StoreModel = cls.StoreModel(connection = connection)
        return StoreModel


    @classmethod
    def create_communication_model(cls,connection):
        '''
        方法功能：

            定义一个创建通信模型实例的类方法

        参数：
            connection (Object): 对象存储MinIO连接对象

        返回：
            CommunicationModel (Object): 存储模型实例对象
        '''

        CommunicationModel = cls.CommunicationModel(connection = connection)
        return CommunicationModel



    class DataModel(DataBase):
        '''
        类介绍：

            这是一个数据模型具体实现类，主要提供增删改查四种管理功能
        '''


        def __init__(self,connection):
            '''
            属性功能：

                定义一个初始化数据模型的方法

            参数：
                connection (object): 数据库连接对象

            返回：
                无
            '''

            self.connection = connection

        
        def register(self,tag,belong,object_name,remarks = 'no remarks',*args,**kwargs):
            '''
            方法功能：

                定义一个注册具体实现方法

            参数：
                tag (str): 数据集名称
                belong (str): 所属项目名称
                object_name (str): 存储对象文件名称
                remarks (str): 备注

            返回：
                无        
            '''

            ### 信息注册
            timenow = str(datetime.datetime.now())
            self.connection.execute("INSERT INTO DataInformation (tag,belong,object_name,remarks,time) VALUES ('{}',\
                                                                                     '{}',\
                                                                                     '{}',\
                                                                                     '{}',\
                                                                                     '{}')".format(tag,belong,object_name,remarks,timenow))
            self.connection.connection.commit()
            print('DataModel {} register well done!'.format(tag))


        def remove(self,tag,object_name):
            '''
            方法功能：

                定义一个删除具体实现方法

            参数：
                tag (str): 数据模型标签
                object_name (str): 对象名称，可用于版本控制

            返回：
                无
            '''

            ### 信息删除
            timenow = str(datetime.datetime.now())
            self.connection.execute("DELETE FROM DataInformation WHERE tag = '{}' AND object_name = '{}'".format(tag,object_name))
            self.connection.connection.commit()
            print('DataModel {}----{} remove well done!'.format(tag,object_name))


        def modify(self):
            '''
            方法功能：

                定义一个修改具体实现方法
            '''

            ### 信息修改
            print('DataModel modify function is developing')


        def query(self,tag):
            '''
            方法功能：

                定义一个查询具体实现方法
            
            参数：
                tag (str): 数据模型标签

            返回：
                view_df (DataFrame): 查询数据
            '''

            ### 信息查询
            view_df = pd.read_sql('SELECT * FROM DataInformation',self.connection.connection)
            # print(type(view_df))
            # print(view_df)
            print('DataModel {} query well done'.format(tag))
            return view_df



    class OperatorModel(OperatorBase):
        '''
        类介绍：

            这是一个算子模型具体实现类，主要提供增删改查运行五种管理功能
        '''


        def __init__(self,connection):
            '''
            属性功能：

                定义一个初始化数据模型的方法

            参数：
                connection (object): 数据库连接对象

            返回：
                无
            '''

            self.connection = connection


        def register(self,tag,belong,object_name,remarks = 'no remarks',*args,**kwargs):
            '''
            方法功能：

                定义一个注册具体实现方法

            参数：
                tag (str): 数据集名称
                belong (str): 所属项目名称
                object_name (str): 存储对象文件名称
                remarks (str): 备注

            返回：
                无        
            '''

            ### 信息注册
            timenow = str(datetime.datetime.now())
            self.connection.execute("INSERT INTO FeatureInformation (tag,belong,object_name,remarks,time) VALUES ('{}',\
                                                                                     '{}',\
                                                                                     '{}',\
                                                                                     '{}',\
                                                                                     '{}')".format(tag,belong,object_name,remarks,timenow))
            self.connection.connection.commit()
            print('OperatorModel {} register well done!'.format(tag))


        def remove(self,tag,object_name):
            '''
            方法功能：

                定义一个删除具体实现方法

            参数：
                tag (str): 算子模型标签
                object_name (str): 对象名称，可用于版本控制

            返回：
                无
            '''

            ### 信息删除
            timenow = str(datetime.datetime.now())
            self.connection.execute("DELETE FROM FeatureInformation WHERE tag = '{}' AND object_name = '{}'".format(tag,object_name))
            self.connection.connection.commit()
            print('OperatorModel {}----{} remove well done!'.format(tag,object_name))


        def modify(self):
            '''
            方法功能：

                定义一个修改具体实现方法
            '''

            ### 信息修改
            print('OperatorModel modify function is developing')


        def query(self,tag):
            '''
            方法功能：

                定义一个查询具体实现方法
            
            参数：
                tag (str): 数据模型标签

            返回：
                view_df (DataFrame): 查询数据
            '''

            ### 信息查询
            view_df = pd.read_sql('SELECT * FROM FeatureInformation',self.connection.connection)
            # print(type(view_df))
            # print(view_df)
            print('OperatorModel {} query well done'.format(tag))
            return view_df


        def run(self,func_obj,*args,**kwargs):
            '''
            方法功能：

                定义一个运行函数对象的方法

            参数：
                func_obj (object): 函数对象

            返回：
                result (object): 函数结果对象
            '''

            result = func_obj.__call__(*args,**kwargs)
            func_name = func_obj.__name__
            print('{} function run well done!'.format(func_name))
            return result



    class StoreModel(StoreBase):
        '''
        类介绍：

            这是一个存储模型具体实现类，主要提供上传下载删除查询四种管理功能
        '''


        def __init__(self,connection):
            '''
            属性功能：

                定义一个初始化数据模型的方法

            参数：
                connection (object): 数据库连接对象

            返回：
                无
            '''

            self.connection = connection


        def transform_to_bytes(self,obj):
            '''
            方法功能：

                定义一个将对象序列化的方法

            参数：
                obj (Object): 需要序列化目标对象

            返回：
                bytes_obj (bytes): 序列化后的二进制对象
            '''

            tmp_bytes_obj = dill.dumps(obj)
            print('Transform well done!')
            return tmp_bytes_obj


        def inverse_transform_from_bytes(self,bytes_obj):
            '''
            方法功能：

                定义一个将对象序列化的方法

            参数：
                bytes_obj (bytes): 序列化后的二进制对象

            返回：
                obj (Object): 需要序列化目标对象
            '''

            tmp_obj = dill.loads(bytes_obj)
            print('Inverse transform well done!')
            return tmp_obj


        def put(self,bucket_name,object_name,bytes_obj):
            '''
            方法功能：

                定义一个上传数据方法        

            参数：
                bucket_name (str): 对象存储中桶的名称
                object_name (str): 二进制数据对象名称
                bytes_obj (object): 二进制对象
            
            返回：
                无
            '''

            self.connection.put_object(bucket_name=bucket_name,
                                       object_name=object_name,
                                       data=io.BytesIO(bytes_obj),
                                       length=-1,
                                       part_size=10 * 1024 * 1024)
            print('{} put well done!'.format(object_name))


        def get(self,bucket_name,object_name):
            '''
            方法功能：

                定义一个获取数据方法

            参数：
                bucket_name (str): 对象存储中桶的名称
                object_name (str): 二进制数据对象名称
            
            返回：
                bytes_obj (object): 二进制数据对象
            '''
            
            response = self.connection.get_object(bucket_name=bucket_name,
                                                  object_name=object_name)
            bytes_obj = response.read()
            print('{} get well done!'.format(object_name))
            return bytes_obj


        def remove(self,bucket_name,object_name):
            '''
            方法功能：

                定义一个删除数据方法

            参数：
                bucket_name (str): 对象存储中桶的名称
                object_name (str): 二进制数据对象名称
            
            返回：
                无
            '''

            self.connection.remove_object(bucket_name=bucket_name,
                                          object_name=object_name)
            print('{} remove well done!'.format(object_name))


        def query(self,bucket_name,object_name):
            '''
            方法功能：

                定义一个查询数据方法

            参数：
                bucket_name (str): 对象存储中桶的名称
                object_name (str): 二进制数据对象名称
            
            返回：
                info_object (Object): 存储数据信息对象
            '''

            info_object = self.connection.stat_object(bucket_name=bucket_name,
                                                      object_name=object_name)
            print('{} query well done!'.format(object_name))
            return info_object



    class CommunicationModel(CommunicationBase):
        '''
        类介绍：

            这是一个通信模型具体实现类，主要提供生产消费确认消费三种功能
        '''


        def __init__(self,connection):
            '''
            属性功能：

                定义一个初始化通信模型的方法

            参数：
                connection (object): 消息中间件连接对象

            返回：
                无
            '''

            self.connection = connection


        def produce(self,queue_name,message):
            '''
            方法功能：

                定义一个生产者方法，用来向消息中间件推送数据

            参数：
                queue_name (str): 消息队列名称
                message (json_dumps): 序列化后的json串

            返回：
                无
            '''

            queue_declare = self.connection.queue_declare(queue=queue_name,durable=True)
            handled_message = json.dumps(message)
            self.connection.basic_publish(exchange='',
                                          routing_key=queue_name,
                                          body=handled_message)
            print('produce push data well done!')


        def consume(self,queue_name,commit=False):
            '''
            方法功能：

                定义一个生产者方法，用来向消息中间件推送数据

            参数：
                queue_name (str): 消息队列名称

            返回：
                consume_data (objcet): 待消费消息队列的第一个数据
            '''
            

            data_obj = self.connection.basic_get(queue=queue_name)
            # 本次请求编号
            delivery_tag = data_obj[0].delivery_tag
            # 本次获取完毕剩余的个数(不包含本条)
            count = data_obj[0].message_count
            # 获得的数据
            consume_data = data_obj[-1].decode()
            if commit == True:
                # 提交本次响应结果
                self.connection.basic_ack(delivery_tag)
            else:
                pass
            print('consume pull well done!')
            return consume_data



##############################################################################################
##############################################################################################


