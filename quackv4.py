import requests
import asyncio
import random
import os
import sys
import base64
import datetime
from dataclasses import dataclass,field
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
    UI_InputMinDuckKeep: str=""
    UI_InputRareBadDuck: str=""
    UI_InputIsHatch: str=""
    UI_InputIsAutoRemoveBadDuck: str=""
    UI_InputTypeWillHatch: str=""
    #In Game
    Game_Balance:str=""
    Game_Egg_Collected:str=""
    Game_Egg_HATCHING:str=""
    Game_Duck_Collected:str=""
    Game_Duck_Removed:str=""
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
        UI_InputMinDuckKeep="Sau Khi Lam Cari Vit, So Luong Toi Thieu Con Lai (Nen De 10): ",
        UI_InputRareBadDuck="Chat Luong Vit Duoi Muc Nay Se Dem Di Lam Cari (3-13):",
        UI_InputIsHatch="Tu Dong Ap Trung [0] Tat | [1] Bat",
        UI_InputIsAutoRemoveBadDuck="Tu Dong Lam Cari Vit Cui [0] Tat | [1] Bat",
        UI_InputTypeWillHatch="Chat Luong Trung Se Duoc Ap No (3-13): ",
        Game_Balance="So Du",
        Game_Egg_Collected="Da Lum Trung",
        Game_Egg_HATCHING="Dang Ap Trung",
        Game_Duck_Collected="Ap Thanh Cong Vit ",
        Game_Duck_Removed="Dang Lam CARI Be Vit",
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
        UI_InputMinDuckKeep="Enter the number of duck to keep( After Remove Bad Duck): ",
        UI_InputRareBadDuck="Enter the number of rare bad duck(min 3): ",
        UI_InputIsHatch="Auto Hatch [0] OFF | [1] ON",
        UI_InputIsAutoRemoveBadDuck="Auto Remove Bad Duck [0] OFF | [1] ON",
        UI_InputTypeWillHatch="Type Of Egg will Hatch >=: ",
        Game_Balance="Balance",
        Game_Egg_Collected="Collected Egg",
        Game_Egg_HATCHING="Hatching Egg",
        Game_Duck_Collected="Collected Duck",
        Game_Duck_Removed="Removed Bad Duck",
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
    @api_request_wrapper("nest/list-reload")
    async def getInfo(self):
        pass
    @api_request_wrapper("nest/lay-egg")
    async def getLayEgg(self):
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
#======================================================

#======================================================
@dataclass
class GameConfig():
    numMinDucks: int = 3 
    numTypeWillHatch: int = 3 #Number of types of egg will be hatched
    numRareBadDuck:int = 3 #Total rare(or lowest) of bad ducks will be remove if $isAutoRemoveBadDuck = True
    isAutoRemoveBadDuck: bool = True
    isAutoHatching: bool = True
CONFIG = GameConfig()
#======================================================

#======================================================
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

