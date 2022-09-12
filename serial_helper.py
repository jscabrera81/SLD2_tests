import serial
import time
import logging

polling_time = 0.02500

class SerialPort():
    def __init__(self, uart):
        self.port = uart


    def __new__(cls, uart):
        global LOGGER
        LOGGER = logging.getLogger(__name__)
        return object.__new__(cls)

    def open(self):
        self.device = serial.Serial(port=self.port, baudrate=115200, timeout=0)

    def wait_for_dev_ready(self):
        command = "AT\n"
        expected_resp = "OK\r\n"
        while True:
            self.device.write(command.encode())
            time.sleep(polling_time)

            if self.device.inWaiting() == 0:
                time.sleep(polling_time)
                continue


            bytes_to_read = self.device.inWaiting()
            read_bytes = self.device.read(bytes_to_read)
            print(bytes_to_read)
            respString = read_bytes.decode("utf-8")
            if expected_resp == respString:
                break

    def execute_command(self, command, wait_for_resp, certificate = False):
        print("Executing command: " + command)
        self.device.reset_input_buffer()
        ret = self.device.write(command.encode())
        time.sleep(polling_time)

        if wait_for_resp == False:
            return ''

        while self.device.inWaiting() == 0:
            print("waiting for response")
            time.sleep(polling_time)

        read_bytes = bytes()
        while self.device.inWaiting():
            read_bytes += self.device.read()
            respString = read_bytes.decode("utf-8")
            if "ERR"  in respString or "OK" in respString:
                if certificate:
                    if "-----END CERTIFICATE-----" in respString:
                        break
                elif "\n" in respString:
                    break
                time.sleep(polling_time)
        return read_bytes

    def send_binary(self, data):
        return self.device.write(data)

    def read_binary(self):
        time.sleep(0.02)
        while self.device.inWaiting() == 0:
            print("waiting for response")
            time.sleep(polling_time)

        bytes_to_read = self.device.inWaiting()
        return self.device.read(bytes_to_read)

    def close_dev(self):
        self.device.close()

    def is_Open(self):
        return self.device.isOpen()

    def logMemory(self, msg):
        LOGGER.info(f"MEMORY,{msg}")

    def ExecuteAndCheck(self, command, expectedValue):
        resp = self.execute_command(command, True)
        respString = resp.decode("utf-8")
        c = command.strip('\n\r')
        e = expectedValue.strip('\n\r')
        r = respString.strip('\n\r')
        if respString == expectedValue:
            LOGGER.info(f'{c},{e},{r},PASS')
            return True
        else:
            print(f'Expected: {expectedValue}')
            print(f'Actual: {respString}')
            LOGGER.info(f'{c},{e},{r},FAIL')
        return False

    def ExecuteAndCheckCertLen(self, command, resp_length):
        resp = self.execute_command(command, True, True)
        respString = resp.decode("utf-8")
        if len(respString) >= resp_length:
            return True
        return False

class Sld2SerialPort1(SerialPort):
    INSTANCE = None
    def __new__(cls, uart):

        if Sld2SerialPort1.INSTANCE is None:
            Sld2SerialPort1.INSTANCE = super().__new__(cls, uart)

        return Sld2SerialPort1.INSTANCE

class Sld2SerialPort2(SerialPort):
    INSTANCE = None
    def __new__(cls, uart):

        if Sld2SerialPort2.INSTANCE is None:
            Sld2SerialPort2.INSTANCE = super().__new__(cls, uart)

        return Sld2SerialPort2.INSTANCE