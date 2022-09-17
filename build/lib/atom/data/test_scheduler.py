from atom.scheduler import *

### 加载Atom调度器
atom = AtomScheduler(mode='delay')


### register-data测试
df = pd.read_csv(r"D:\Workspace\JiYuan\WindPowerForecast\LSTM\demo\merge_data_GDTYUAN_ec.csv")
atom.data_register(tag='test',
                   belong='first',
                   object_name='merge_data_GDTYUAN_ec_1',
                   data_object=df,
                   remarks='this is a test data!')

### register-operator测试
### 即时模式----装饰器方式
# @atom.operator_register(tag='test',
#                         belong='first',
#                         object_name='test_function_a',
#                         remarks='this is a test operator!')
def test_function(a,b):
    c = a + b * 2 + 1
    return c
# tmp_a = test_function(1,2)
### 及时模式----函数方式
# tmp_func = atom.operator_register(tag='test',
#                         belong='first',
#                         object_name='test_function_b',
#                         remarks='this is a test operator!')(test_function)
# tmp_b = tmp_func(3,4) 
### 延时模式
atom.operator_register(tag='test',
                       belong='first',
                       object_name='test_function_a', ## cc
                       operator_object=test_function,
                       remarks='this is a test operator!')


# ### data-remove测试
# atom.data_remove(tag='test',object_name='merge_data_GDTYUAN_ec_00')


### operator-remove测试
# atom.operator_remove(tag='test',object_name='test_function_cc')
 
                       
### data-query测试
data_view_df = atom.data_query(tag='test')
print(data_view_df)


### operator-query测试
operator_view_df = atom.operator_query(tag='test')
print(operator_view_df)


### data-modify测试
atom.data_modify()


### operator-modify测试
atom.operator_modify()


### data-load测试
data_load_df = atom.data_load(tag='test',object_name='merge_data_GDTYUAN_ec_1')
print(data_load_df)


### operator-load测试
operator_load_a = atom.operator_load(tag='test',object_name='test_function_a')
print(operator_load_a(10,20))
# print(test_function(**{'a':10,'b':20})) ### 字典参数传递