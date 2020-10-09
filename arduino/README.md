# Arduino Peripherals for Smart Home

Arduinos are used in various places to keep this home smart!

## Software Setup
1. Install Arduino IDE.
2. Install the additional board packages for ATTiny85 and ESP8266.
    * Open `File > Preferences > Additional Boards Managers URLs` and include:
        ```
        https://raw.githubusercontent.com/damellis/attiny/ide-1.6.x-boards-manager/package_damellis_attiny_index.json
        http://arduino.esp8266.com/stable/package_esp8266com_index.json
        ```
    * Then under `Tools > Boards > Boards Manager`, install:
        * ATTiny
        * ESP8266
3. Create a symbolic link to add your libraries to the Arduino IDE.
```
$ cd ~/Arduino/libraries
$ ln -s <project_dir>/arduino/cpp/lib SmartHome
```
4. Clone 3rd party libraries into your libraries as well.
```
$ cd ~/Arduino/libraries
$ git clone https://github.com/nRF24/RF24.git
$ git clone https://github.com/lucullusTheOnly/TinyWire
```

#### Eclipse Setup
If you're feeling brave, you can open Eclipse and configure it to look for an existing project, and then practise developing your libraries using the provided Makefile.
* Build the test project by running `make` in the same directory as the makefile.

## RGB Controller Setup
Working with `controller.ino`.
1. Wire up your system to the Arduino Nano.
    ```
    +-----------+---------+-----+
    | Device    | Mode    | Pin |
    +-----------+---------+-----+
    | Fan       | Digital | 5   |
    | Red Pin   | Analog  | 10  |
    | Green Pin | Analog  | 9   |
    | Blue Pin  | Analog  | 6   |
    +-----------+---------+-----+
    ```
2. Configure your IDE to talk to the Nano.
    * Board: Arduino Nano
    * Bootloader: ATMega328P (Old Bootloader)
3. Upload the sketch.
4. Try running the following python commands to test out the lights and fan.
```
>>> import serial
>>> s = serial.Serial('/dev/ttyUSB0',9600)
>>> s.write(b'\x03\x01\x01')         # The fan should turn on.
>>> s.write(b'\x05\x02\xff\xff\xff') # The lights should fade on.
```

## Blue or Green Wireless Light Setup
Working with `BlueGreenRFNode.ino`.
1. Wire up your system to use the RF24 pins and the output pin to the light.
    ```
    +-----------+-----+------------+
    | Use       | Pin | Mode       |
    +-----------+-----+------------+
    | Light     | 6   | Analog Out |
    | CE        | 7   | (RF24)     |
    | CSN       | 8   | (RF24)     |
    | SCK       | 13  | (RF24)     |
    | M0 (MOSI) | 11  | (RF24)     |
    | M1 (MISO) | 12  | (RF24)     |
    | VCC       | 5V  | (RF24)     |
    | GND       | GND | (RF24)     |
    +-----------+-----+------------+
    ```
    Notes:
    * CE and CSN are user configurable but have been chosen to be 7 and 8.
    * Light output goes high when you want the light you're controlling to turn on.
    * Light pin also configurable but is chosen to be out of the way of the RF modules.
    * IRQ on the nRF24L01 module isn't used for anything in this design.
2. Configure your IDE to talk to the Nano.
    * Board: Arduino Nano
    * Bootloader: ATMega328P (Old Bootloader)
3. In the sketch, make sure the address is configured to the Blue or Green Light by setting `rxAddr[]` correctly.
4. Upload the sketch.
5. Get nice and comfy with the 'Hello World' example for the RF24 and rig up a transmitter to broadcast
   to this receiver with the messages `00 00 00 00` and `FF 00 00 00`. This should hopefully switch the light
   on and off.

