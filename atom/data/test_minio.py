from minio import Minio
from minio.error import S3Error
import pandas as pd
import dill
import io

client = Minio(endpoint = '192.168.1.18:9000',
               access_key = 'minioadmin',
               secret_key = 'minioadmin',
               secure = False)
found = client.bucket_exists('test')
if not found:
    client.make_bucket('test')
else:
    print('Bucket already exists!')

### 上传文件
df = pd.read_csv(r"D:\Workspace\JiYuan\WindPowerForecast\LSTM\demo\merge_data_GDTYUAN_ec.csv")
tmp_df = dill.dumps(df)#,"D:\Workspace\JiYuan\Atom\Demo\test\data\merge_data_GDTYUAN_ec.pkl")
client.put_object('test','merge_data_GDTYUAN_ec',io.BytesIO(tmp_df),length = -1,part_size = 10 * 1024 * 1024)
# client.fput_object('test','merge_data_GDTYUAN_ec_0',r"D:\Workspace\JiYuan\Atom\Demo\test\data\merge_data_GDTYUAN_ec.pkl")
print("file upload well done!")
response = client.get_object('test','merge_data_GDTYUAN_ec')
print("file download well done!")
tmp_data = dill.loads(response.read())
print(type(tmp_data))
print(tmp_data)
# client.remove_object('test','merge_data_GDTYUAN_ec')
info_object = client.stat_object('test','merge_data_GDTYUAN_ec')
print(info_object)
