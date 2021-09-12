import serial
from time import sleep
import serial.tools.list_ports as p
from threading import Thread


class DeviceStatus:
    def __init__(self):
        super().__init__()
        self.PORT = ""
        self.ports = list(p.comports())
        for i in self.ports:
            if "CH340" in i.description:
                self.PORT = i.name

    def serPort(self):
        return self.PORT


class SerialConnection(Thread):
    def __init__(self, PORT="COM41"):
        super().__init__()
        self.PORT = PORT
        self.rate = 115200
        self.timeout = 1
        self.DEV_ID = ""
        self.status = "DISCONNECTED"
        self.ser = serial.Serial(self.PORT, self.rate, timeout=self.timeout)
        sleep(2)

        self.start = False
        self.setUp()

    def setUp(self):
        # Connection loop
        while True:
            if self.ser.in_waiting > 0:  # check if there is any serial data coming
                data = self.ser.readline().decode("utf-8")

                if data[:-2] == "ready":  # Request for device id if the device is ready
                    self.ser.write(b'id')

                if data[:2] == "id":  # Save the device id
                    self.DEV_ID = data[2:-2]
                    if self.DEV_ID:  # set the start flag to true and exit the loop after getting the id
                        self.start = True
                        break

    def startLoop(self):
        while True:
            if self.start:
                self.ser.write(b'start')  # trigger device to start sending data
                self.start = False

            if self.ser.in_waiting > 0:
                data = self.ser.readline().decode("utf-8")
                print(data)


if __name__ == "__main__":
    p = DeviceStatus()
    s = SerialConnection(p.serPort())
    print(s.DEV_ID)
    s.startLoop()
