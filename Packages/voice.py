import pyaudio
from vosk import Model, KaldiRecognizer
class Voice():
    def __init__(self) -> None:
        self.SPEAKING = False
        return

    def GetVoice(self):
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192) 
        stream.start_stream()
        self.SPEAKING = True
        while True:
            print('listening')
            data = stream.read(4096)
            if self.recognizer.AcceptWaveform(data):
                self.SPEAKING = False
                text = self.recognizer.Result()
                text = f"{text[14:-3]}"
                FinalText = ""
                for char in text:
                    if(char!=" "):
                        FinalText+=char
                return 
    
    def StartMic(self):

        TEXT_INPUT = self.GetVoice()

        if(TEXT_INPUT=="我有多少钱"):
            speaktext = f"你有 "+str(self.Current_Cash["D10"]*10 + self.Current_Cash["D20"]*20
                    + self.Current_Cash["D50"]*50 + self.Current_Cash["D100"]*100
                    + self.Current_Cash["D500"]*500)+" 塊錢"

            print(speaktext)

            self.ThreadSpeck(text=speaktext)
        # elif(TEXT_INPUT[0:3]=="我想买"):
        #     product_name = TEXT_INPUT[3:]

            # self.voice_order_state[0] = self.Timer
            # self.voice_order_state[1] = "SearchProduct"
            # self.voice_order_state[2] = product_name

        return TEXT_INPUT