#======================================================
@dataclass
class Account():
    token: str
    logsCallBack: Callable[[Any],None]
    userID: int = -1
    eggs: list[Egg] = field(default_factory=list)
    ducks: list[Duck] = field(default_factory=list)
    config: dict = field(default_factory=dict)
    logs: str = ""
    api:API = None
    balance:list = field(default_factory=list)

    def addLogs(self,log:str):
        if self.logsCallBack:
            if self.balance:
                balance = " | ".join([f"{key} - {val}" for key,val in self.balance])
                self.logsCallBack({"id":self.userID,"logs":log,"balance":balance})
            else:
                self.logsCallBack({"id":self.userID,"logs":log})
        self.logs += log
    #Check Token is valid before start
    async def Authentication(self, token:str):
        if token == "":
            self.addLogs(f"{Lang.API_tokenNotFound} {Lang.Acion_Exit}")
            return False
        
        self.api = API(token=token)
        
        for i in range(3):
            result = await self.api.getBalance()
            if result is None or result.status_code != 200:
                self.addLogs(f"{Lang.API_LoginFailed}, {Lang.Action_Retry if i < 3 else Lang.Acion_Exit}")
                if i == 2:
                    return False
                await asyncio.sleep(3)
                continue
            if result.status_code == 200:
                self.addLogs(f"[Acc {self.userID}] {Lang.API_LoginSuccess}")
                break
            
        return True
    def getData(self,res:Response):
        if res and res.status_code == 200 and res.json() and res.json().get("data"):
            return res.json().get("data")
        return None
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
            if data and data["data"]:
                self.balance = [[item["symbol"],item["balance"]] for item in data["data"]]
    async def collectEgg(self):
        if self.eggs:
            for egg in self.eggs:
                if egg.egg_config_id == None:
                    if self.ducks:
                        lazyDucks = [duck for duck in self.ducks if duck.last_active_time == None] or self.ducks.copy()
                        lazyDucks = sorted(lazyDucks, key=lambda x: x.last_active_time)
                        if lazyDucks:
                            lazyDuck = lazyDucks[0]
                            await self.api.getLayEgg(data={"nest_id":egg.id,"duck_id":lazyDuck.id})
                elif CONFIG.isAutoHatching and egg.type_egg >= CONFIG.numTypeWillHatch:
                        if egg.finish_time == None:
                            result = await self.api.hatchEgg(data={"nest_id":egg.id})
                            if result and result.status_code == 200:
                                self.addLogs(f"{Lang.Game_Egg_HATCHING} {egg.id}")
                        elif egg.finish_time <= int(datetime.datetime.now().timestamp()*1000):
                            result = await self.api.collectDuck(data={"nest_id":egg.id})
                            if result and result.status_code == 200:
                                self.addLogs(f"{Lang.Game_Duck_Collected} {egg.id}")
                else:
                    result = await self.api.collectEgg(data={"nest_id":egg.id})
                    if result and result.status_code == 200:
                        self.addLogs(f"{Lang.Game_Egg_Collected} {egg.id}")
        if len(self.ducks) > CONFIG.numMinDucks and CONFIG.isAutoRemoveBadDuck:
            for duck in self.ducks:
                if duck.total_rare <= CONFIG.numRareBadDuck:
                    result = await self.api.removeDuck(data=f"ducks=%7B%22ducks%22%3A%5B{duck.id}%5D%7D")
                    if result and result.status_code == 200 and result.reason == "OK":
                        self.addLogs(f"{Lang.Game_Duck_Removed} {duck.id}")
                        return
    async def checkReward(self):
        isCollected = False
        symbolTypeGoldenDuck = ["","TON","PET","EGG","TRU"]
        valueGoldenDuck = 0
        typeGoldenDuck = 0
        next_time=-1
        info = await self.api.getNextTimeGoldenDuck()
        if not info or info.status_code != 200 or not info.json() or not info.json().get("data"):
            return  # Early exit if the request failed or data is missing
        try:
            next_time = info.json()["data"]["time_to_golden_duck"]
        except:
            pass

        if next_time <= 0:
            reward = await self.api.getReward()

            if reward and reward.status_code == 200 and reward.json() and reward.json().get("data") and reward.json().get("data").get("amount"):
                valueGoldenDuck = reward.json()["data"]["amount"]
                typeGoldenDuck = reward.json()["data"]["type"]
                self.addLogs(f"{Lang.Game_GoldenEgg_Value} {valueGoldenDuck}")
            for i in range(3):
                result = await self.api.collectGoldenDuck(data={"type": 1})
                if result and result.status_code == 200 and result.json() and result.json().get("data") :
                        if result.json().get("data") == True:
                            symbol = ""
                            if typeGoldenDuck and typeGoldenDuck <= 3:
                                symbol = symbolTypeGoldenDuck[typeGoldenDuck]
                            self.addLogs(f"{Lang.Game_GoldenEgg_Collected} {valueGoldenDuck} {symbol}")
                            break
                        else:
                            self.addLogs(f"{Lang.Game_GoldenEgg_Value} {result.json()['data']['amount']} {Lang.Action_Retry}")
    async def start(self):
        if await self.Authentication(self.token):
            while True:
                await self.getBalance()
                await self.getInfo()
                await self.collectEgg()
                await self.checkReward()
                await asyncio.sleep(8)
#======================================================

#======================================================
#Test Zone
def fakeCallBack(info):
    try:
        id = info.get("id")
        logs = info.get("logs")
        balance = info.get("balance")
        balance = f"{balance}".replace("000000","")
        time = datetime.datetime.now().strftime('%H:%M:%S')
        
        print(f"{time} | {id} | {logs} | {balance}")
        print("dev by Blackfoxiv99")
        print("="*69)
    except:
        pass
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
def setupTools():
    global CONFIG,Lang
    numTypeWillHatch = -1
    numRareBadDuck = -1
    numMinDucks = -1
    selectedLang = inputNumber("Sellect language: [0]Vietnamese, [1]English:",max=1)
    Lang = LanguagePack[selectedLang]

    #ConfigTools
    isAutoHatching = inputNumber(f"{Lang.UI_InputIsHatch}",max=1)
    if isAutoHatching:
        numTypeWillHatch = inputNumber(f"{Lang.UI_InputTypeWillHatch}",min=1)
    isAutoRemoveBadDuck = inputNumber(f"{Lang.UI_InputIsAutoRemoveBadDuck}",1)
    if isAutoRemoveBadDuck:
        numRareBadDuck = inputNumber(f"{Lang.UI_InputRareBadDuck}",min=3)
        numMinDucks = inputNumber(f"{Lang.UI_InputMinDuckKeep}",min=1)
    
    CONFIG = GameConfig(numMinDucks=numMinDucks,
                    numTypeWillHatch=numTypeWillHatch,
                    numRareBadDuck=numRareBadDuck,
                    isAutoRemoveBadDuck=isAutoRemoveBadDuck,
                    isAutoHatching=isAutoHatching)
    print("\n")

#======================================================

#======================================================
async def main():
    setupTools()
    current_path = os.path.abspath(os.path.dirname(__file__))
    accounts = []
    with open(current_path+"/token.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            token = line.strip()
            if token != "":
                account = Account(token=token,logsCallBack=fakeCallBack)
                accounts.append(account)
        await asyncio.gather(*[account.start() for account in accounts])
asyncio.run(main())
#======================================================
