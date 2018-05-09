
# coding: utf-8

# ### 驿动新接口处理
# 驿动接口文档  
# http://apidoc.fzkuliya.com/api/tj/index.html#api-route-huoquxianlushikebiao  

# In[1]:


import time
from datetime import datetime
import hashlib
import uuid
import requests as re
# import xlwt


# In[82]:


key = '12Xso1XU9sd3SDJ8s0kcsxops9'
nonceStr = str(uuid.uuid1())
timestamp = str(int(time.time()))

url_1 = 'http://ydwl.ev-shanghai.com/ydwl-app' # 正式环境地址
url_2 = 'http://ydwl.fzkuliya.com/ydwl-app'    # 测试环境地址

url_RouteList = '/tj/route/queryRouteList.jhtml'               # 获取线路
url_RouteStationList = '/tj/route/queryRouteStationList.jhtml' # 获取站点信息
url_StationTime = '/tj/routeStationTime/queryRouteStationTime.jhtml'  # 到站时间信息
url_BusSchedule = '/tj/route/queryBusSchedule.jhtml'           # 排班信息
url_Car = '/tj/route/getRouteCarDynamic.jhtml'


# In[72]:


def getRouteStationList(routeSeq=None):
    routeSeq = routeSeq
    signParam = 'nonceStr=' + nonceStr + '&routeSeq=' + str(routeSeq) + '&timestamp=' + timestamp + '&key=' + key
    signValue = hashlib.md5(signParam.encode('utf-8')).hexdigest().upper()

    form_data =  {
            "nonceStr" : nonceStr,
            "timestamp":timestamp,
            "sign":signValue,
            "routeSeq":routeSeq
                  }
    
    html = re.post(url=url, data=form_data)
    dataset = html.json()
    dataset = dataset['data']
    return dataset

def getRouteStationTime(routeSeq=None, _type=0, routeCode=None):
    routeSeq = routeSeq
    signParam = 'nonceStr=' + nonceStr  + '&routeCode=' + routeCode + '&routeSeq=' + str(routeSeq) +  '&timestamp=' + timestamp + '&type=' + str(_type) + '&key=' + key
    signValue = hashlib.md5(signParam.encode('utf-8')).hexdigest().upper()

    form_data =  {
            "nonceStr" : nonceStr,
            "timestamp":timestamp,
            "sign":signValue,
            "routeSeq":routeSeq,
            "type": _type,
            "routeCode":routeCode
                  }
    
    html = re.post(url=url, data=form_data)
    dataset = html.json()
    dataset = dataset['data']
    return dataset

def getBusSchedule(routeSeq=None, scheduleDate=None):
    url = url_2 + url_BusSchedule
    routeSeq = routeSeq
    signParam = 'nonceStr=' + nonceStr + '&routeSeq=' + str(routeSeq) + '&scheduleDate=' + str(scheduleDate) +'&timestamp=' + timestamp + '&key=' + key
    signValue = hashlib.md5(signParam.encode('utf-8')).hexdigest().upper()

    form_data =  {
            "nonceStr" : nonceStr,
            "timestamp":timestamp,
            "sign":signValue,
            "routeSeq":routeSeq,
            "scheduleDate":scheduleDate,
            #"routeCode":routeCode
                  }
    
    html = re.post(url=url, data=form_data)
    # dataset = html.json()
    # dataset = dataset['data']
    # return dataset
    return html.text

# # In[69]:
#
#
# url = url_2 + url_RouteStationList
# getRouteStationList(21)
#
#
# # In[83]:
#
#
# url = url_2 + url_StationTime
# # url = 'http://ydwl.fzkuliya.com/ydwl-app/tj/routeStationTime/queryRouteStationTime.jhtml'
# getRouteStationTime(21, 0, 'HQ1255')
#
#
# # In[59]:



print(getBusSchedule(21, '2018-03-10'))

