from time import sleep

from qiniu import put_file, etag, urlsafe_base64_encode,CdnManager
from config import Config
from datetime import datetime

def upload(Compress = Config.compress,refresh_flag=True):
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
        if refresh_flag:
            sleep(5)
            result = refresh()
        # return '成功上传文档{}至{}'.format(key, Config.BUCKET_NAME)
        return info,result
    except Exception as e:
        print(e.args)
        raise e

def refresh():
    cdn_manager = CdnManager(Config.q)
    refresh_url_result = cdn_manager.refresh_urls(Config.urls)
    print(refresh_url_result)
    return refresh_url_result

if __name__ == '__main__':
    refresh()