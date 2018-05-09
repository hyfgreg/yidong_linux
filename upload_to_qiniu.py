from qiniu import put_file, etag, urlsafe_base64_encode
from config import Config
from datetime import datetime

def upload(Compress = Config.compress):
    if not Compress:
        file = Config.updateData_FILE
    else:
        file = Config.updateData_FILE_Compress
    if datetime.today().weekday() in [0,1,2,3,4]:
        key = Config.edbus_weekday
    else:
        key = Config.edbus_weekend
    try:
        localfile = Config.updateData_DIR + file

        token = Config.q.upload_token(Config.BUCKET_NAME, key, 3600)
        ret, info = put_file(token, key, localfile)
        print(info)
        assert ret['key'] == key
        assert ret['hash'] == etag(localfile)
        print('成功上传文档{}至{}'.format(key, Config.BUCKET_NAME))
        return '成功上传文档{}至{}'.format(key, Config.BUCKET_NAME)
    except Exception as e:
        print(e.args)
        raise e