from Packages import *

INPUT_MODE = "udp://192.168.0.125:1234" # 0 for Build-in Cam / Url for A-EYE Device
INPUT_MODE = 0

if __name__ == "__main__":

    Aeye = AEYE.A_EYE(STREAM_INPUT=INPUT_MODE)

    Aeye.Start()