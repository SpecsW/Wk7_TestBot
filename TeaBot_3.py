#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki 2.0 Template For Python3

    [URL] https://api.droidtown.co/Loki/BulkAPI/

    Request:
        {
            "username": "your_username",
            "input_list": ["your_input_1", "your_input_2"],
            "loki_key": "your_loki_key",
            "filter_list": ["intent_filter_list"] # optional
        }

    Response:
        {
            "status": True,
            "msg": "Success!",
            "version": "v223",
            "word_count_balance": 2000,
            "result_list": [
                {
                    "status": True,
                    "msg": "Success!",
                    "results": [
                        {
                            "intent": "intentName",
                            "pattern": "matchPattern",
                            "utterance": "matchUtterance",
                            "argument": ["arg1", "arg2", ... "argN"]
                        },
                        ...
                    ]
                },
                {
                    "status": False,
                    "msg": "No Match Intent!"
                }
            ]
        }
"""

from requests import post
from requests import codes
import math
try:
    from intent import Loki_sugar
    from intent import Loki_ice
    from intent import Loki_item
    from intent import Loki_temperature
    from intent import Loki_amount
except:
    from .intent import Loki_sugar
    from .intent import Loki_ice
    from .intent import Loki_item
    from .intent import Loki_temperature
    from .intent import Loki_amount


LOKI_URL = "https://api.droidtown.co/Loki/BulkAPI/"
USERNAME = "s.stephanie.chen@gmail.com"
LOKI_KEY = "&@3%as2X^JuvEJ6YmKXlw%p+IwNyprl"
# 意圖過濾器說明
# INTENT_FILTER = []        => 比對全部的意圖 (預設)
# INTENT_FILTER = [intentN] => 僅比對 INTENT_FILTER 內的意圖
INTENT_FILTER = []

class LokiResult():
    status = False
    message = ""
    version = ""
    balance = -1
    lokiResultLIST = []

    def __init__(self, inputLIST, filterLIST):
        self.status = False
        self.message = ""
        self.version = ""
        self.balance = -1
        self.lokiResultLIST = []
        # filterLIST 空的就採用預設的 INTENT_FILTER
        if filterLIST == []:
            filterLIST = INTENT_FILTER

        try:
            result = post(LOKI_URL, json={
                "username": USERNAME,
                "input_list": inputLIST,
                "loki_key": LOKI_KEY,
                "filter_list": filterLIST
            })

            if result.status_code == codes.ok:
                result = result.json()
                self.status = result["status"]
                self.message = result["msg"]
                if result["status"]:
                    self.version = result["version"]
                    self.balance = result["word_count_balance"]
                    self.lokiResultLIST = result["result_list"]
            else:
                self.message = "Connect failed."
        except Exception as e:
            self.message = str(e)

    def getStatus(self):
        return self.status

    def getMessage(self):
        return self.message

    def getVersion(self):
        return self.version

    def getBalance(self):
        return self.balance

    def getLokiStatus(self, index):
        rst = False
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["status"]
        return rst

    def getLokiMessage(self, index):
        rst = ""
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["msg"]
        return rst

    def getLokiLen(self, index):
        rst = 0
        if index < len(self.lokiResultLIST):
            if self.lokiResultLIST[index]["status"]:
                rst = len(self.lokiResultLIST[index]["results"])
        return rst

    def getLokiResult(self, index, resultIndex):
        lokiResultDICT = None
        if resultIndex < self.getLokiLen(index):
            lokiResultDICT = self.lokiResultLIST[index]["results"][resultIndex]
        return lokiResultDICT

    def getIntent(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["intent"]
        return rst

    def getPattern(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["pattern"]
        return rst

    def getUtterance(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["utterance"]
        return rst

    def getArgs(self, index, resultIndex):
        rst = []
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["argument"]
        return rst

def runLoki(inputLIST, filterLIST=[]):
    resultDICT = {}
    lokiRst = LokiResult(inputLIST, filterLIST)
    if lokiRst.getStatus():
        for index, key in enumerate(inputLIST):
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                # sugar
                if lokiRst.getIntent(index, resultIndex) == "sugar":
                    resultDICT = Loki_sugar.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # ice
                if lokiRst.getIntent(index, resultIndex) == "ice":
                    resultDICT = Loki_ice.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # item
                if lokiRst.getIntent(index, resultIndex) == "item":
                    resultDICT = Loki_item.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # temperature
                if lokiRst.getIntent(index, resultIndex) == "temperature":
                    resultDICT = Loki_temperature.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # amount
                if lokiRst.getIntent(index, resultIndex) == "amount":
                    resultDICT = Loki_amount.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

    else:
        resultDICT = {"msg": lokiRst.getMessage()}
    return resultDICT

def testLoki(inputLIST, filterLIST):
    INPUT_LIMIT = 20
    for i in range(0, math.ceil(len(inputLIST) / INPUT_LIMIT)):
        resultDICT = runLoki(inputLIST[i*INPUT_LIMIT:(i+1)*INPUT_LIMIT], filterLIST)


if __name__ == "__main__":
    # sugar
    #print("[TEST] sugar")
    #inputLIST = ['嚴選微微','烏龍不要冰','一杯去冰原鄉','去冰烏龍一杯','一杯烏龍綠不冰少糖','翡翠三杯糖冰都一半','一杯翡翠烏龍和原鄉四季','我要錫蘭，無糖不要冰塊','兩杯熱的特選普洱，甜度冰塊正常','菁茶兩杯，一杯半糖少冰，一杯全糖正常冰','烏龍正常一杯, 紅茶一杯不糖去冰, 一杯特級少糖微冰']
    #testLoki(inputLIST, ['sugar'])
    #print("")

    # ice
    #print("[TEST] ice")
    #inputLIST = ['嚴選微微','烏龍不要冰','一杯去冰原鄉','去冰烏龍一杯','一杯烏龍綠不冰少糖','翡翠三杯糖冰都一半','一杯翡翠烏龍和原鄉四季','我要錫蘭，無糖不要冰塊','兩杯熱的特選普洱，甜度冰塊正常','菁茶兩杯，一杯半糖少冰，一杯全糖正常冰','烏龍正常一杯, 紅茶一杯不糖去冰, 一杯特級少糖微冰']
    #testLoki(inputLIST, ['ice'])
    #print("")

    # item
    #print("[TEST] item")
    #inputLIST = ['嚴選微微','烏龍不要冰','一杯去冰原鄉','去冰烏龍一杯','一杯烏龍綠不冰少糖','翡翠三杯糖冰都一半','一杯翡翠烏龍和原鄉四季','我要錫蘭，無糖不要冰塊','兩杯熱的特選普洱，甜度冰塊正常','菁茶兩杯，一杯半糖少冰，一杯全糖正常冰','烏龍正常一杯, 紅茶一杯不糖去冰, 一杯特級少糖微冰']
    #testLoki(inputLIST, ['item'])
    #print("")

    # temperature
    #print("[TEST] temperature")
    #inputLIST = ['嚴選微微','烏龍不要冰','一杯去冰原鄉','去冰烏龍一杯','一杯烏龍綠不冰少糖','翡翠三杯糖冰都一半','一杯翡翠烏龍和原鄉四季','我要錫蘭，無糖不要冰塊','兩杯熱的特選普洱，甜度冰塊正常','菁茶兩杯，一杯半糖少冰，一杯全糖正常冰','烏龍正常一杯, 紅茶一杯不糖去冰, 一杯特級少糖微冰']
    #testLoki(inputLIST, ['temperature'])
    #print("")

    # amount
    #print("[TEST] amount")
    #inputLIST = ['嚴選微微','烏龍不要冰','一杯去冰原鄉','去冰烏龍一杯','一杯烏龍綠不冰少糖','翡翠三杯糖冰都一半','一杯翡翠烏龍和原鄉四季','我要錫蘭，無糖不要冰塊','兩杯熱的特選普洱，甜度冰塊正常','菁茶兩杯，一杯半糖少冰，一杯全糖正常冰','烏龍正常一杯, 紅茶一杯不糖去冰, 一杯特級少糖微冰']
    #testLoki(inputLIST, ['amount'])
    #print("")

    # 輸入其它句子試看看
    inputLIST = ["普洱微微"]
    #inputLIST = ["我要菁茶，半糖不要冰塊"]
    #inputLIST = ["原鄉兩杯，一杯半糖少冰，一杯全糖正常冰"]
    #inputLIST = ["冰紅茶不要冰"]
    #inputLIST = ["兩杯熱的錫蘭紅茶，甜度冰塊正常"]
    #inputLIST = ["一杯錫蘭紅茶和烏龍綠茶"]
    
    filterLIST = []
    resultDICT = runLoki(inputLIST, filterLIST)
    print("Result => {}".format(resultDICT))
    
    import json
    from ArticutAPI import Articut
    with open("/Users/stephanie/Documents/Droidtown/Unit 4/account_info.py", encoding="utf-8") as f:
        userinfoDICT = json.loads(f.read())
    articut = Articut(username=userinfoDICT["username"], apikey=userinfoDICT["apikey"])

    for amt in range(0, len(resultDICT["amount"])):
        articutLv3ResultDICT = articut.parse(resultDICT["amount"][amt], level="lv3")
        amount = articutLv3ResultDICT["number"][resultDICT["amount"][amt]]
        resultDICT["amount"][amt] = amount
        

    
    if resultDICT["ice"] == []:
        if resultDICT["item"] != []:
            for i in range(len(resultDICT["item"])):
                resultDICT["ice"].append("正常")
                
        #每個item都要在ice裡面加"正常"
    
    if resultDICT["sugar"] == []:
        if resultDICT["item"] != []:
            for i in range(len(resultDICT["item"])):
                resultDICT["sugar"].append("正常")

    
    print("您點的總共是:")
    for k in range(len(resultDICT["amount"])):
        print("{} x {} ( {} ; {} )".format(resultDICT["item"][k], resultDICT["amount"][k], resultDICT["ice"], resultDICT["sugar"] ))
        

#other notes:
# 曾經有遠大的理想用 k + 1 之類的方法把糖跟冰 format 在一起, 可是試了幾種條件都滿江紅(key error, index out of range...) 所以暫時放棄