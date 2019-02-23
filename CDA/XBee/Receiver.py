import os
import time
#import digi.xbee.devices
from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress
Tx = XBeeDevice("COM11", 9600) # COM port of the Receiver
Rx= RemoteXBeeDevice(Tx, XBee64BitAddress.from_hex_string("0013A20041630A6B"))
received_ack = True
Tx.open()

#def message_received(data):
xbee_message = Tx.read_data()
        #if xbee_message.data == "Acknowledgment":
        #               print "Acknowledgment received"
        #               global recieved_ack
        #               recieved_ack = True
def my_data_received_callback(xbee_message):
        address = xbee_message.remote_device.get_64bit_addr()
        data = xbee_message.data.decode("utf8")
        if data == "Transmitting":
                print("Received data from %s: %s" % (address, data))
                global received_ack
                received_ack = True

# Add the callback.
Tx.add_data_received_callback(my_data_received_callback)



while True:
        try:
                if received_ack == True:
                        Tx.send_data(Rx, "Acknowledgment")
                        received_ack= False
                        time.sleep(1)
        except KeyboardInterrupt:
                break
Tx.close()
