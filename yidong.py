import json
import time
from collections import OrderedDict
from datetime import datetime, date
import hashlib
import uuid
import requests
import sys

from config import Config
from custom_error import CustomError

import pymongo

client = pymongo.MongoClient('localhost', connect=False)
db = client['yidong']

key = '12Xso1XU9sd3SDJ8s0kcsxops9'
url_StationTime = '/tj/routeStationTime/queryRouteStationTime.jhtml'  # 到站时间信息
url_BusSchedule = '/tj/route/queryBusSchedule.jhtml'  # 排班信息
url_Car = '/tj/route/getRouteCarDynamic.jhtml'


class QueryYidong(object):
    def __init__(self):
        self._key = key
        self._nonceStr = str(uuid.uuid1())
        # self._url_official = 'http://ydwl.ev-shanghai.com'
        self._url_demo = Config.yidong_url  # 读取config中的url
        self._port = ':' + str(Config.yidong_port)
        self._url_queryBusSchedule = '/tj/route/queryBusSchedule.jhtml'  # 排班信息
        self._url_queryRouteStionList = '/tj/route/queryRouteStationList.jhtml'  # 站点信息
        self._url_queryRouteList = '/tj/route/queryRouteList.jhtml'  # 线路信息
        self._url_queryRouteStationTime = '/tj/routeStationTime/queryRouteStationTime.jhtml'  # 时刻表
        self._url_getRouteCarDynamic = '/tj/route/getRouteCarDynamic.jhtml'  # 车辆实时动态
        self._routeList = []
        self._save_func = [self.saveBusSchedule, self.saveRouteList, self.saveRouteStationList,
                           self.saveRouteStationTime]

    def queryBusSchedule(self, routeSeq=None, scheduleDate=str(date.today())):
        text = self._queryBusSchedule(routeSeq=routeSeq, scheduleDate=scheduleDate)
        return self.parse_data(text)

    def _queryBusSchedule(self, routeSeq=None, scheduleDate=str(date.today())):

        timestamp = str(int(time.time()))

        if not routeSeq:
            # routeSeq为空，则代表查询所有的排班
            signParam = 'nonceStr=' + self._nonceStr + '&scheduleDate=' + str(
                scheduleDate) + '&timestamp=' + timestamp + '&key=' + key
        else:
            # routeSeq不为空，查询某一班车的排班
            signParam = 'nonceStr=' + self._nonceStr + '&routeSeq=' + str(routeSeq) + '&scheduleDate=' + str(
                scheduleDate) + '&timestamp=' + timestamp + '&key=' + key

        signValue = hashlib.md5(signParam.encode('utf-8')).hexdigest().upper()

        if not routeSeq:
            data = {
                'nonceStr': self._nonceStr,
                'timestamp': timestamp,
                'sign': signValue,
                # 'routeSeq': routeSeq,
                'scheduleDate': scheduleDate
            }
        else:
            data = {
                'nonceStr': self._nonceStr,
                'timestamp': timestamp,
                'sign': signValue,
                'routeSeq': routeSeq,
                'scheduleDate': scheduleDate
            }

        try:
            # print(self._url_demo+self._url_queryBusSchedule)
            response = requests.post(url=self._url_demo + self._url_queryBusSchedule, data=data)
            if response.status_code == 200:
                return response.text
            else:
                print('请求失败', response.status_code)
                print(response.text)
                raise CustomError(
                    sys._getframe().f_code.co_name + 'code {}, {}'.format(response.status_code, response.text))
                return None
        except Exception as e:
            print('请求错误')
            raise e
            return e.args

    def queryRouteStationList(self, routeSeq=None):
        assert routeSeq is not None
        text = self._queryRouteStationList(routeSeq)
        return self.parse_data(text)

    def _queryRouteStationList(self, routeSeq=None):
        timestamp = str(int(time.time()))
        signParam = 'nonceStr=' + self._nonceStr + '&routeSeq=' + str(
            routeSeq) + '&timestamp=' + timestamp + '&key=' + self._key
        signValue = hashlib.md5(signParam.encode('utf-8')).hexdigest().upper()

        data = {
            'nonceStr': self._nonceStr,
            'timestamp': timestamp,
            'sign': signValue,
            'routeSeq': routeSeq,
        }

        try:
            response = requests.post(url=self._url_demo + self._url_queryRouteStionList, data=data)
            if response.status_code == 200:
                return response.text
            else:
                print('请求失败', response.status_code)
                print(response.text)
                raise CustomError(
                    sys._getframe().f_code.co_name + 'code {}, {}'.format(response.status_code, response.text))
                return None
        except Exception as e:
            print('请求错误')
            raise e
            return e.args

    def queryRouteList(self, categoryType=None):
        text = self._queryRouteList()
        return self.parse_data(text)

    def _queryRouteList(self, categoryType=None):
        timestamp = str(int(time.time()))
        signParam = 'nonceStr=' + self._nonceStr + '&timestamp=' + timestamp + '&key=' + self._key
        signValue = hashlib.md5(signParam.encode('utf-8')).hexdigest().upper()

        data = {
            'nonceStr': self._nonceStr,
            'timestamp': timestamp,
            'sign': signValue,
        }

        try:
            response = requests.post(url=self._url_demo + self._url_queryRouteList, data=data)
            if response.status_code == 200:
                return response.text
            else:
                print('请求失败', response.status_code)
                print(response.text)
                raise CustomError(
                    sys._getframe().f_code.co_name + 'code {}, {}'.format(response.status_code, response.text))
                return None
        except Exception as e:
            print('请求错误')
            raise e
            return e.args

    def queryRouteStationTime(self, routeSeq=None, routeCode=None, type=0):
        text = self._queryRouteStationTime(routeSeq, routeCode, type)
        return self.parse_data(text)

    def _queryRouteStationTime(self, routeSeq=None, routeCode=None, type=0):
        timestamp = str(int(time.time()))
        signParam = 'nonceStr=' + self._nonceStr + '&timestamp=' + timestamp + '&key=' + self._key
        signValue = hashlib.md5(signParam.encode('utf-8')).hexdigest().upper()

        if routeSeq and routeCode:
            data = {
                'nonceStr': self._nonceStr,
                'timestamp': timestamp,
                'sign': signValue,
                'routeSeq': str(routeSeq),
                'routeCode': routeCode,
                'type': type
            }
        elif routeSeq and not routeCode:
            data = {
                'nonceStr': self._nonceStr,
                'timestamp': timestamp,
                'sign': signValue,
                'routeSeq': str(routeSeq),
                'type': type
            }
        elif routeCode and not routeSeq:
            data = {
                'nonceStr': self._nonceStr,
                'timestamp': timestamp,
                'sign': signValue,
                'routeCode': routeCode,
                'type': type
            }
        else:
            data = {
                'nonceStr': self._nonceStr,
                'timestamp': timestamp,
                'sign': signValue,
                # 'type': type
            }

        try:
            response = requests.post(url=self._url_demo + self._url_queryRouteStationTime, data=data)
            if response.status_code == 200:
                return response.text
            else:
                print('请求失败', response.status_code)
                print(response.text)
                raise CustomError(
                    sys._getframe().f_code.co_name + 'code {}, {}'.format(response.status_code, response.text))
                return None
        except Exception as e:
            print('请求错误')
            raise e
            return e.args

    def getRouteCarDynamic(self, busline=None, vehicleNo=None):
        text = self._getRouteCarDynamic(busline, vehicleNo)
        return self.parse_data(text)

    def _getRouteCarDynamic(self, busline=None, vehicleNo=None):
        # busline: 0上行，1下行
        # vehicleNo: 车牌号
        timestamp = str(int(time.time()))
        signParam = 'nonceStr=' + self._nonceStr + '&timestamp=' + timestamp + '&key=' + key
        signValue = hashlib.md5(signParam.encode('utf-8')).hexdigest().upper()

        if vehicleNo:
            data = {
                'nonceStr': self._nonceStr,
                'timestamp': timestamp,
                'sign': signValue,
                'vehicleNo': vehicleNo
            }
        else:
            data = {
                'nonceStr': self._nonceStr,
                'timestamp': timestamp,
                'sign': signValue,
            }

        try:
            response = requests.post(self._url_demo + self._url_getRouteCarDynamic, data=data)
            if response.status_code == 200:
                # print(response.text)
                return response.text
            else:
                print('获取失败: ', response.status_code)
                print(response.text)
                raise CustomError(
                    sys._getframe().f_code.co_name + 'code {}, {}'.format(response.status_code, response.text))
                return None
        except Exception as e:
            print('请求出错:', e.args)
            raise e

    def parse_data(self, text):
        data = json.loads(text)
        if data and 'data' in data.keys():
            items = data.get('data')
            for item in items:
                yield item

    def save2DB(self, item, Table=None):
        if Table and db[Table].insert(item):
            print('保存到DB成功,', item)
            return True
        if Table == None:
            print('请输出集合名称!')
        return False

    def saveRouteList(self):
        routeList = []
        routeListSet = []
        for item in self.queryRouteList():
            # print(item)
            if item:
                if not item in routeList:
                    self._routeList.append(item['routeSeq'])
                    routeListSet.append(item)
                routeList.append(item)

        routeList.sort(key=lambda x: x['routeSeq'])
        routeListSet.sort(key=lambda x: x['routeSeq'])

        self.save2JSON('routeList', routeList)
        self.save2JSON('routeListSet', routeListSet)

    def setRouteList(self):
        for item in self.queryRouteList():
            if item:
                if not item['routeSeq'] in self._routeList:
                    self._routeList.append(item['routeSeq'])

    def saveBusSchedule(self):
        # if not self._routeList:
        #     self.setRouteList()
        # busScheduleDict = {i:[] for i in self._routeList}
        # busScheduleOtherDict = {}
        busScheduleDict = {}
        for item in self.queryBusSchedule():
            if item['routeSeq'] in busScheduleDict:
                busScheduleDict[item['routeSeq']].append(item)
                # 只考虑在routelist里有的车子，其他的不保存
            else:
                # 还是另外保存起来吧
                # if item['routeSeq'] in busScheduleOtherDict:
                #     busScheduleOtherDict[item['routeSeq']].append(item)
                # else:
                busScheduleDict[item['routeSeq']] = []
                busScheduleDict[item['routeSeq']].append(item)

        self.save2JSON('busSchedule', busScheduleDict)
        # self.save2JSON('busScheduleOther',busScheduleOtherDict)

    def saveBusScheduleCHN(self):
        busScheduleDict = {}
        for item in self.queryBusSchedule():
            if item['routeName'] in busScheduleDict:
                busScheduleDict[item['routeName']].append(item)
            else:
                busScheduleDict[item['routeName']] = []
                busScheduleDict[item['routeName']].append(item)

        self.save2JSON('busScheduleCHN', busScheduleDict)

    def saveRouteStationList(self):
        routeStationList = {}

        # 以名字为key
        # with open('busScheduleCHN' + str(date.today()) + '.json', 'r', encoding='utf-8') as f:
        #     a = f.read()
        #     a = json.loads(a)

        # 以序号为key
        with open('data\\' + 'busSchedule\\' + 'busSchedule' + str(date.today()) + '.json', 'r', encoding='utf-8') as f:
            a = f.read()
            a = json.loads(a)

        for k, v in a.items():

            single = {0: [], 1: []}
            for item in self.queryRouteStationList(v[-1]['routeSeq']):
                if item['type'] == 0:
                    single[0].append(item)
                else:
                    single[1].append(item)
            routeStationList[k] = single

        self.save2JSON('routeStationList', routeStationList)

    def saveRouteStationTime(self):
        routeStationTime = {}
        for item in self.queryRouteStationTime():
            if item['routeSeq'] in routeStationTime:
                if item['type'] == 0:
                    if item['routeCode'] in routeStationTime[item['routeSeq']][0]:
                        routeStationTime[item['routeSeq']][0][item['routeCode']].append(item)
                    else:
                        routeStationTime[item['routeSeq']][0][item['routeCode']] = []
                        routeStationTime[item['routeSeq']][0][item['routeCode']].append(item)
            else:
                routeStationTime[item['routeSeq']] = {0: {}, 1: {}}
                if item['type'] == 0:
                    if item['routeCode'] in routeStationTime[item['routeSeq']][0]:
                        routeStationTime[item['routeSeq']][0][item['routeCode']].append(item)
                    else:
                        routeStationTime[item['routeSeq']][0][item['routeCode']] = []
                        routeStationTime[item['routeSeq']][0][item['routeCode']].append(item)

        for item in self.queryRouteStationTime(type=1):
            if item['routeSeq'] in routeStationTime:
                if item['type'] == 1:
                    if item['routeCode'] in routeStationTime[item['routeSeq']][1]:
                        routeStationTime[item['routeSeq']][1][item['routeCode']].append(item)
                    else:
                        routeStationTime[item['routeSeq']][1][item['routeCode']] = []
                        routeStationTime[item['routeSeq']][1][item['routeCode']].append(item)
            else:
                routeStationTime[item['routeSeq']] = {0: {}, 1: {}}
                if item['type'] == 1:
                    if item['routeCode'] in routeStationTime[item['routeSeq']][1]:
                        routeStationTime[item['routeSeq']][1][item['routeCode']].append(item)
                    else:
                        routeStationTime[item['routeSeq']][1][item['routeCode']] = []
                        routeStationTime[item['routeSeq']][1][item['routeCode']].append(item)

        self.save2JSON('routeStationTime', routeStationTime)

    def saveAll(self):
        for func in self._save_func:
            try:
                func()
            except Exception as e:
                print(e.args)
                print('{}失败'.format(func.__name__))
                raise e

    def save2JSON(self, folder_name, document):
        assert type(folder_name) is str
        if type(document) == list or type(document) == dict:
            documentJSON = json.dumps(document, ensure_ascii=False, indent=4)
            documentJSONBYTES = documentJSON.encode('utf-8')
        try:
            with open('data/' + folder_name + '/' + folder_name + str(date.today()) + '.json', 'wb') as f:
                f.write(documentJSONBYTES)
        except Exception as e:
            print('保存',folder_name,'失败')
            raise CustomError('保存',folder_name,'失败')

