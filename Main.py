from Packages import *

INPUT_MODE = "http://192.168.0.206:5000/stream" # 0 for Build-in Cam / Url for A-EYE Device
INPUT_MODE = 0

if __name__ == "__main__":

    # Mode = input("Mode: ")


    Aeye = AEYE.A_EYE(STREAM_INPUT=INPUT_MODE)

    Aeye.Start()