from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import cv2
import json

class Design(QMainWindow):
    def __init__(self, *args):
        super(Design, self).__init__()
        uic.loadUi('mainwindow.ui', self)

        # Fix the size of the widget
        self.setFixedSize(self.geometry().width(), self.geometry().height())

        self.pbloadSetting.clicked.connect(self.onLoadSetting)
        self.pbstartRecord.clicked.connect(self.onStartRecord)
        self.pbstopRecord.clicked.connect(self.onStopRecord)
        self.pbfinish.clicked.connect(self.close)
        
        self.show()

        self.savePath = ""
        self.videoLength = 5    # 5 minutes
        self.ipAddresses = []
        
        self.video_counter = 0
        self.bRecording = False

        self.pbstopRecord.setEnabled(False)
        self.pbstartRecord.setEnabled(False)

    # Pointing Function
    def onLoadSetting(self):
        file = open('test.json')
        data = json.load(file)

        self.savePath = data['videoFolder']
        self.videoLength = data['videoLength']

        ips = data['ips']

        for ipAddress in ips:
            self.ipAddresses.append(ipAddress)

        self.pbstartRecord.setEnabled(True) 
        QMessageBox.information(self, 'alert', 'setting success!')

    def onStartRecord(self):

        QObject.startTimer(self, 1000 * 60 * self.videoLength)
        self.pbstartRecord.setEnabled(False)
        self.pbstopRecord.setEnabled(True)
        self.bRecording = True

        stream = cv2.VideoCapture('rtsp://admin_11:admin123@192.168.1.46:88/videoMain', cv2.CAP_FFMPEG)  
        # stream = cv2.VideoCapture('http://192.168.1.46:88/cgi-bin/CGIStream.cgi?cmd=GetMJStream&usr=admin_11&pwd=admin123')
        # stream = cv2.VideoCapture("http://192.168.1.46:88/videostream.cgi?user=admin_11&pwd=admin123")  
      
        # stream = cv2.VideoCapture(0)
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(self.savePath + "/" + str(self.video_counter) + ".avi", self.fourcc, 25.0, (640, 480))

        while True:
            if self.bRecording is False:
                break

            r, f = stream.read()

            if r is False:
                continue

            # print(f.shape)
            f = cv2.resize(f, (640, 480))
            cv2.imshow('IP Camera stream', f)

            self.out.write(f)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def onStopRecord(self):
        self.out = None
        self.pbstartRecord.setEnabled(True)
        self.pbstopRecord.setEnabled(False)
        self.bRecording = False

    def timerEvent(self, event):
        self.out.release()
        self.video_counter += 1
        self.out = cv2.VideoWriter(self.savePath + "/" + str(self.video_counter) + ".avi", self.fourcc, 25.0, (640, 480))
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Design()
    form.show()
    app.exec()



       