# yidong = QueryYidong()
# print(yidong._queryRouteStationTime())

# if __name__ == '__main__':
#     yidong = QueryYidong()
#
#     yidong.saveRouteList()

# routeSeqXL = []
# for item in yidong.queryRouteList():
#     if item:
#         if not item['routeSeq'] in routeSeqXL:
#             routeSeqXL.append(item['routeSeq'])
# routeSeqXL.sort()
# print('线路routeSeq:{},共{}条线路'.format(routeSeqXL, len(routeSeqXL)))
#
# routeSeqPB = []
# for item in yidong.queryBusSchedule():
#     if item:
#         if not item['routeSeq'] in routeSeqPB:
#             routeSeqPB.append(item['routeSeq'])
# routeSeqPB.sort()
# print('排班routeSeq:{},共{}条线路'.format(routeSeqPB, len(routeSeqPB)))
#
# routeSeqSKB = []
# for item in yidong.queryRouteStationTime():
#     if not item['routeSeq'] in routeSeqSKB:
#         routeSeqSKB.append(item['routeSeq'])
# routeSeqSKB.sort()
# print('时刻表routeSeq:{},共{}条线路'.format(routeSeqSKB,len(routeSeqSKB)))

# single = {0:[],1:[]}
# for item in yidong.queryRouteStationList(21):
#     if item['type'] == 0:
#         single[0].append(item)
#     else:
#         single[1].append(item)
#
#
#
# for k,v in single.items():
#     print('type:{}'.format(k))
#     for item in v:
#         print(item)

