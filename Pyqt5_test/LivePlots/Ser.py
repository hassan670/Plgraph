import serial
import serial.tools.list_ports as p
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets
import numpy as np
import threading
from Arduino import ser_test


class Live(QWidget):
    start = False

    def __init__(self, w, start=False):
        super().__init__()
        self.start = start
        self.PORT = ""
        self.ptr = 0
        self.dev_flag = False    # indicator to show connection of device
        self.check = True        # allows device checkup

        self.serial_device = ser_test.SerialDevice()
        self.win = pg.GraphicsLayoutWidget(w, show=True)
        self.win.resize(383, 192)
        self.p1 = self.win.addPlot()
        self.win.nextRow()
        self.p2 = self.win.addPlot()
        self.win.nextRow()
        self.p3 = self.win.addPlot()
        self.win.nextRow()

        self.gsrValues = [0] * 300
        self.HrtValues = [0] * 300
        self.RrtValues = [0] * 300
        self.timeStampValues = list(range(300))

        self.curve1 = self.p1.plot(self.timeStampValues, self.HrtValues, pen="g")
        self.curve2 = self.p2.plot(self.timeStampValues, self.RrtValues, pen="y")
        self.curve3 = self.p3.plot(self.timeStampValues, self.gsrValues, pen="r")

        self.th1 = threading.Thread(target=self.ser_check, daemon=True)  # will keep of checking if there is a device
        self.th1.start()

        self.ser = serial.Serial()

        self.timer = pg.QtCore.QTimer()

    def start_(self):
        self.timer.timeout.connect(self.receiver)
        self.timer.start()

    def ser_port(self):
        return self.PORT

    def ser_check(self):
        while True:

            if self.serial_device.device():
                if self.check:
                    try:
                        self.PORT = self.serial_device.ser_port()
                        self.ser.port = self.PORT
                        self.ser.baudrate = 115200
                        self.ser.timeout = 1
                        self.ser.open()
                        self.dev_flag = True  # set the device flag to true once the serial port is opened
                        self.check = False    # disable check up if serial connection is obtained
                    except serial.serialutil.SerialException:
                        pass

            if not self.serial_device.device():
                self.ser.close()
                self.dev_flag = False
                self.check = True         # enable checkup if device is reconnected

    def connection(self):
        return self.dev_flag

    def receiver(self):
        if self.start is True and self.dev_flag is True and self.serial_device.device() is True:
            try:
                if self.ser.in_waiting > 0:
                    data = self.ser.readline()
                    data = data[:-2].decode().split(",")

                    self.RrtValues = np.roll(self.RrtValues, 1)
                    self.gsrValues = np.roll(self.gsrValues, 1)
                    self.HrtValues = np.roll(self.HrtValues, 1)

                    self.RrtValues[0] = float(data[0])
                    self.gsrValues[0] = float(data[1])
                    self.HrtValues[0] = float(data[2])

                    self.ptr += 1
                    self.curve1.setData(self.HrtValues)
                    self.curve1.setPos(self.ptr, 0)
                    self.curve2.setData(self.RrtValues)
                    self.curve2.setPos(self.ptr, 0)
                    self.curve3.setData(self.gsrValues)
                    self.curve3.setPos(self.ptr, 0)
            except ValueError:
                pass
            except serial.serialutil.SerialException:
                self.dev_flag = False
                pass


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    # ui = Live()
    sys.exit(app.exec_())
