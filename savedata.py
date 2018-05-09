import json
from datetime import date
import shutil
from config import Config
import gzip

class SaveData(object):

    def __init__(self):
        self.newBusSchedule_simple = None
        self.newBusSchedule = None

    common_items_all = ['routeName', 'routeSeq', 'createTime', 'updateTime', 'scheduleDate']
    schedule_items_all = ['departureTime', 'arrivalTime', 'remark1', 'routeCodeStr', \
                          'vehicleModelName', 'vehicleNo', 'name', 'driverId', 'type', \
                          'schedulingSeq', 'id', 'authId', 'vehicleModel', 'startStationName', \
                          'endStation']

    common_items_simple = ['routeName', 'routeSeq', 'scheduleDate']
    schedule_items_simple = ['departureTime', 'arrivalTime', 'routeCodeStr', \
                             'vehicleNo', 'driverId', 'type', \
                             'startStationName', \
                             'endStation']
    station_time_items_simple = ['stationId', 'stationFlag', 'type', 'time']

    def saveYesterday(self):
        try:
            shutil.copy(Config.updateData_DIR+Config.yesterday_FILE,Config.updateData_DIR+Config.updateData_FILE)
        except Exception:
            shutil.copy(Config.updateData_DIR + Config.yesterday_FILE, Config.updateData_DIR + Config.updateData_FILE)

    def handle_busSchedule(self,busSchedule):
        ## 处理busSchedule
        for routeSeq in self.newBusSchedule_simple.keys():
            # print(routeSeq)
            for key in self.common_items_simple:
                self.newBusSchedule_simple[routeSeq][key] = busSchedule[routeSeq][0][key]

            self.newBusSchedule_simple[routeSeq]['schedule'] = []
            for item in busSchedule[routeSeq]:
                single = {}
                for key in self.schedule_items_simple:
                    single[key] = item[key]
                self.newBusSchedule_simple[routeSeq]['schedule'].append(single)

    #稍微修改routeStationList的几个Key
    #"gdId"->"MID"，"id"->"UID"，"stationName"->"name"
    def change_routeStationList(self,routeStationList):
        assert routeStationList is not None
        keys = {'gdId':'MID','id':'UID','stationName':'name'}
        for k,v in routeStationList.items():
            for _,vv in v.items():
                if vv:
                    for vvv in vv:
                        for old,new in keys.items():
                            try:
                                vvv[new] = vvv.pop(old)
                            except Exception:
                                print(Exception.args)
        return routeStationList


    def handle_routeStationList(self,routeStationList):
        routeStationList = self.change_routeStationList(routeStationList)
        ## 处理routeStationList
        for routeSeq in self.newBusSchedule_simple.keys():
            if routeSeq in routeStationList:
                self.newBusSchedule_simple[routeSeq]['routeStationList'] = routeStationList[routeSeq]
            else:
                self.newBusSchedule_simple[routeSeq]['routeStationList'] = {0: [], 1: []}
                # print(k,newBusSchedule[k]['routeStationList'])

    def handle_routeStationTime(self,routeStationTime_simple):
        ## 处理routeStationTime
        for routeSeq in self.newBusSchedule_simple.keys():
            if routeSeq in routeStationTime_simple:
                for item in self.newBusSchedule_simple[routeSeq]['schedule']:
                    item['routeStationTime'] = []
                    if item['type'] == 0:
                        try:
                            item['routeStationTime'] = routeStationTime_simple[routeSeq]["0"][item['routeCodeStr']]
                        except KeyError:
                            print('routeStationTime[{}]["0"][{}] not exists'.format(routeSeq, item['routeCodeStr']))
                            item['routeStationTime'] = []
                    else:
                        try:
                            item['routeStationTime'] = routeStationTime_simple[routeSeq]["1"][str(item['routeCodeStr'])]
                        except KeyError:
                            print('routeStationTime[{}]["1"][{}] not exists'.format(routeSeq, item['routeCodeStr']))
                            item['routeStationTime'] = []
            else:
                for item in self.newBusSchedule_simple[routeSeq]['schedule']:
                    item['routeStationTime'] = []

    def save2File(self,compress=Config.compress):
        ## 保存成文件
        if type(self.newBusSchedule_simple) == list or type(self.newBusSchedule_simple) == dict:
            #dict --> list
            newBusSchedule_list_simple = self.dict2list(self.newBusSchedule_simple)
            documentJSON = json.dumps(newBusSchedule_list_simple, ensure_ascii=False, indent=4)
            documentJSONBYTES = documentJSON.encode('utf-8')
        if not compress:
            with open(Config.updateData_DIR+Config.updateData_FILE, 'wb') as f:
                f.write(documentJSONBYTES)
        else:
            with gzip.open(Config.updateData_DIR+Config.updateData_FILE_Compress, 'wb') as f:
                f.write(documentJSONBYTES)

    #最后决定把那个给key干掉，保存成list形式
    def dict2list(self,mydict):
        mylist = []
        for k,v in mydict.items():
            mylist.append(v)
        return mylist

    def saveSimple(self):
        try:
            with open(Config.busSchedule_DIR + Config.busSchedule_FILE, 'r', encoding='utf-8') as f:
                busSchedule = json.loads(f.read())
        except FileNotFoundError:
            busSchedule = None

        try:
            with open(Config.routeStationList_DIR + Config.routeStationList_FILE, 'r', encoding='utf-8') as f:
                routeStationList = json.loads(f.read())
        except FileNotFoundError:
            routeStationList = None

        try:
            with open(Config.routeStationTime_DIR + Config.routeStationTime_FILE, 'r', encoding='utf-8') as f:
                routeStationTime = json.loads(f.read())
        except FileNotFoundError:
            routeStationTime = None

        try:
            with open(Config.routeListSet_DIR + Config.routeListSet_FILE, 'r', encoding='utf-8') as f:
                routeListSet = json.loads(f.read())
        except FileNotFoundError:
            routeListSet = None

        if routeStationTime:
            routeStationTime_simple = {k: {'0': {}, '1': {}} for k in routeStationTime}
            for routeSeq, v in routeStationTime.items():
                for ty, vv in v.items():
                    for code, schedule in vv.items():
                        single = []
                        for item in schedule:
                            sub_single = {}
                            for key in self.station_time_items_simple:
                                sub_single[key] = item[key]
                            single.append(sub_single)
                        routeStationTime_simple[routeSeq][ty][code] = single
        else:
            routeStationTime_simple = None

        key_items = None

        busSchedule_key = set([k for k in busSchedule.keys()])
        print('busSchedule_key:',busSchedule_key)
        if busSchedule_key:
            key_items = busSchedule_key

        routeListSet_key = set([str(item['routeSeq']) for item in routeListSet])
        print('routeListSet_key,',routeListSet_key)
        if routeListSet_key:
            if key_items:
                key_items = key_items&routeListSet_key
            else:
                key_items = routeListSet_key

        routeStationList_key = set([k for k in routeStationList.keys()])
        print('routeStationList_key',routeStationList_key)
        if routeStationList_key:
            if key_items:
                key_items = key_items&routeStationList_key
            else:
                key_items = routeStationList_key

        routeStationTime_key = set([k for k in routeStationTime.keys()])
        print('routeStationTime_key',routeStationTime_key)
        if routeStationTime_key:
            key_items = key_items&routeStationTime_key
        else:
            key_items = routeStationTime_key

        self.newBusSchedule_simple = {k: {} for k in
                          key_items}
        # print(key_items)



        try:
            if not busSchedule or not routeStationTime_simple or not routeStationList or not routeListSet:
                raise ValueError
            self.handle_busSchedule(busSchedule)
            self.handle_routeStationList(routeStationList)
            self.handle_routeStationTime(routeStationTime_simple)
            print('开始保存')
            self.save2File()
        except ValueError:
            raise ValueError
            print('save yesterday')
            self.saveYesterday()
        # except Exception:
        #     print('save yesterday')
        #     self.saveYesterday()




    def saveAll(self):
        with open(Config.busSchedule_DIR + Config.busSchedule_FILE, 'r', encoding='utf-8') as f:
            busSchedule = f.read()
            busSchedule = json.loads(busSchedule)

        with open(Config.routeStationList_DIR + Config.routeStationList_FILE, 'r', encoding='utf-8') as f:
            routeStationList = json.loads(f.read())

        with open(Config.routeStationTime_DIR + Config.routeStationTime_FILE, 'r', encoding='utf-8') as f:
            routeStationTime = json.loads(f.read())

        newBusSchedule = {k: {} for k in busSchedule.keys()}

        for k, v in busSchedule.items():

            for key in self.common_items_all:
                newBusSchedule[k][key] = v[0][key]

            newBusSchedule[k]['schedule'] = []
            for item in v:
                single = {}
                for key in self.schedule_items_all:
                    single[key] = item[key]
                newBusSchedule[k]['schedule'].append(single)

        for k in newBusSchedule.keys():
            if k in routeStationList:
                newBusSchedule[k]['routeStationList'] = routeStationList[k]
            else:
                newBusSchedule[k]['routeStationList'] = {0: [], 1: []}
                # print(k,newBusSchedule[k]['routeStationList'])

        for k in newBusSchedule.keys():
            if k in routeStationTime:
                print(k)
                for item in newBusSchedule[k]['schedule']:
                    if item['type'] == 0:
                        try:
                            item['routeStationTime'] = routeStationTime[k]["0"][item['routeCodeStr']]
                        except KeyError:
                            print('routeStationTime[{}]["0"][{}] not exists'.format(k, item['routeCodeStr']))
                            item['routeStationTime'] = []
                    else:
                        try:
                            item['routeStationTime'] = routeStationTime[k]["1"][str(item['routeCodeStr'])]
                        except KeyError:
                            print('routeStationTime[{}]["1"][{}] not exists'.format(k, item['routeCodeStr']))
                            item['routeStationTime'] = []
            else:
                for item in newBusSchedule[k]['schedule']:
                    item['routeStationTime'] = []

        if type(newBusSchedule) == list or type(newBusSchedule) == dict:
            documentJSON = json.dumps(newBusSchedule, ensure_ascii=False, indent=4)
            documentJSONBYTES = documentJSON.encode('utf-8')
        with open('testdata\\' + 'newBusSchedule' + str(date.today()) + '.json', 'wb') as f:
            f.write(documentJSONBYTES)