# yidong.saveBusScheduleCHN()

# with open('busScheduleCHN' + str(date.today()) + '.json', 'r', encoding='utf-8') as f:
#     a = f.read()
#     print(a)
#     a = json.loads(a)
#     print(len(a))

# busScheduleDict = {}
# for item in yidong.queryBusSchedule():
#     print(item)
#
# print(busScheduleDict)


# yidong.saveRouteList()

# routeList = []
# routeListSet = []
# # 首先，是查看线路
# for item in yidong.queryRouteList():
#     # print(item)
#     if item:
#         if not item in routeList:
#             routeListSet.append(item)
#         routeList.append(item)
#
#
# print('routeList num: {}'.format(len(routeList)))
# print('routeListSet num: {}'.format(len(routeListSet)))
#
# routeList.sort(key=lambda x:x['routeSeq'])
# routeListSet.sort(key=lambda x:x['routeSeq'])
#
# routeListJson = json.dumps(routeList,ensure_ascii=False,indent=4)
# routeListSetJson = json.dumps(list(routeListSet),ensure_ascii=False,indent=4)
#
# with open('routeList.json','wb') as f:
#     f.write(routeListJson.encode('utf-8'))
#
# with open('routeListSet.json','wb') as f:
#     f.write(routeListSetJson.encode('utf-8'))


