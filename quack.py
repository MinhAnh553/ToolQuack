import requests
import asyncio
import random
import os
import sys
import base64
import datetime
from dataclasses import dataclass,field,fields
from collections import defaultdict
from typing import Callable, Dict,Any
from requests import Response
from functools import wraps
# import PyQt6.QtCore


#======================================================
@dataclass
class Language():
    Action_Retry: str=""
    Acion_Exit: str=""
    #API
    API_tokenNotFound: str=""
    API_connectionError: str=""
    API_LoginFailed: str=""
    API_LoginSuccess: str=""
    #UI
    UI_SelectInputMode: str=""
    UI_InputNumberAcc: str=""
    UI_InputToken: str=""
    UI_InputRareBadDuck: str=""
    UI_InputIsHatch: str=""
    UI_InputIsAutoRemoveBadDuck: str=""
    UI_InputTypeWillHatch: str=""
    UI_LastUpdate:str=""
    UI_MaxDuckNotHatch:str=""
    #In Game
    Game_Balance:str=""
    Game_Egg_Collected:str=""
    Game_Egg_Hatching:str=""
    Game_Duck_Collected:str=""
    Game_Duck_Removed:str=""
    Game_Duck_Lazy:str=""
    Game_GoldenEgg_NextTime:str=""
    Game_GoldenEgg_Collected:str=""
    Game_GoldenEgg_Value:str=""
#======================================================

#======================================================
#VietNamese
LanguagePack = [
    #Vietnamese
    Language(
        Action_Retry="Dang Thu Lai",
        Acion_Exit="Dang Thoat",
        API_tokenNotFound="Khong Tim Thay Token",
        API_connectionError="Loi Ket Noi",
        API_LoginFailed="Dang Nhap That Bai",
        API_LoginSuccess="Dang Nhap Thanh Cong",
        UI_SelectInputMode="Chon Che Do: \n[0] Nhap Token | [1] Tai Tu File(token.txt): ",
        UI_InputNumberAcc="Nhap So Luong Tai Khoan",
        UI_InputToken="Nhap Token Cho Tai Khoan",
        UI_InputRareBadDuck="Chat Luong Vit Duoi Muc Nay Se Dem Di Lam Cari (3-13):",
        UI_InputIsHatch="Tu Dong Ap Trung [0] Tat | [1] Bat",
        UI_InputIsAutoRemoveBadDuck="Auto Lam 'Cari Vit' De Ap Vit Moi [0] Tat | [1] Bat",
        UI_InputTypeWillHatch="Chat Luong Trung Se Duoc Ap No (3-13): ",
        UI_LastUpdate="Cap Nhat Lan Cuoi Luc: ",
        UI_MaxDuckNotHatch="Day Vit Roi, Khong Bat Auto Cari/Vit Xin Hon Cai Dat, Khong The Ap",
        Game_Balance="So Du",
        Game_Egg_Collected="Da Lum",
        Game_Egg_Hatching="Dang Ap",
        Game_Duck_Collected="Vit Da No, ID ",
        Game_Duck_Removed="Dang Lam CARI Be Vit",
        Game_Duck_Lazy="Cho Vit De",
        Game_GoldenEgg_NextTime = "Nhung Lau Bach Tuoc Vao Luc: ",
        Game_GoldenEgg_Collected = "Da Lum Duoc ",
        Game_GoldenEgg_Value = "Vit Vang Dang Co Gia Tri : "
        ),

    #English
    Language(
        Action_Retry="Retrying...",
        Acion_Exit="Exiting...",
        API_tokenNotFound="No token found",
        API_connectionError="Connection error",
        API_LoginFailed="Login failed",
        API_LoginSuccess="Login success",
        UI_SelectInputMode="Select Mode: \n[0] Input Token | [1] Load From File(token.txt): ",
        UI_InputNumberAcc="Enter the number of accounts: ",
        UI_InputToken="Enter token of Account ",
        UI_InputRareBadDuck="Enter the number of rare bad duck(min 3): ",
        UI_InputIsHatch="Auto Hatch [0] OFF | [1] ON",
        UI_InputIsAutoRemoveBadDuck="Auto Remove Bad Duck For Hatching [0] OFF | [1] ON",
        UI_InputTypeWillHatch="Type Of Egg will Hatch >=: ",
        UI_LastUpdate="Last Update: ",
        UI_MaxDuckNotHatch="Duck is full, Auto Remove Bad Duck is OFF or Lowest, Cannot Hatch",
        Game_Balance="Balance",
        Game_Egg_Collected="Collected Egg",
        Game_Egg_Hatching="Hatching Egg",
        Game_Duck_Collected="Collected Duck",
        Game_Duck_Removed="Removed Bad Duck",
        Game_Duck_Lazy="Waiting duck",
        Game_GoldenEgg_NextTime = "Next Golden Egg Time: ",
        Game_GoldenEgg_Collected = "Collected : ",
        Game_GoldenEgg_Value = "Golden Egg Value: "
        )
]
#======================================================
Lang = LanguagePack[0]
#======================================================
def api_request_wrapper(url):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, data:Any=None):
            isPOST = data is not None
            response =  await self.APIRequest(url=url,isPOST=isPOST, data=data, token=self.token,contentType = "application/x-www-form-urlencoded")
            return response
        return wrapper
    return decorator 
