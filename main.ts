radio.setTransmitPower(7)
radio.setGroup(99)
let packetsRCVD = 0
let sumRSSI = 0
radio.onReceivedValue(function on_received_value(name: string, value: number) {
    let rssi: number;
    
    if (name == "RST") {
        packetsRCVD = 0
        sumRSSI = 0
        serial.writeLine("RESET")
    } else if (name == "SYNC") {
        rssi = radio.receivedPacket(RadioPacketProperty.SignalStrength)
        packetsRCVD = packetsRCVD + 1
        sumRSSI = sumRSSI + rssi
        serial.writeValue("SUCCESS %", packetsRCVD / value)
    } else if (name == "ENDSYNC") {
        serial.writeLine("")
        serial.writeValue("SUCCESS RATE", packetsRCVD / 1000)
        serial.writeValue("AVERAGE RSSI", sumRSSI / packetsRCVD)
    }
    
})
input.onButtonPressed(Button.AB, function on_button_pressed_ab() {
    let i: number;
    for (i = 0; i < 10; i++) {
        basic.showNumber(9 - i)
    }
    // basic.pause(1000)
    basic.clearScreen()
    for (i = 0; i < 100; i++) {
        radio.sendValue("RST", 0)
        basic.pause(50)
    }
    for (i = 0; i < 1000; i++) {
        radio.sendValue("SYNC", i)
        led.toggle(2, 2)
        basic.pause(100)
    }
    for (i = 0; i < 100; i++) {
        radio.sendValue("ENDSYNC", 0)
        basic.pause(50)
    }
})
