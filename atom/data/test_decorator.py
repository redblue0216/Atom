from functools import wraps
import types


class TmpDecorator(object):

    def __init__(self,passwd):
        self.passwd = passwd

    def test_decorator(self,name):
        if self.passwd == '123456':
            def decorate(func):
                @wraps(func)
                def wrapper(*args,**kwargs):
                    print('this is a test decorator')
                    result = func(*args,**kwargs)
                    print('------',name,self.passwd)
                    return result
                return wrapper
            return decorate
        else:
            a = 'done'
            return a

    def test_transfer(self,data):
        print('this is a test transfer')
        return data + 1



Tmp = TmpDecorator('1234567')
# @Tmp.test_decorator('test')
def add_func(a,b):
    c = a + b
    return c

### 作用于函数
add_func_a = Tmp.test_decorator('test')(add_func)
c = add_func_a(1,2)
print(c)


### 作用于数据
d = 100
dd = Tmp.test_transfer(d)
print(dd)



# d = 100
# class dd(object):
#     def __init__(self,data):
#         self.data = data

# d_objected = dd(d)
# def calld(self):
#     return self.data

# import types
# d_objected.calld = types.MethodType(calld,d_objected)

# print(dir(d_objected))
# # dd = Tmp.test_transfer(d)
# # print(dd)
