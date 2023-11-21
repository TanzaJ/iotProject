from mfrc522 import SimpleMFRC522

class RFID(object):
    def ReadRFID():
        reader = SimpleMFRC522()
        id = reader.read()[0]
        return id
