# -*- coding: utf-8 -*-
# author:shihua
# coder:shihua
# 这是一个atom服务应用类，主要使用fastapi搭建ASGI服务器
"""
模块介绍
-------

这是一个atom服务应用类，主要使用fastapi搭建ASGI服务器

设计模式：

    无

关键点：    

    （1）fastapi

主要功能：            

    （1）atom服务应用
                                                     
使用示例
-------


类说明
------

"""



####### 载入程序包 ##########################################################
############################################################################



from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from atom.scheduler import *
import atom as at
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import RedirectResponse
import socket
import sys



####### atom服务应用 ########################################################
### 设计模式：                                                            ###
###     无                                                               ###
### 关键点：                                                              ###
### （1）fastapi                                                          ###
### 主要功能：                                                            ###
### （1）atom服务应用                                                     ###
############################################################################



###### Atom-FastAPI初始操作 #####################################################################
################################################################################################


### 创建FastAPI应用实例
app = FastAPI()
### 获取模板路径
api_path = at.__file__.replace('__init__.py','')
system_platform = sys.platform
if system_platform == 'win32':
    templates_path = api_path + '\\'
elif system_platform == 'linux':
    templates_path = api_path + '/'
### 创建模板应用实例
templates = Jinja2Templates(directory=templates_path + 'templates')


### 定义数据模型
class FeatureComputerParam(BaseModel):
    '''
    类介绍：

        这是一个特征计算参数数据模型类，主要包括算子标签tag,对象名称object_name和数据字典data_json
    '''

    tag: str = 'hello'
    object_name: str = 'world'
    data_json: dict = None



###### Atom-FastAPI路由操作 #####################################################################
################################################################################################



### hello_world路由
@app.get("/atom")
async def atom(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})


### feature_compute特征计算路由
@app.post("/feature_compute")
async def feature_compute(feature_computer_param: FeatureComputerParam):
    ### 加载Atom调度器
    atom = AtomScheduler(mode='delay')
    ### 获取数据
    tag = feature_computer_param.tag
    object_name = feature_computer_param.object_name
    data_json = feature_computer_param.data_json
    operator_load = atom.operator_load(tag=tag,object_name=object_name)
    operator_result = operator_load.__call__(**data_json)
    print('=====================================================>>>>>> operator_result {}'.format(operator_result))
    return operator_result


### data_query路由
@app.get("/data_query")
async def data_query(): 
    ### 获取当前执行python主机IP
    exector_ip = socket.gethostbyname(socket.gethostname())
    response = RedirectResponse('http://{}:11021/DataInformation/content/'.format(exector_ip))
    return response


### operator_query路由
@app.get("/operator_query")
async def operator_query():
    ### 获取当前执行python主机IP
    exector_ip = socket.gethostbyname(socket.gethostname())    
    response = RedirectResponse('http://{}:11021/FeatureInformation/content/'.format(exector_ip))
    return response


### python脚本主程化
if __name__ == '__main__':
    uvicorn.run(app='api:app',host='0.0.0.0',port=11020,reload=True,debug=True)



######################################################################################################################
######################################################################################################################


