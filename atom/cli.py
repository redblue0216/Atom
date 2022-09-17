# -*- coding: utf-8 -*-
# author:shihua
# coder:shihua
# 这是一个atom常用命令行接口类
"""
模块介绍
-------

这是一个atom常用命令行接口类

设计模式：

    无

关键点：    

    （1）click 

主要功能：            

    （1）atom程序管理
                                                     
使用示例
-------


类说明
------

"""



####### 载入程序包 ##########################################################
############################################################################



import click
import os
import pandas as pd
from rich.console import Console
import atom as at
from atom.scheduler import *
from atom.config import *
from atom.utils import *
import sys



####### CLI命令行接口 #######################################################
### 设计模式：                                                            ###
###     无                                                               ###
### 关键点：                                                              ###
### （1）click                                                           ###
### 主要功能：                                                            ###
### （1）atom程序管理                                                     ###
############################################################################



###### CLI命令行接口 #####################################################################
#########################################################################################


### atom命令组
@click.group()
@click.help_option('-H','--help')
@click.version_option('-V','--version')
def atom():
    console = Console()
    console.print("\n\
                   =========================================================================== \n\
                   =======                                                             ======= \n\
                   =======                    Hello! Welcome to Atom                   ======= \n\
                   =======                                                             ======= \n\
                   ===========================================================================",style="red")


### atom设置环境变量
@click.command(help="set up a workspace for atom")
@click.option("--workspace",help="atom worspace(system path)")
def set(workspace):
    console = Console()
    workspace = str(workspace)
    Setup.set_workspace(atom_workspace=workspace)
    console.print('=================================================================>>>>>> atom set a workspace {}'.format(workspace),style="red")


### atom初始化工作空间
@click.command(help="atom workspace initialize")
def init():
    console = Console()
    atom_workspace = os.environ['atom_workspace']
    console.print('=================================================================>>>>>> enter atom workspace {}'.format(atom_workspace),style="red")
    Setup.initialization()
    console.print('=================================================================>>>>>> atom initialize well done!',style="red")


### atom-metadata启动后台服务
@click.command(help="atom metadata service")
def metadata_service():
    console = Console()
    atom_workspace_path = os.environ['atom_workspace']
    console.print('=================================================================>>>>>> enter atom metadata path {}'.format(atom_workspace_path),style="red")
    console.print('=================================================================>>>>>> atom metadata servive start',style="red")
    system_platform = sys.platform
    if system_platform == 'win32':
        os.system("{} & cd {} & sqlite_web atom.db --host 0.0.0.0 --port 11021 --no-browser".format(atom_workspace_path[:2],atom_workspace_path))  
    elif system_platform == 'linux':
        os.system("cd {} & sqlite_web atom.db --host 0.0.0.0 --port 11021 --no-browser".format(atom_workspace_path)) 
    # sqlite_web atom.db --host 0.0.0.0 --port 11021 --browser


### atom启动后台服务
@click.command(help="start atom service")
def start_service():
    console = Console()
    api_path = at.__file__.replace('__init__.py','')### __init__.py前的atom\需要去掉，打包后
    console.print('=================================================================>>>>>> enter atom package path {}'.format(api_path),style="red")
    console.print('=================================================================>>>>>> atom servive start',style="red")
    system_platform = sys.platform
    if system_platform == 'win32':
        os.system("{} & cd {} & python api.py".format(api_path[:2],api_path))
    elif system_platform == 'linux':
        os.system("cd {} & python api.py".format(api_path))
    # uvicorn api:app --reload --host '0.0.0.0' --port 11020


### atom数据查询命令
@click.command(help="start atom service")
def query_data():
    console = Console()
    console.print('=================================================================>>>>>> atom data query',style="red")
    with dbconnection() as db:
        view_df = pd.read_sql('SELECT * FROM DataInformation',db.connection)
    console.print(view_df,style='blue')


### atom特征查询命令
@click.command(help="start atom service")
def query_feature():
    console = Console()
    console.print('=================================================================>>>>>> atom data query',style="red")
    with dbconnection() as db:
        view_df = pd.read_sql('SELECT * FROM FeatureInformation',db.connection)
    console.print(view_df,style='blue')


### 向atom命令组添加命令
atom.add_command(set)
atom.add_command(init)
atom.add_command(metadata_service)
atom.add_command(start_service)
atom.add_command(query_data)
atom.add_command(query_feature)


### python脚本主程化
if __name__ == '__main__':
    console = Console()
    console.print("\n\
                   =========================================================================== \n\
                   =======                                                             ======= \n\
                   =======                    Hello! Welcome to Atom                   ======= \n\
                   =======                                                             ======= \n\
                   ===========================================================================",style="red")
    atom()



##########################################################################################################################
##########################################################################################################################