@dataclass
class API():
    URL:str = "https://api.quackquack.games/"
    token:str=""

    async def APIRequest(self,
                         url:str, 
                         token: str = "", 
                         contentType: str = "application/x-www-form-urlencoded",
                         isPOST: bool = False, 
                         data: Any = None,
                         isUseJson: bool = True):
        url = self.URL + url
        #Check Token is valid
        response = None
        if token == "":
            print(Lang.API_tokenNotFound)
            return None
        HEADER = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,vi;q=0.8",
            "authorization": f"Bearer {self.token}",
            "content-type": contentType,
            # ... (other headers - update if needed)
        }
        try:
            response = await asyncio.to_thread(requests.post if isPOST else requests.get,
                                                url=url, 
                                                headers=HEADER, 
                                                data=data)
            return response
        except:
            return None
    # POST removeDuck,collectEgg,collectDuck,hatchEgg,collectReward
    def setToken(self, token:str):
        self.token = token
    @api_request_wrapper("balance/get")
    async def getBalance(self):
        pass
    @api_request_wrapper("nest/list")
    async def getInfo(self):
        pass
    @api_request_wrapper("nest/lay-egg")
    async def getLayEgg(self):
        pass
    @api_request_wrapper("nest/max-duck")
    async def getMaxDucks(self):
        pass
    @api_request_wrapper("golden-duck/info")
    async def getNextTimeGoldenDuck(self):
        pass
    @api_request_wrapper("golden-duck/reward")
    async def getReward(self):
        pass
    @api_request_wrapper("golden-duck/claim")
    async def collectGoldenDuck(self,data:Any=None):
        pass
    @api_request_wrapper("nest/hatch")
    async def hatchEgg(self,data:Any=None):
        pass
    @api_request_wrapper("nest/collect-duck")
    async def collectDuck(self,data:Any=None):
        pass
    @api_request_wrapper("nest/collect")
    async def collectEgg(self,data:Any=None):
        pass
    @api_request_wrapper(url="duck/remove")
    async def removeDuck(self,data:Any=None):
        pass
#======================================================

#======================================================
ITEM_TYPE = ["None","Common","Common","UnCommon","UnCommon","Rare","Rare","Epic","Epic","Legendary","Legendary","Mythic","Mythic","Eternal"]
SYMBOL_TOKEN = ["","TON","PET","EGG","TRU"]
#======================================================

#======================================================
@dataclass
class GameConfig():
    numTypeWillHatch: int = 3 #Number of types of egg will be hatched
    numRareBadDuck:int = 3 #Total rare(or lowest) of bad ducks will be remove if $isAutoRemoveBadDuck = True
    isAutoRemoveBadDuck: bool = True
    isAutoHatching: bool = True
CONFIG = GameConfig()
#======================================================

#======================================================
@dataclass

@dataclass
class Egg():
    id: int = -1
    status: int = -1
    egg_config_id: int = -1
    type_egg: int = -1
    finish_time: int = -1
    remain_time: int = -1
    updated_time: int = -1
@dataclass
class Duck():
    id: int =-1
    status: int =-1
    total_rare: int =-1
    last_active_time: int =-1
#======================================================
@dataclass
class TIME():
    @staticmethod
    def getTimeNow():
        return int(datetime.datetime.now().timestamp()*1000)
    @staticmethod
    def getTimeStr(time:int):
        if time ==0:
            return ""
        return datetime.datetime.fromtimestamp(time/1000).strftime('%H:%M:%S')

