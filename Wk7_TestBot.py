#!/usr/bin/env python
# -*- coding:utf-8 -*-

import discord
import json

from TeaBot_3 import runLoki

from ArticutAPI import Articut
with open("/Users/stephanie/Documents/Droidtown/Unit 4/account_info.py", encoding="utf-8") as f:
    userinfoDICT = json.loads(f.read())
articut = Articut(username=userinfoDICT["username"], apikey=userinfoDICT["apikey"])

with open("account.info", encoding="utf-8") as f:
    accountDICT = json.loads(f.read())

class BotClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {} with id {}'.format(self.user, self.user.id))

    async def on_message(self, message):
        # Don't respond to bot itself. Or it would create a non-stop loop.
        # 如果訊息來自 bot 自己，就不要處理，直接回覆 None。不然會 Bot 會自問自答個不停。
        if message.author == self.user:
            return None

        print("到到來自 {} 的訊息".format(message.author))
        print("訊息內容是 {}。".format(message.content))
        if self.user.mentioned_in(message):
            print("本 bot 被叫到了！")
            msg = message.content.replace("<@!{}> ".format(self.user.id), "")
            if msg == 'ping':
                await message.reply('pong')
            elif msg == "<@!{}>".format(self.user.id):
                await message.reply('找我不在')
            elif msg == 'ping ping':
                await message.reply('pong pong')
            elif msg == '隨便':
                await message.reply('出現選擇困難，自爆程序五秒後啟動 :c')
            else:
                #從這裡開始接上 NLU 模型
                responseSTR = "我是預設的回應字串…你會看到我這串字，肯定是出了什麼錯！"
                inputLIST = [msg]
                filterLIST = []
                resultDICT = runLoki(inputLIST, filterLIST)
                print("Result => {}".format(resultDICT))
            
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
            
                
                responsesSTR = "您點的總共是:"
                for k in range(len(resultDICT["amount"])):
                    responsesSTR = responsesSTR + "{} x {} ( {} ; {} )".format(resultDICT["item"][k], resultDICT["amount"][k], resultDICT["ice"], resultDICT["sugar"] )
                
                await message.reply(responsesSTR)

if __name__ == "__main__":
    client = BotClient()
    client.run(accountDICT["discord_token"])