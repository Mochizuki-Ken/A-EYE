import threading
import os

class Text_To_Voice():

    SPEACH = {
        "Welcome":"你好呀! 我係A-EYE, 今日等我陪你一齊買嘢啦, 只要食指拇指雙擊兩下我就會出嚟㗎啦!"#, 今日等我陪你一齊買嘢啦, 只要食指拇指雙擊兩下我就會出嚟㗎啦!
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


    def ThreadSpeak(self,text = "",temp = "",rate = 180):

        if( temp != "" ):
            
            text = self.SPEACH[ temp ]

        thread = threading.Thread(target=self.Say,args=[text,rate])

        thread.start()