@dataclass
class LOG():
    COLLECT_EGG:int = 1
    GOLDEN_DUCK:int = 2
    COLLECT_DUCK:int = 3
    INFO:int = 4
    ERROR:int =5
    BALANCE:int = 6

@dataclass
class Log():
    id:int =0
    lastTime:int=0
    nextTime:int=0
    data:str=""
    counter:int=0

    def getTimeStr(self,isLastTime:bool=False):
        time = self.lastTime if isLastTime else self.nextTime
        if time ==0:
            return ""
        return TIME.getTimeStr(time)
    def setNextTime(self,nextTime:int):
        self.nextTime = nextTime
    def setData(self,data:str):
        if data:
            self.data = data
            self.lastTime = TIME.getTimeNow()
    def addCouter(self,numAdd:int=1):
        self.counter= self.counter+numAdd
    def subCouter(self,numSub:int=1):
        if self >0:
            self.counter = self.counter - numSub
    def resetCouter(self):
        self.counter=0

#======================================================
@dataclass
class Account():
    token: str
    logsCallBack: Callable[[Any,int],None]
    userID: int = -1
    eggs: list[Egg] = field(default_factory=list)
    ducks: list[Duck] = field(default_factory=list)
    maxDuck:int = 15
    logs: str = ""
    api:API = None
    gameLogs: list[Log] = field(default_factory=lambda: [Log(id=i ) for i in range(len(fields(LOG))+ 1)])

    def addLogs(self,logType:int=LOG.COLLECT_EGG,nextTime:int=0,data:str=""):
        if logType <= len(fields(LOG)):
            self.gameLogs[logType].setData(data)
            if nextTime>0:
                self.gameLogs[logType].setNextTime(nextTime)
            if self.logsCallBack and logType !=LOG.BALANCE:
                self.logsCallBack(self.gameLogs,self.userID)
    def checkResponse(self,res:Response):
        return res and res.status_code == 200 and res.reason == "OK"
    def getData(self,res:Response):
        if self.checkResponse(res) and res.json() and res.json().get("data"):
            return res.json().get("data")
        return None
    #Check Token is valid before start
    async def Authentication(self, token:str):
        if token == "":
            self.addLogs(logType=LOG.INFO,data=f"{Lang.API_tokenNotFound} {Lang.Acion_Exit}")
            return False
        
        self.api = API(token=token)
        
        for i in range(3):
            result = await self.api.getMaxDucks()
            if self.checkResponse(result):
                self.maxDuck = self.getData(result).get("max_duck",15)
                self.addLogs(logType=LOG.INFO,data=Lang.API_LoginSuccess)
                break
            elif i==2:
                self.addLogs(logType=LOG.INFO,data=f"{Lang.API_LoginFailed}, {Lang.Action_Retry if i < 3 else Lang.Acion_Exit}")
                return False
            
        return True
    
    async def getInfo(self):
        res = await self.api.getInfo()
        data = self.getData(res=res)
        if data:
            if data.get("duck"):
                self.ducks = [Duck(**{key: item.get(key, 0) for key in Duck.__annotations__}) for item in data.get("duck", [])]
                if self.userID == -1 and data.get("duck")[0].get("user_id"):
                    self.userID = data.get("duck")[0].get("user_id")
            if data.get("nest"):
                self.eggs = [Egg(**{key: item.get(key, 0) for key in Egg.__annotations__}) for item in data.get("nest", [])]
    async def getBalance(self):
        res = await self.api.getBalance()
        if res:
            data = self.getData(res=res)
            if data and data.get("data"):
                balance = ""
                for item in data["data"]:
                    symbol = item["symbol"]
                    val = item["balance"]
                    val = float(val)
                    val = f"{val:.2f}"
                    balance = balance + f"{symbol}: {val} "
                self.addLogs(logType=LOG.BALANCE,data=balance)

    async def checkEgg(self)-> Dict: #Return status 0 is wait for Duck,1 if egg is Hatched, 2 is Collected Duck, 3 is Collected Egg, -1 is Can't Grab Duck
        results = []
        for egg in self.eggs:
            mode = -1
            result = {"id":egg.id,"status":mode,"mes":""}
            res:Response = None
            if egg.egg_config_id == None and self.ducks:
                mode = 0
                lazyDuck = min(self.ducks, key=lambda duck: duck.last_active_time or float('inf'))
                res = await self.api.getLayEgg(data={"nest_id":egg.id,"duck_id":lazyDuck.id})
            elif egg.type_egg >= CONFIG.numTypeWillHatch and CONFIG.isAutoHatching:
                if egg.finish_time == None:
                    is_full_duck = len(self.ducks) == self.maxDuck
                    if is_full_duck:
                        if not CONFIG.isAutoRemoveBadDuck:
                            self.addLogs(logType=LOG.INFO, data=Lang.UI_MaxDuckNotHatch)
                            continue

                        badDuck = min(self.ducks, key=lambda duck: duck.total_rare or float('inf'))
                        if badDuck and badDuck.total_rare <= CONFIG.numRareBadDuck:
                            restmp = await self.api.removeDuck(data=f"ducks=%7B%22ducks%22%3A%5B{badDuck.id}%5D%7D")
                            if not self.checkResponse(res=restmp):
                                continue
                            else:
                                self.addLogs(logType=LOG.INFO,data=Lang.Game_Duck_Removed + f"{badDuck.id}")
                        elif badDuck and badDuck.total_rare > CONFIG.numRareBadDuck:
                            self.addLogs(logType=LOG.INFO, data=Lang.UI_MaxDuckNotHatch)
                            continue
                    # Hatching for both case
                    res = await self.api.hatchEgg(data={"nest_id": egg.id})
                    if self.checkResponse(res):
                        self.addLogs(logType=LOG.INFO, data=f"{Lang.Game_Egg_Hatching} {egg.id}")

                elif egg.finish_time +1000 <= TIME.getTimeNow():
                    mode=2
                    res = await self.api.collectDuck(data={"nest_id":egg.id})
                    data = self.getData(res)
                    if data:
                        duckID = data.get("duck_id",0)
                        totalRare = data.get("total_rare",0)
                        if duckID and totalRare:
                            result["id"] =  f"{duckID}"
                            result["mes"] = f"{totalRare}"

            else:
                mode = 3
                res = await self.api.collectEgg(data={"nest_id":egg.id})
            if self.checkResponse(res):
                result["status"] = mode
            else:
                result["status"] = -1
            results.append(result)
            await asyncio.sleep(0.4)
        return results       
    
    async def collectEgg(self):
        if self.eggs:
            results = await self.checkEgg()
            status = [Lang.Game_Duck_Lazy,Lang.Game_Egg_Hatching,Lang.Game_Duck_Collected,Lang.Game_Egg_Collected,"Error"]
            hatchingEggs = []
            hatchedEggs = []
            collectedEggs = []
            waitingEggs = []
            for item in results:
                id = item.get("id")
                idStr = f"[{id}]"
                mes = item.get('mes')
                if item.get("status") == 1:
                    hatchingEggs.append(idStr)
                elif item.get("status") == 2:
                    hatchedEggs.append(f"{idStr} Total Rare {mes}")
                elif item.get("status") == 3:
                    collectedEggs.append(idStr)
                elif item.get("status") == 0:
                    waitingEggs.append(idStr)
            if hatchingEggs:
                self.addLogs(logType=LOG.COLLECT_DUCK,data=Lang.Game_Egg_Hatching+": "+" ,".join(hatchingEggs))
            if hatchedEggs:
                self.addLogs(logType=LOG.COLLECT_DUCK,data=Lang.Game_Duck_Collected+": "+" ,".join(hatchedEggs))
            if collectedEggs:
                text = "\n\t"+Lang.Game_Duck_Lazy+":"+ " ,".join(waitingEggs) if waitingEggs else ""
                self.addLogs(logType=LOG.COLLECT_EGG,data=Lang.Game_Egg_Collected+": "+" ,".join(collectedEggs)+ text) 
            
        
    async def checkReward(self):
        isCollected = False
        valueGoldenDuck = 0
        typeGoldenDuck = 0
        nextTime=-1
        info = await self.api.getNextTimeGoldenDuck()
        if not info or info.status_code != 200 or not info.json() or not info.json().get("data"):
            return  # Early exit if the request failed or data is missing
        try:
            nextTime = info.json().get("data").get("time_to_golden_duck")
        except:
            return
        if nextTime != 0:
            try:
                self.gameLogs[LOG.GOLDEN_DUCK].setNextTime(TIME.getTimeNow() + (nextTime*1000))
            except:
                pass
        else:
            reward = await self.api.getReward()
            if self.getData(res=reward):
                valueGoldenDuck = reward.json()["data"]["amount"]
                typeGoldenDuck = reward.json()["data"]["type"]
        if nextTime <= 0:
            reward = await self.api.getReward()
            for _ in range(3):
                result = await self.api.collectGoldenDuck(data={"type": 1})
                if self.getData(res=result) == True :
                    symbol = ""
                    if typeGoldenDuck and typeGoldenDuck <= 3:
                        symbol = SYMBOL_TOKEN[typeGoldenDuck]
                    self.gameLogs[LOG.GOLDEN_DUCK].setData(f"{Lang.Game_GoldenEgg_Collected} {valueGoldenDuck} {symbol}")
                    break
    async def start(self):
        if await self.Authentication(self.token):
            while True:
                second = datetime.datetime.now().second
                await self.getInfo()
                await self.collectEgg()
                await self.getBalance()
                timeNext = self.gameLogs[LOG.GOLDEN_DUCK].nextTime
                if timeNext==0 or timeNext <= TIME.getTimeNow():
                    await self.checkReward()
                await asyncio.sleep(2)
