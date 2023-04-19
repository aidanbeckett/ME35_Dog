from machine import Pin, PWM, ADC
from secrets import Tufts_eecs as wifi
import mqtt_CBR
import time

mqtt_broker = '10.5.2.239' 
topic_sub = 'walk'
topic_pub = 'walk'
client_id = 'dog'

mqtt_CBR.connect_wifi(wifi)

led = Pin(13, machine.Pin.OUT)
led.on()
pwm_1 = PWM(Pin(26))
pwm_2 = PWM(Pin(27))
pwm_1.freq(100)
pwm_2.freq(100)

def whenCalled(topic, msg):
    print((topic.decode(), msg.decode()))
    message = msg.decode()
    if message == 'start':
        send_to_legs()
    time.sleep(20)
#TODO: Add function that checks message and executes function based on message sent
def send_to_legs():
    while True:
        led.off()
        time.sleep(0.5)
        led.on()
        pwm_1.duty_u16(0)
        pwm_1.duty_u16(65000)
        time.sleep_ms(100)
        pwm_1.duty_u16(0)
        time.sleep_ms(15000)
        
def start_sending():
    fred = mqtt_CBR.mqtt_client(client_id, mqtt_broker, whenCalled)
    fred.subscribe(topic_sub)
    led.off()
    time.sleep(0.5)
    led.on()
    old = 0
    i = 0
    while True:
        try:
            fred.check()
        except OSError as e:
            print(e)
            fred.connect()
        except KeyboardInterrupt as e:
            fred.disconnect()
            print('done')
            break
            
 start_sending()
