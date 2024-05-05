import pyaudio
from vosk import Model, KaldiRecognizer

from .speak import Text_To_Voice

class Voice():

    def __init__(self) -> None:

        self.SPEAKING = False

        self.VoiceToTextModel = Model("./Packages/vosk-model-small-cn-0.22")
        self.recognizer = KaldiRecognizer(self.VoiceToTextModel, 16000) 
        self.SPEAK = Text_To_Voice()

        return
    
    def GetResponse(self,text):
        if text:
            return text

    def GetVoice(self):

        MIC = pyaudio.PyAudio()

        VOICE_STREAM = MIC.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192) 

        VOICE_STREAM.start_stream()

        self.SPEAKING = True

        while True:

            print('listening')

            data = VOICE_STREAM.read(4096)

            if self.recognizer.AcceptWaveform(data):

                self.SPEAKING = False

                text = self.recognizer.Result()
                text = f"{text[14:-3]}"

                FinalText = ""

                for char in text:
                    if(char!=" "):
                        FinalText+=char

                return FinalText
    
    def StartMIC(self,Text = "有咩幫到你!"):

        if( Text != "") : self.SPEAK.Say(Text)

        TEXT_INPUT = self.GetVoice()

        return TEXT_INPUT