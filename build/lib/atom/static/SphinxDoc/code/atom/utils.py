# -*- coding: utf-8 -*-
# author:shihua
# coder:shihua
# 这是一个辅助类，主要功能实现各种外部依赖工具功能，主要技术内部类和with上下文管理器

"""
模块介绍
-------

这是一个辅助类，主要功能实现各种外部依赖工具功能，主要技术内部类和with上下文管理器

设计模式：

    （1）  无

关键点：    

    （1）with上下文管理器

    （2）内部类

主要功能：            

    （1）实现各种外部依赖工具功能                                 

使用示例
-------


类说明
------

"""



####### 载入程序包 ##########################################################
############################################################################



import sqlite3
import pandas as pd
import datetime
import pika 
import json
from minio import Minio
from minio.error import S3Error
import dill
import io
import os
import sys



####### 辅助类 #############################################################
### 设计模式：                                                           ###
### （1）无                                                              ###
### 关键点：                                                             ###
### （1）with上下文管理器                                                 ###
### （2）内部类                                                           ###
### 主要功能：                                                            ###
### （1）实现各种外部依赖工具功能                                           ###
############################################################################


####### Sqlite3数据库连接类 ################################################
###########################################################################



class dbconnection(object):
    '''
    类介绍：

        这是一个数据库连接器管理类
    '''


    def __init__(self,dbpath = 'default'):
        '''
        属性功能:

            定义一个初始化Sqlite3连接管理的初始化属性方法

        参数:
            dbpath (str): Sqlite3数据库文件路径

        返回:
            无
        '''

        if dbpath == 'default':
            ### 获取atom工作空间    
            atom_workspace = os.environ['atom_workspace']
            system_platform = sys.platform
            if system_platform == 'win32':
                atom_db_path = atom_workspace + '\\'
            elif system_platform == 'linux':
                atom_db_path  = atom_workspace + '/'
            final_db_path = atom_db_path + 'atom.db'
        else:
            final_db_path = dbpath
        # print(final_db_path)
        ### SQLite3连接
        self.connection = sqlite3.connect(final_db_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA encoding = 'UTF-8';")



    def __enter__(self):
        '''
        方法功能：

            定义一个进入上下文管理器方法

        参数：
            无

        返回：
            无
        '''

        return self.cursor


    def __exit__(self,exc_type,exc_instance,traceback):
        '''
        方法功能：

            定义一个退出上下文管理器方法

        参数：
            exc_type (object): 执行类型
            exc_instacnce (object): 执行实例
            traceback (object): 执行记录

        返回：
            无
        '''

        self.cursor.close()
        self.connection.close()



####### RabbitMQ消息中间件连接类 ################################################
################################################################################



class mqconnection(object):
    '''
    类介绍：

        这是一个消息中间件连接器管理类
    '''
    
    def __init__(self,host,port):
        '''
        属性功能:

            定义一个初始化RabbitMQ连接管理的初始化属性方法

        参数:
            host (str): IP地址
            port (str): 端口

        返回:
            无
        '''

        userx = pika.PlainCredentials(username = 'admin',password = 'admin')
        parameters = pika.ConnectionParameters(host = host,port = port,virtual_host = '/',credentials = userx)
        self.connection = pika.BlockingConnection(parameters = parameters)
        self.channel = self.connection.channel()


    def __enter__(self):
        '''
        方法功能：

            定义一个进入上下文管理器方法

        参数：
            无

        返回：
            无
        '''

        return self.channel


    def __exit__(self,exc_type,exc_instance,traceback):
        '''
        方法功能：

            定义一个退出上下文管理器方法

        参数：
            exc_type (object): 执行类型
            exc_instacnce (object): 执行实例
            traceback (object): 执行记录

        返回：
            无
        '''

        self.channel.close()
        self.connection.close()



####### MinIO对象存储连接类 #####################################################
################################################################################



class minioconnection(object):
    '''
    类介绍：

        这是一个消息中间件连接器管理类
    '''
    
    def __init__(self,host,port):
        '''
        属性功能:

            定义一个初始化RabbitMQ连接管理的初始化属性方法

        参数:
            host (str): IP地址
            port (str): 端口

        返回:
            无
        '''

        endpoint = str(host) + ':' + str(port)
        client = Minio(endpoint = endpoint,
                    access_key = 'minioadmin',
                    secret_key = 'minioadmin',
                    secure = False)
        found = client.bucket_exists('atom')
        if not found:
            client.make_bucket('atom')
        else:
            print('Bucket already exists!')
        self.client = client


    def __enter__(self):
        '''
        方法功能：

            定义一个进入上下文管理器方法

        参数：
            无

        返回：
            无
        '''

        return self.client


    def __exit__(self,exc_type,exc_instance,traceback):
        '''
        方法功能：

            定义一个退出上下文管理器方法

        参数：
            exc_type (object): 执行类型
            exc_instacnce (object): 执行实例
            traceback (object): 执行记录

        返回：
            无
        '''

        self.client = None



####################################################################################
####################################################################################


