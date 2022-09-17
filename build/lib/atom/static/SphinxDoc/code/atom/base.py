# -*- coding: utf-8 -*-
# author:shihua
# coder:shihua
# 这是一个atom基础类模块，主要包括数据抽象类和算子抽象类
"""
模块介绍
-------

这是一个atom基础类模块，主要包括数据抽象类和算子抽象类

设计模式：

    （1）  无 

关键点：    

    （1）abstractmethod

主要功能：            

    （1）抽象接口                                   

使用示例
-------


类说明
------

"""



####### 载入程序包 ##########################################################
############################################################################



from abc import ABCMeta,abstractmethod



####### 数据模型基础抽象类 ##################################################
### 设计模式：                                                           ###
### （1）无                                                              ###
### 关键点：                                                             ###
### （1）abstractmethod                                                  ###
### 主要功能：                                                            ###
### （1）抽象接口                                                         ###
############################################################################


####### 数据抽象类 #############################################################
###############################################################################



class DataBase(metaclass = ABCMeta):
    '''
    类介绍：

        这是一个数据抽象类，主要提供增删改查四种管理功能接口
    '''


    @abstractmethod
    def register(self):
        '''
        方法功能：

            定义一个注册抽象方法        
        '''

        pass


    @abstractmethod
    def remove(self):
        '''
        方法功能：

            定义一个删除抽象方法
        '''

        pass


    @abstractmethod
    def modify(self):
        '''
        方法功能：

            定义一个修改抽象方法
        '''

        pass


    @abstractmethod
    def query(self):
        '''
        方法功能：

            定义一个查询抽象方法
        '''

        pass



####### 算子抽象类 #############################################################
###############################################################################



class OperatorBase(metaclass = ABCMeta):
    '''
    类介绍：

        这是一个数据抽象类，主要提供增删改查四种管理功能接口
    '''


    @abstractmethod
    def register(self):
        '''
        方法功能：

            定义一个注册抽象方法        
        '''

        pass


    @abstractmethod
    def remove(self):
        '''
        方法功能：

            定义一个删除抽象方法
        '''

        pass


    @abstractmethod
    def modify(self):
        '''
        方法功能：

            定义一个修改抽象方法
        '''

        pass


    @abstractmethod
    def query(self):
        '''
        方法功能：

            定义一个查询抽象方法
        '''

        pass


    @abstractmethod
    def run(self):
        '''
        方法功能：

            定义一个运行抽象方法
        '''

        pass



####### 存储抽象类 #############################################################
###############################################################################



class StoreBase(metaclass = ABCMeta):
    '''
    类介绍：

        这是一个存储抽象类，主要提供上传下载功能接口
    '''


    @abstractmethod
    def put(self):
        '''
        方法功能：

            定义一个上传抽象方法   
        '''

        pass


    @abstractmethod
    def get(self):
        '''
        方法功能：

            定义一个下载抽象方法
        '''

        pass


    @abstractmethod
    def remove(self):
        '''
        方法功能：

            定义一个删除抽象方法
        '''

        pass


    @abstractmethod
    def query(self):
        '''
        方法功能：

            定义一个查询抽象方法
        '''

        pass


####### 通信抽象类 #############################################################
###############################################################################



class CommunicationBase(metaclass = ABCMeta):
    '''
    类介绍：

        这是一个通信抽象类，主要提供生产消费确认消费三种功能接口
    '''


    @abstractmethod
    def produce(self):
        '''
        方法功能：

            定义一个生产抽象方法   
        '''

        pass


    @abstractmethod
    def consume(self):
        '''
        方法功能：

            定义一个消费抽象方法
        '''

        pass



######################################################################################
######################################################################################