## RGB Wireless Light Setup
Working with `RgbRFNode.ino`.
1. Wire up your system to use the RF24 pins and the output pin to the RGB Channels.
    ```
    +------------+-----+------------+
    | Use        | Pin | Mode       |
    +------------+-----+------------+
    | Vcc (+12V) | Vin | POWER      |
    | PIN_LED_B  | D6  | Analog Out |
    | CE         | D7  | (RF24)     |
    | CSN        | D8  | (RF24)     |
    | PIN_LED_G  | D9  | Analog Out |
    | PIN_LED_R  | D10 | Analog out |
    | M0 (MOSI)  | D11 | (RF24)     |
    | M1 (MISO)  | D12 | (RF24)     |
    | SCK        | D13 | (RF24)     |
    | Vcc        | 5V  | (RF24)     |
    | Vdd        | GND | (RF24)     |
    +------------+-----+------------+
    ```
    Notes:
    * CE and CSN are user configurable but have been chosen to be 7 and 8.
    * Light output goes high when you want the light you're controlling to turn on.
2. Configure your IDE to talk to the Nano.
    * Board: Arduino Nano
    * Bootloader: ATMega328P (Old Bootloader)
3. In the sketch, make sure the address is configured to the RGB Light by setting `rxAddr[]` correctly.
4. Upload the sketch.
5. Get familiar with the 'test_transmit_rgb.py' example for the RF24 and rig up a transmitter to broadcast to this receiver with the messages `03 00 00 00` and `03 FF FF FF`. This should hopefully switch the lights on and off.

## Compound RGB Pixel Display Setup
Involves programming both an ESP8266 and an ATTiny85.

#### Wiring
```
+-------+---------+----------+----------------------------+
| Use   | ESP8266 | ATTiny85 | CIRCUIT                    |
+-------+---------+----------+----------------------------+
| VCC   | VBat    | Vcc      | Vcc(5V)                    |
| SDA   | 4       | PB0      | 1k Resistor pull up to Vcc |
| SCL   | 5       | PB2      | 1k Resistor pull up to Vcc |
| LED_R |         | PB1      | Red Channel Output         |
| LED_G |         | PB3      | Green Channel Output       |
| LED_B |         | PB4      | Blue Channel Output        |
| GND   | GND     | GND      | GND                        |
+-------+---------+----------+----------------------------+
```
Notes:
* If VCC is supplied through the FTDI cable, the ESP8266 should connect to VCC through `V+` instead of `VBat`.
* You may connect multiple ATTiny85's together as long as you give them unique addresses and LEDs.

#### ESP8266
Working with `crpd_server.ino`.
1. Wire up the ESP8266 according to the circuit described above.
2. Configure IDE to talk to the ESP8266.
    * Board: Adafruit Feather HUZZAH ESP8266
    * CPU Frequency: 80MHz
    * Baud Upload Speed: 115200
    * Serial Port: <As Applicable, probably COM0>
3. Connect FTDI cable to the module. Black goes to ground.
4. Put the ESP8266 into flash mode and upload the sketch.

#### ATTiny85
Working with `crpd_strip.ino`.
Notes:
* The ATTiny85 is programmed using a special procedure where you wire up an arduino to flash the sketch to the ATTiny85. The details on creating a programming solution is not included in these steps.

Steps:
1. Wire up the ATTiny85 according to the circuit described above.
2. Configure IDE to talk to the ATTiny85.
    * Board: ATTiny 25/45/85
    * Processor: ATTiny85
    * Clock: 8MHz
    * Port: Whichever your FTDI Adapter for the programmer is plugged into.
    * Programmer: "Arduino As ISP"
3. Burn the bootloader and upload the sketch.
4. Connect the ATTiny85 to the circuit.

## IDE Configuration
Once you've dialed in your IDE to use a specific configuration for, say, the ATTiny85, take a backup of the `preferences.txt` file that lives in `~/.arduino15`. Then, you can quickly resume your settings if you just open your IDE from command line like this:

```
$ arduino --preferences-file ~/.arduino15/preferences_attiny85.txt
```

for more variations, see https://github.com/arduino/Arduino/blob/master/build/shared/manpage.adoc.
