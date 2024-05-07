import pyaudio
import speech_recognition as sr
import audioop

# from vosk import Model, KaldiRecognizer

from .speak import Text_To_Voice

import random

class Voice():

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    SILENCE_THRESHOLD = 300  
    RECORD_SECONDS = 10

    RESPONSE = {
        "早晨":["早晨呀","早!","早呀"],
        "午安":["午安!","午安呀, 食咗飯未呀？"],
        "晚安":["晚安! 未到夜晚喎"],
        "介紹下你自己":["我係A EYE, 我專門負責為視力障礙人士提供購物協助, 希望可以喺購物中幫到佢哋!"],
        "你今年幾多歲":["我一歲都未滿啊, 你想點先"],
        "你係男定女":["你估吓","唔知呢"],
        "你可以做啲乜嘢":["我可以幫助視力障礙人士搵到佢哋想搵嘅商品, 同時我都可以推薦最適合佢哋嘅商品, 我仲可以導航佢哋到想去嘅地方添!"]
    }
    

    def __init__(self) -> None:

        self.SPEAKING = False

        # self.VoiceToTextModel = Model("./Packages/vosk-model-small-cn-0.22")
        # self.recognizer = KaldiRecognizer(self.VoiceToTextModel, 16000) 
        self.SPEAK = Text_To_Voice()

        self.COUNT = 0

        return
    
    def GetResponse(self,text):

        if(text == False) : 
            text = ""

        if text in self.RESPONSE.keys():
            
            return random.choice(self.RESPONSE[text])
        
        else:

            return "對唔住呀，暫時幫唔到你住"

    # def GetVoice(self):

    #     MIC = pyaudio.PyAudio()

    #     VOICE_STREAM = MIC.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192) 

    #     VOICE_STREAM.start_stream()

    #     self.SPEAKING = True

    #     while True:

    #         print('listening')

    #         data = VOICE_STREAM.read(4096)

    #         if self.recognizer.AcceptWaveform(data):

    #             self.SPEAKING = False

    #             text = self.recognizer.Result()
    #             text = f"{text[14:-3]}"

    #             FinalText = ""

    #             for char in text:
    #                 if(char!=" "):
    #                     FinalText+=char

    #             return FinalText
            
    def GetCantonese(self):

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

            if rms < self.SILENCE_THRESHOLD and is_recording and self.COUNT >= 30:
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
                print("Result：" + text)

                return text

            except sr.UnknownValueError:
                print("Can not Recognize")

            except sr.RequestError as e:
                print("Request Error：" + str(e))
        
        return False

    
    # def StartMIC(self,Text = "有咩幫到你!",):

    #     if( Text != "") : self.SPEAK.Say(Text)

    #     TEXT_INPUT = self.GetVoice()

    #     return TEXT_INPUT
    
    def StartCantonese(self,Text = "有咩幫到你!",):

        self.COUNT = 0

        if( Text != "") : self.SPEAK.Say(Text)

        TEXT_INPUT = self.GetCantonese()

        return TEXT_INPUT
    
