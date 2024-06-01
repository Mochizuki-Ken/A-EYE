import speech_recognition as sr

# # 創建 Recognizer 物件
r = sr.Recognizer()

# # 使用麥克風錄音
# with sr.Microphone() as source:
#     print("請開始說話...")
#     audio = r.listen(source,100)

#     try:
#         # 語音識別
#         text = r.recognize_google(audio, language="yue-Hant-HK")  # 使用廣東話語言代碼
#         print("識別結果：" + text)
#     except sr.UnknownValueError:
#         print("無法識別語音")
#     except sr.RequestError as e:
#         print("無法從 Google Speech Recognition 服務獲取結果： {0}".format(e))


import pyaudio

MIC = pyaudio.PyAudio()

VOICE_STREAM = MIC.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192) 

VOICE_STREAM.start_stream()


while True:

    print('listening')

    audio = VOICE_STREAM.read(4096)

    audio = r.listen(audio)


    try:
            # 語音識別
        text = r.recognize_google(audio, language="yue-Hant-HK")  # 使用廣東話語言代碼
        if(text) : break
        print("識別結果：" + text)
    except sr.UnknownValueError:
        print("無法識別語音")
    except sr.RequestError as e:
        print("無法從 Google Speech Recognition 服務獲取結果： {0}".format(e))