#======================================================

#======================================================
#Test Zone
MultiAccLogs:Dict[str,list[Log]] = {}
SPLIT_LINE = "="*59
def fakeCallBack(logs:list[Log],id:int=-1):
    global MultiAccLogs
    strID = f"{id}"
    MultiAccLogs[strID] = logs
    
    
    os.system("clear||cls")
    print(SPLIT_LINE+"\n===" + " dev by Blackfoxiv( https://github.com/Blackfoxiv) " + "===\n" + SPLIT_LINE +"\n")
    for id,log in MultiAccLogs.items():
        if id != "-1":
            print(f"\t\t[{id}]")
            for childLog in log:
                lastTime = TIME.getTimeStr(childLog.lastTime)
                nextTime = "Next :"+TIME.getTimeStr(childLog.nextTime)
                info = childLog.data
                print(f"_{lastTime}_{'  ' if childLog.id==LOG.GOLDEN_DUCK else ''}  {info}  {nextTime if childLog.id==LOG.GOLDEN_DUCK else ''} ")
            print(SPLIT_LINE)



    
async def mainTest():
    Token = ""
    account = Account(token=Token,logsCallBack=fakeCallBack)
    await account.start()
#======================================================

#======================================================
def inputNumber(tooltip:str,min:int=-1,max:int=-1):
    num = -1
    while num<0:
        try:
            os.system("clear||cls")
            num = int(input(tooltip+"\n"))
            if (max > 0 and num > max) or (min > 0 and num < min):
                continue
        except ValueError:
            continue
    return num
