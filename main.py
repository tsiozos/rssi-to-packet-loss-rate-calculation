radio.set_transmit_power(7)
radio.set_group(99)
packetsRCVD = 0
sumRSSI = 0

def on_received_value(name, value):
    global packetsRCVD, sumRSSI
    if name=="RST":
        packetsRCVD = 0
        sumRSSI = 0
        serial.write_line("RESET")
    elif name=="SYNC":
        rssi = radio.received_packet(RadioPacketProperty.SIGNAL_STRENGTH)
        packetsRCVD = packetsRCVD + 1
        sumRSSI = sumRSSI+rssi
        serial.write_line("SUXS " + str(packetsRCVD/1000) + " RSSI(AVG):"+str(sumRSSI/packetsRCVD))
    elif name=="ENDSYNC":
        serial.write_line("SR:"+str(packetsRCVD/1000)+" PCK:"+str(packetsRCVD)+" RSSI:"+sumRSSI/packetsRCVD)
#        serial.write_value("SUCCESS RATE", packetsRCVD/1000)
#        serial.write_value("AVERAGE RSSI", sumRSSI/packetsRCVD)

radio.on_received_value(on_received_value)

def on_button_pressed_ab():
    for i in range(10):
        basic.show_number(9-i)
        #basic.pause(1000)
    basic.clear_screen()
    for i in range(100):
        radio.send_value("RST", 0)
        basic.pause(50)

    for i in range(1000):
        radio.send_value("SYNC", i)
        led.toggle(2,2)
        basic.pause(100)

    for i in range(100):
        radio.send_value("ENDSYNC", 0)
        basic.pause(50)
input.on_button_pressed(Button.AB, on_button_pressed_ab)