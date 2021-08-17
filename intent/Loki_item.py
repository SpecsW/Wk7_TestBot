#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for item

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_item = True
userDefinedDICT = {"ice": ["正常", "去冰", "不冰", "不要冰塊", "不加冰塊", "不加", "不要加冰塊", "少冰", "半冰", "冰塊不要太多", "微", "正常冰", "微冰", "冰", "溫", "溫的", "溫飲", "熱飲", "熱", "熱的", "常溫", "不要冰的", "常溫", "不要冰"], "both": ["都少", "甜度冰塊都少", "都一半", "甜度冰塊都一半", "都正常", "甜度冰塊都正常", "甜度冰塊正常", "各"], "sugar": ["半糖", "半", "一半", "少糖", "不要太甜", "微糖", "微", "一點", "一點點", "無糖", "無", "不要甜", "不糖", "不加糖", "不加", "不要糖", "全糖"], "whatever": ["都可以", "隨便"], "原鄉四季": ["原鄉", "四季", "原鄉四", "四季原鄉"], "極品菁茶": ["極品", "菁茶", "極品菁", "菁茶極品"], "特級綠茶": ["特級", "綠茶", "特綠", "特級綠", "綠茶特級"], "特選普洱": ["特選", "普洱", "特選普", "普洱特選", "普洱茶"], "翡翠烏龍": ["翡翠", "烏龍", "翡烏", "翡龍", "翡翠烏", "烏龍翡翠"], "錫蘭紅茶": ["錫蘭", "紅茶", "錫紅", "錫蘭紅", "紅茶錫蘭", "冰紅茶"], "烏龍綠茶": ["烏龍", "綠茶", "烏綠", "烏龍綠", "綠茶烏龍"], "嚴選高山茶": ["嚴選", "高山茶", "嚴選高山", "山茶", "山茶嚴選", "嚴選高"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_item:
        print("[item] {} ===> {}".format(inputSTR, utterance))
        
def getItem(argsLIST):
    #小心全名！！
    for a in argsLIST:
        if a in userDefinedDICT["原鄉四季"] or a == "原鄉四季":
            return argsLIST.index(a)
        elif a in userDefinedDICT["極品菁茶"] or a == "極品菁茶":
            return argsLIST.index(a)
        elif a in userDefinedDICT["特級綠茶"] or a == "特級綠茶":
            return argsLIST.index(a)
        elif a in userDefinedDICT["特選普洱"] or a == "特選普洱":
            return argsLIST.index(a)
        elif a in userDefinedDICT["翡翠烏龍"] or a == "翡翠烏龍":
            return argsLIST.index(a)
        elif a in userDefinedDICT["錫蘭紅茶"] or a == "錫蘭紅茶":
            return argsLIST.index(a)
        elif a in userDefinedDICT["烏龍綠茶"] or a == "烏龍綠茶":
            return argsLIST.index(a)
        elif a in userDefinedDICT["嚴選高山茶"] or a == "嚴選高山茶":
            return argsLIST.index(a)
        elif a in userDefinedDICT["whatever"]:
            return "出現選擇困難, 自爆程序啟動..."
        else:
            pass
    return None

def getFullName(argsSTR):
    for k in userDefinedDICT.keys():
        if argsSTR in userDefinedDICT[k]:
            return k
        elif argsSTR == k:#argsSTR 就是全名的時候
            return argsSTR
        else:
            pass
    return None

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    resultDICT["item"] = []
        
    if utterance == "[一杯][去冰][原鄉]":
        checkResult = getItem(args)
        if checkResult != None:
            resultDICT["item"].append(args[checkResult])

    if utterance == "[一杯][翡翠烏龍]和[原鄉四季]":
        resultDICT["item"].append(getFullName(args[1]))
        resultDICT["item"].append(getFullName(args[2]))

    if utterance == "[兩杯][熱的][特選普洱]，[甜度冰塊正常]":
        checkResult = getItem(args)
        if checkResult != None:
            resultDICT["item"].append(args[checkResult])
            
    if utterance == "[去冰][烏龍][一杯]":
        checkResult = getItem(args)
        if checkResult != None:
            resultDICT["item"].append(args[checkResult])

    if utterance == "[嚴選][微][微]":
        checkResult = getItem(args)
        if checkResult != None:
            resultDICT["item"].append(getFullName(args[checkResult]))

    if utterance == "[我]要[錫蘭]，[無糖][不要冰塊]":
        checkResult = getItem(args)
        if checkResult != None:
            resultDICT["item"].append(args[checkResult])

    if utterance == "[烏龍][不要冰]":
        checkResult = getItem(args)
        if checkResult != None:
            resultDICT["item"].append(args[checkResult])

    if utterance == "[烏龍][正常][一杯], [紅茶][一杯][不糖][去冰], [一杯][特級][少糖][微冰]":
        resultDICT["item"].append(args[0])
        resultDICT["item"].append(args[3])
        resultDICT["item"].append(args[8])

    if utterance == "[翡翠][三杯]糖冰[都一半]":
        checkResult = getItem(args)
        if checkResult != None:
            resultDICT["item"].append(args[checkResult])

    if utterance == "[菁茶][兩杯]，[一杯][半糖][少冰]，[一杯][全糖][正常冰]":
        checkResult = getItem(args)
        if checkResult != None:
            resultDICT["item"].append(args[checkResult])

    if utterance == "[一杯][烏龍綠][不冰][少糖]":
        checkResult = getItem(args)
        if checkResult != None:
            resultDICT["item"].append(args[checkResult])

    return resultDICT