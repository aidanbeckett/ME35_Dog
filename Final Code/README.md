# Final Code
## Files:
- `adafruitBrokerScript.py`: activates the script that connects to the Adafruit dashboard used to control the robot
- `read2040_v3.py`: script loaded onto the Pimoroni Servo 2040 that processes analog inputs from the RP2040
- `commands.txt`: documents the different commands that are sent through MQTT
- `final_readfromcamera.py`: script loaded onto the RP2040 that connects to a broker through MQTT and reads the messages that come through. Sends voltages according to the message sent through MQTT to the Pimoroni. Also receives commands sent from the camera through analog I/O.
