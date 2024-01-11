import threading
import cv2
angle=0

def  thread_job():
    global angle
    tracker = cv2.TrackerCSRT_create()  # 創建追蹤器
    tracking = False                    # 設定 False 表示尚未開始追蹤
    cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Cannot receive frame")
            break
        frame = cv2.resize(frame,(540,300))  # 縮小尺寸，加快速度
        frame=cv2.flip(frame,1)

        keyName = cv2.waitKey(1)

        if keyName == ord('q'):
            break
        if keyName == ord('a'):
            area = cv2.selectROI('oxxostudio', frame, showCrosshair=False, fromCenter=False)
            tracker.init(frame, area)    # 初始化追蹤器
            tracking = True              # 設定可以開始追蹤
        if tracking:
            success, point = tracker.update(frame)   # 追蹤成功後，不斷回傳左上和右下的座標
            if success:
                p1 = [int(point[0]), int(point[1])]
                p2 = [int(point[0] + point[2]), int(point[1] + point[3])]
                cv2.rectangle(frame, p1, p2, (0,0,255), 3)   # 根據座標，繪製四邊形，框住要追蹤的物件
                #print(p1)
                if p1[1]>220:angle=90 
                
        cv2.imshow('oxxostudio', frame)

    cap.release()
    cv2.destroyAllWindows()
thread1= threading.Thread( target=thread_job)
thread1.start()
import serial
import time
#開啟COM埠
serialPort=serial.Serial(port ='COM3',baudrate=9600)
i=0
while True:
  if (serialPort.in_waiting > 0):
    #讀取序列埠傳來之資料解碼後並印出
    line=serialPort.readline().decode('utf-8')
    print(line)
    if "req:" in line:
      #讀取序列埠傳來之資料包含 "req:" 時才回應
      if serialPort.writable():
        #回應資料為 "res:" + str(i) + "\n"  編碼後送出
        serialPort.write(f"{angle}\n".encode('utf-8'))
        time.sleep(0.1)
        if angle == 90:
            i+=1
            if i==3:
                angle = 0
                i=0
