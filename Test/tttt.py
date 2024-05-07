import pyaudio
import speech_recognition as sr
import audioop

# 初始化PyAudio
audio = pyaudio.PyAudio()

# 定义录音参数
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
SILENCE_THRESHOLD = 250  # 设置音量阈值，根据需要调整
RECORD_SECONDS = 10
COUNT = 0

# 打开麦克风流
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("开始录音...")

# 创建Recognizer对象
recognizer = sr.Recognizer()

# 创建一个空的音频列表
audio_frames = []

# 录音状态标志
is_recording = True

# 持续录音
for i in range(int(RATE / CHUNK * RECORD_SECONDS)):
    # 从麦克风流中读取音频数据
    data = stream.read(CHUNK)
    audio_frames.append(data)

    COUNT += 1

    # 计算音量
    rms = audioop.rms(data, 2)  # 使用2字节采样宽度

    # 如果音量低于阈值，表示说话已结束，停止录音
    if rms < SILENCE_THRESHOLD and is_recording and COUNT >= 30:
        print("停止录音")
        is_recording = False
        break

# 关闭麦克风流
stream.stop_stream()
stream.close()
audio.terminate()

if not is_recording:
    # 将音频数据转换为音频源格式
    audio_source = sr.AudioData(b''.join(audio_frames), sample_rate=RATE, sample_width=2)

    # 使用语音识别库进行语音识别
    try:
        # 使用Google Web语音识别进行语音识别
        text = recognizer.recognize_google(audio_source, language='yue-Hant-HK')
        print("识别结果：" + text)
    except sr.UnknownValueError:
        print("无法识别音频")
    except sr.RequestError as e:
        print("请求出错：" + str(e))