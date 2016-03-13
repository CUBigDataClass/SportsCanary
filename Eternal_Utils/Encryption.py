import datetime
from Crypto.Cipher import AES
from CommonUtils import CommonUtils


class Encryption:
    def __init__(self):
        self.BS = 16
        self.input = CommonUtils.get_environ_variable('NODE_API_KEY')
        self.iv = CommonUtils.get_environ_variable('NODE_API_IV')

    def pad(self, data):
        padding = self.BS - len(data) % self.BS
        return data + padding * chr(padding)

    @staticmethod
    def un_pad(data):
        return data[0:-ord(data[-1])]

    def decrypt_node(self, hex_data):
        iv = self.iv
        key = datetime.datetime.now().strftime(self.input) + datetime.datetime.now().strftime(self.input)
        data = ''.join(map(chr, bytearray.fromhex(hex_data)))
        aes = AES.new(key, AES.MODE_CBC, iv)
        return self.un_pad(aes.decrypt(data))

    def encrypt_node(self, data):
        iv = self.iv
        key = datetime.datetime.now().strftime(self.input) + datetime.datetime.now().strftime(self.input)
        aes = AES.new(key, AES.MODE_CBC, iv)
        return aes.encrypt(self.pad(data)).encode('hex')