async def setupTools():
    global CONFIG,Lang
    numTypeWillHatch = -1
    numRareBadDuck = -1
    selectedLang = inputNumber("Sellect language: [0]Vietnamese, [1]English:",max=1)
    Lang = LanguagePack[selectedLang]

    #Config
    isAutoHatching = inputNumber(f"{Lang.UI_InputIsHatch}",max=1)
    if isAutoHatching:
        numTypeWillHatch = inputNumber(f"{Lang.UI_InputTypeWillHatch}",min=1)
    #Config
    isAutoRemoveBadDuck = inputNumber(f"{Lang.UI_InputIsAutoRemoveBadDuck}",max=1)
    if isAutoRemoveBadDuck:
        numRareBadDuck = inputNumber(f"{Lang.UI_InputRareBadDuck}",min=3)
    
    CONFIG = GameConfig(numTypeWillHatch=numTypeWillHatch,
                        numRareBadDuck=numRareBadDuck,
                        isAutoRemoveBadDuck=isAutoRemoveBadDuck,
                        isAutoHatching=isAutoHatching)
    print("\n")
    current_path = os.path.abspath(os.path.dirname(__file__))
    accounts = []
    with open(current_path+"/token.txt", "r") as f:
        lines = f.readlines()
        accounts = [Account(token=token.strip(),logsCallBack=fakeCallBack) for token in lines if token.strip() != ""]
        await asyncio.gather(*[account.start() for account in accounts])
#======================================================

#======================================================
async def main():
    # await mainTest()
    await setupTools()
    
asyncio.run(main())
#======================================================
