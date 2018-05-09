from datetime import date,timedelta
import os
from qiniu import Auth
# import qiniu.config
import platform


def getYesterday():
    today = date.today()
    oneday = timedelta(days=1)
    yesterday = today - oneday
    return yesterday

class ConfigBase(object):
    ###上传的配置
    # if platform.platform().startswith('W'):
    #     DATAFOLDER = os.getcwd() + '\\data\\'
    # else:
    #     DATAFOLDER = os.getcwd() + '/data/'
    BUCKET_NAME = 'yimove'
    # BUCKET_NAME = {
    #     'default': 'yimove',
    #     'edrs': 'edbusroutelist',
    #     'edrsl': 'edbusroutestationlist',
    #     'edtt': 'edbustimetable',
    #     'evacl': 'evcardareacodelist',
    #     'evcsl': 'evcardcityshoplist',
    #     'evvml': 'evcardvehiclemodelist',
    #     'weather': 'weather'
    # }
    access_key = 'WxtU5PasZSCeEnuWZl_QtnlaIanDVSN7jO4s03HC'
    secret_key = 'GeRvR9HYjmwaM75PilZumocBfmfnv7KboMFWVp1f'
    q = Auth(access_key, secret_key)
    edbus_weekday = 'edbus_weekday.json.gz'
    edbus_weekend = 'edbus_weekend.json.gz'


    today = str(date.today())
    yesterday = str(getYesterday())
    BASE_DIR = os.getcwd()

    if platform.platform().startswith('W'):
        busSchedule_DIR = BASE_DIR + '\\data\\busSchedule\\'
        routeListSet_DIR = BASE_DIR + '\\data\\routeListSet\\'
        routeStationList_DIR = BASE_DIR + '\\data\\routeStationList\\'
        routeStationTime_DIR = BASE_DIR + '\\data\\routeStationTime\\'
    else:
        busSchedule_DIR = BASE_DIR + '/data/busSchedule/'
        routeListSet_DIR = BASE_DIR + '/data/routeListSet/'
        routeStationList_DIR = BASE_DIR + '/data/routeStationList/'
        routeStationTime_DIR = BASE_DIR + '/data/routeStationTime/'

    busSchedule_FILE = 'busSchedule' + today + '.json'
    routeListSet_FILE = 'routeListSet' + today + '.json'
    routeStationList_FILE = 'routeStationList' + today + '.json'
    routeStationTime_FILE = 'routeStationTime' + today + '.json'

    #是否压缩
    compress = True

    #驿动api
    official_url = 'http://ydwl.ev-shanghai.com/ydwl-app'
    demo_url = 'http://ydwl.fzkuliya.com/ydwl-app'
    yidong_port = 80



class Config(ConfigBase):
    if platform.platform().startswith('W'):
        updateData_DIR = ConfigBase.BASE_DIR + '\\updateData\\'
    else:
        updateData_DIR = ConfigBase.BASE_DIR + '/updateData/'
    updateData_FILE = 'edbus'+ConfigBase.today+'.json'
    updateData_FILE_Compress = 'edbus' + ConfigBase.today + '.json.gz'
    yesterday_FILE = 'edbus' + ConfigBase.yesterday +'.json'
    yesterday_FILE_Compress = 'edbus' + ConfigBase.yesterday + '.json.gz'

    yidong_url = ConfigBase.official_url



# class Config_test(ConfigBase):
#     today = str(date.today())
#     yesterday = str(getYesterday())
#     BASE_DIR = os.getcwd()
#
#     busSchedule_DIR = BASE_DIR + '\\data\\busSchedule\\'
#     routeListSet_DIR = BASE_DIR + '\\data\\routeListSet\\'
#     routeStationList_DIR = BASE_DIR + '\\data\\routeStationList\\'
#     routeStationTime_DIR = BASE_DIR + '\\data\\routeStationTime\\'
#
#     testdate = '2018-03-25'
#     testyesterday = '2018-03-24'
#
#     busSchedule_FILE = 'busSchedule' + testdate + '.json'
#     routeListSet_FILE = 'routeListSet' + testdate + '.json'
#     routeStationList_FILE = 'routeStationList' + testdate + '.json'
#     routeStationTime_FILE = 'routeStationTime' + testdate + '.json'
#
#     updateData_DIR = ConfigBase.BASE_DIR + '\\updateData\\'
#     updateData_FILE = 'edbus' + testdate + '.json'
#     updateData_FILE_Compress = 'edbus' + testdate + '.json.gz'
#     yesterday_FILE = 'edbus' + testyesterday+ '.json'
#     yesterday_FILE_Compress = 'edbus' + testyesterday + '.json.gz'
#
#     yidong_url = ConfigBase.demo_url


#email
class Email(object):
    from_addr = 'hyfgreg@163.com'
    password = 'Zhangxia2008111'
    to_addr = 'hyfgreg@163.com'
    smtp_server = 'smtp.163.com'
    smtp_port = 25