import threading
import os

class Text_To_Voice():

    SPEACH = {
        "Welcome":""
    }

    def __init__(self) -> None:
        pass

    def Say(self,text="你好呀! 我係 A-EYE, 等我陪你一齊買嘢啦!",rate=180):

        os.system(f"say {text} -r {rate}")

    def SayMoney(self,MoneyData:dict,rate = 180 ):

        MONEY = 0

        for key in MoneyData.keys() :

            MONEY += MoneyData[key] * int(key[3:])

        text = f"你而家有{MONEY}蚊"

        os.system(f"say {text} -r {rate}")


    def ThreadSpeak(self,text,rate = 180):

        thread = threading.Thread(target=self.Say,args=[text,rate])

        thread.start()