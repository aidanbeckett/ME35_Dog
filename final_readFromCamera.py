import machine
from machine import Pin, PWM, ADC
from secrets import Tufts_Wireless as wifi
import mqtt_CBR
import time
import uasyncio as asyncio

mqtt_broker = '10.245.153.66'
topic_sub = 'walk'
topic_pub = 'walk'
client_id = 'dog'

mqtt_CBR.connect_wifi(wifi)

walk_input = Pin(20,Pin.IN)
sit_input = Pin(19,Pin.IN)

pwm_walk = PWM(Pin(26))
pwm_sit = PWM(Pin(27))
pwm_dance = PWM(Pin(28))
pwm_start = PWM(Pin(29))
pwm_head = PWM(Pin(13))
pwm_walk.freq(100)
pwm_sit.freq(100)
pwm_dance.freq(100)
pwm_start.freq(100)
pwm_head.freq(100)

previous_value = 0

def read_camera():
    print('camera starting')
    global previous_value
    for i in range(0,6000):
        walk_read = walk_input.value()
        sit_read = sit_input.value()
        if walk_read >= 1 and previous_value!= 1:
            pwm_walk.duty_u16(65000)
            time.sleep_ms(100)
            pwm_walk.duty_u16(0)
            print('should walk')
            previous_value = 1
        elif sit_read >= 1 and previous_value!= 2:
            pwm_sit.duty_u16(65000)
            time.sleep_ms(100)
            pwm_sit.duty_u16(0)
            print('should sit')
            previous_value = 2
        time.sleep(0.01)
    

def parse_message(msg2):
    if msg2 == 'start':
        pwm_start.duty_u16(65000)
        time.sleep_ms(100)
        pwm_start.duty_u16(0)
        print('should start')
    elif msg2 == 'walk':
        pwm_walk.duty_u16(65000)
        time.sleep_ms(100)
        pwm_walk.duty_u16(0)
        print('should walk')
    elif msg2 == 'sit':
        pwm_sit.duty_u16(65000)
        time.sleep_ms(100)
        pwm_sit.duty_u16(0)
        print('should sit')
    elif msg2 == 'dance':
        pwm_dance.duty_u16(65000)
        time.sleep_ms(100)
        pwm_dance.duty_u16(0)
        print('should dance')
    elif msg2 == 'headPanLeft':
        pwm_head.duty_u16(65000)
        time.sleep_ms(100)
        pwm_head.duty_u16(0)
        print('should pan')
        
def whenCalled(topic, msg):
    print((topic.decode(), msg.decode()))
    print('test')
    message = msg.decode()
    parse_message(message)
    
        
def start_sending():
    print('mqtt starting')
    fred = mqtt_CBR.mqtt_client(client_id, mqtt_broker, whenCalled)
    fred.subscribe(topic_sub)
    old = 0
    i = 0
    while True:
        try:
            fred.check()
            time.sleep(2)
        except OSError as e:
            print(e)
            print('err')
            fred.connect()
        except KeyboardInterrupt as e:
            fred.disconnect()
            print('done')
            break

read_camera()
start_sending()
