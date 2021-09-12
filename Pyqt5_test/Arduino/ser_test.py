from threading import Thread
import serial.tools.list_ports as p
import serial


class SerialDevice(Thread):
    def __init__(self):
        super().__init__()
        self.PORT = ""
        self.ports = list(p.comports())
        for i in self.ports:
            if "CP210x" in i.description:
                self.PORT = i.name

    def device(self):
        ports = list(p.comports())
        for i in ports:
            if "CP210x" in i.description:
                self.PORT = i.name
                return True
            else:
                self.PORT = ""
                return False


    def ser_port(self):
        return self.PORT

if __name__ == "__main__":
    d = SerialDevice()
    print(d.ser_port())
