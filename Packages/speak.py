import threading
import os
class Text_To_Voice():
    def __init__(self) -> None:
        pass

    def Say(self,text="你好呀! 我係 A-EYE, 等我陪你一齊買嘢啦!",rate=180):
        print(text)
        os.system(f"say {text} -r {rate}")

    def ThreadSpeak(self,text,rate = 180):
        thread = threading.Thread(target=self.Say,args=[text,rate])
        thread.start()

        


# Text_To_Voice().Say()