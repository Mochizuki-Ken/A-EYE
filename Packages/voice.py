import pyaudio
import speech_recognition as sr
import audioop

# from vosk import Model, KaldiRecognizer

from .speak import Text_To_Voice
from .sound import Sound

import random

class Voice():

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    SILENCE_THRESHOLD = 300  
    RECORD_SECONDS = 10

    RESPONSE = {
        "Goodmorning":["早晨呀","早!","早呀"],
        "Goodevening":["午安!","午安呀, 食咗飯未呀？"],
        "GoodNight":["晚安! 未到夜晚喎"],
        "IntroSelf":["我係A EYE, 我專門負責為視力障礙人士提供購物協助, 希望可以喺購物中幫到佢哋!"],
        "HowOld":["我一歲都未滿啊, 你想點先?"],
        "Gender":["你估吓","唔知呢"],
        "Mision":["我可以幫助視力障礙人士搵到佢哋想搵嘅商品, 同時我都可以推薦最適合佢哋嘅商品, 我仲可以導航佢哋到想去嘅地方添!"],
        "Name":["我叫做A-EYE","可以叫我A-EYE"],
        "DisplayMode":["冇問題, 而家為大家示範我嘅基本功能, 尋找和識別商品, 以及推薦優惠商品."],

        "Yes":["好","可以","冇問題","允許","係","冇錯","確認"],
        "No":[] 
        
    }

    FUNT_CMD = ["Want_To_Buy","Cancel_Target","Discount","Current_Target","Find_Place"]

    DICT = {
        "Want_To_Buy":["我想搵商品","我要搵商品","幫我搵商品","我想搵物品","我要搵物品","幫我搵物品","搵商品","搵物品","我想搵嘢","我要搵嘢","買嘢","商品","買"],
        "Cancel_Target":["幫我取消物品","幫我取消","取消物品","取消商品","取消尋找物品","取消尋找商品","刪除"],
        "Current_Target":["而家有咩目標物品","而家有咩目標商品","而家有咩","搵緊"],
        "Discount":["而家做緊咩優惠","優惠","推廣","折扣","促銷","宣傳","活動"],
        "Find_Place":["地方","我想去","區域"],
        "Cancel_Find_Place":["取消尋找區域", "取消尋找地方","取消區域","取消地方","取消目標區域","取消目標地方"],
        "IntroSelf":["介紹下自己","介紹下你自己","自我介紹下","介紹自己"],
        "Goodmorning":["早晨","早上好","早"],
        "Goodevening":["午安","中午好"],
        "GoodNight":["晚安","晚上好"],
        "HowOld":["你幾多歲","你今年幾多歲","幾歲","你幾歲","你今年幾歲"],
        "Gender":["你嘅性別係乜","你係男定女","你係咪男仔","你係咪女仔","性別","男","女"],
        "Mision":["你可以做啲乜","你嘅使命係乜","使命","任務","責任"],
        "Name":["你叫咩名","名字","名"],
        "DisplayMode":["示範","測試","展示"],


    }
    

    def __init__(self) -> None:

        self.SPEAKING = False

        self.LANG = "CHI"

        self.SPEAK = Text_To_Voice()

        self.SOUND = Sound()

        self.COUNT = 0

        return
    
    def GetResponse(self,text):

        if(text == False) : 
            text = ""

        CMD = False

        for i in self.DICT.keys():

            for e in self.DICT[i] :

                if e in text:

                    CMD = i

        if ( CMD == False ):

            return "對唔住呀，暫時幫唔到你住"

        if( CMD not in self.FUNT_CMD ) :

            return random.choice( self.RESPONSE[CMD] )

        else:

            return CMD

    def GetCantonese(self,limit=30):

        audio = pyaudio.PyAudio()

        try:

            stream = audio.open(

                format=self.FORMAT, 
                channels=self.CHANNELS, 
                rate=self.RATE, 
                input=True, 
                frames_per_buffer=self.CHUNK
                
            )

        except :
            print("cant open mic")

        print("Start recording")

        recognizer = sr.Recognizer()

        audio_frames = []

        is_recording = True

        for i in range(int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
 
            data = stream.read(self.CHUNK)
            audio_frames.append(data)

            self.COUNT += 1

            rms = audioop.rms(data, 2)  

            if rms < self.SILENCE_THRESHOLD and is_recording and self.COUNT >= limit:
                print("Stop Recoerding")
                is_recording = False
                break

        stream.stop_stream()
        stream.close()
        audio.terminate()

        if not is_recording:

            audio_source = sr.AudioData(b''.join(audio_frames), sample_rate=self.RATE, sample_width=2)

            try:

                text = recognizer.recognize_google(audio_source, language='yue-Hant-HK')

                if( self.LANG == "ENG" ) :
                    
                    text = recognizer.recognize_google(audio_source, language='en-US')

                print("Result：" + text)

                return text

            except sr.UnknownValueError:
                print("Can not Recognize")

            except sr.RequestError as e:
                print("Request Error：" + str(e))
        
        return False

    
    def StartCantonese(self,Text = "有咩幫到你!",limit=30):

        self.COUNT = 0

        if( Text != "") : 
            
            self.SPEAK.Say(Text)

            self.SOUND.ThreadPlaySound("Note-1")

        TEXT_INPUT = self.GetCantonese(limit=limit)

        return TEXT_INPUT
    
    def Confirm(self):

        self.COUNT = 0

        TEXT_INPUT = self.GetCantonese()

        if( TEXT_INPUT == False):

            return False

        for i in self.RESPONSE["Yes"] :

            if i in TEXT_INPUT :

                return True

        return False
    
