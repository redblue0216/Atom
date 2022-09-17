# -*- coding: utf-8 -*-
# author:shihua
# coder:shihua
# 这是一个配置类，主要功能设置环境变量和初始化，主要技术静态方法

"""
模块介绍
-------

这是一个配置类，主要功能设置环境变量和初始化，主要技术静态方法

设计模式：

    （1）  无

关键点：    

    （1）静态方法

主要功能：            

    （1）设置环境变量和初始化                             

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
import os
import sys
import yaml
from atom.utils import *



####### 辅助类 #############################################################
### 设计模式：                                                           ###
### （1）无                                                              ###
### 关键点：                                                             ###
### （1）静态方法                                                         ###
### 主要功能：                                                            ###
### （1）设置环境变量和初始化                                              ###
############################################################################


####### 配置类 #############################################################
###########################################################################



class Setup(object):
    '''
    类介绍：

        这是一个配置类，主要功能设置环境变量和初始化，主要技术静态方法
    '''


    @staticmethod
    def set_workspace(atom_workspace):
        '''
        方法功能：

            定义一个设置环境变量的静态方法

        参数：
            atom_workspace (str): atom工作空间环境变量
        
        返回：
            无
        '''

        os.environ['atom_workspace'] = atom_workspace
        system_platform = sys.platform
        if system_platform == 'win32':
            os.system('setx atom_workspace {}'.format(atom_workspace))
        elif system_platform == 'linux':
            os.system('echo export atom_workspace={} >> ~/.bashrc'.format(atom_workspace))
        print('Atom workspace set up well done!')            
        


    @staticmethod
    def initialization():
        '''
        方法功能：

            定义一个初始化的静态方法

        参数：
            无

        返回：
            无
        '''

        ### 获取atom工作空间    
        atom_workspace = os.environ['atom_workspace']
        system_platform = sys.platform
        if system_platform == 'win32':
            atom_db_path = atom_workspace + '\\'
        elif system_platform == 'linux':
            atom_db_path  = atom_workspace + '/'
        ### 创建数据和算子工作空间(文件夹)
        if not os.path.exists(atom_db_path + 'data'):
            os.mkdir(atom_db_path + 'data')
        if not os.path.exists(atom_db_path + 'operator'):
            os.mkdir(atom_db_path + 'operator')
        if not os.path.exists(atom_db_path + 'atom_config.yaml'):
            atom_config = {'store':'minio','store_host':'127.0.0.1','store_port':9000}
            with open(atom_db_path + 'atom_config.yaml','w') as atom_yaml:
                yaml.dump(atom_config,atom_yaml)
        ### 创建元数据库
        with dbconnection(atom_db_path + 'atom.db') as db:
            ### 创建数据集信息表
            db.execute('''CREATE TABLE IF NOT EXISTS DataInformation(
                tag TEXT NOT NULL,
                belong TEXT NOT NULL,
                object_name TEXT NOT NULL,
                remarks TEXT NOT NULL,
                time TEXT NOT NULL 
            )
            ''')
            ### 创建特征集信息表
            db.execute('''CREATE TABLE IF NOT EXISTS FeatureInformation(
                tag TEXT NOT NULL,
                belong TEXT NOT NULL,
                object_name TEXT NOT NULL,
                remarks TEXT NOT NULL,
                time TEXT NOT NULL
            )
            ''')
            ### 提交建表事务
            db.connection.commit()
            print('atom initialization successful!')
            

        
################################################################################
################################################################################