# 排班信息
# table = 'BusSchedule' + str(date.today())
#
#
# route = []
# for item in yidong.queryBusSchedule():
#     if item['routeSeq'] == 21 and item['type'] == 0:
#         # test = OrderedDict()
#         # test['routeName']=item['routeName']
#         # test['startStationName'] = item['startStationName']
#         # test['departureTime'] = item['departureTime']
#         # test['endStation'] = item['endStation']
#         # test['arrivalTime'] = item['arrivalTime']
#         # test['type'] = item['type']
#         route.append(item)
#
#         # print('线路名称:{0}, 起点:{1}, 发车时间:{2}, 终点:{3}, 到达时间:{4}, 上/下行:{5}' \
#         #       .format(item['routeName'], item['startStationName'], item['departureTime'], item['endStation'],
#         #               item['arrivalTime'], item['type']))
#
#
# route.sort(key=lambda x:x['departureTime'])
# for item in route:
#     print(item)
# #
# for item in yidong.queryRouteStationTime(routeSeq=21,routeCode='HQ0625'):
#     print(item)
#
#
# for item in yidong.queryRouteList():
#     if item and item['routeSeq'] == 21:
#         print(item)
#
# for item in yidong.queryRouteStationList(21):
#     if item['type'] == 0:
#         print(item)
