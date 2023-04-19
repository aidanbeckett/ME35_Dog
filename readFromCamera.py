import machine
from machine import Pin, PWM, ADC
from secrets import Tufts_Wireless as wifi
import mqtt_CBR
import time

mqtt_broker = '10.245.155.171' 
topic_sub = 'walk'
topic_pub = 'walk'
client_id = 'dog'

mqtt_CBR.connect_wifi(wifi)

led = Pin(13, machine.Pin.OUT)
led.on()
pwm_walk = PWM(Pin(26))
pwm_sit = PWM(Pin(27))
pwm_dance = PWM(Pin(28))
pwm_start = PWM(Pin(29))
pwm_stop = PWM(Pin(12))
pwm_walk.freq(100)
pwm_sit.freq(100)
pwm_dance.freq(100)
pwm_start.freq(100)
pwm_stop.freq(100)

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
    elif msg2 == 'stop':
        pwm_stop.duty_u16(65000)
        time.sleep_ms(100)
        pwm_stop.duty_u16(0)
        print('should stop')
        
def whenCalled(topic, msg):
    print((topic.decode(), msg.decode()))
    print('test')
    message = msg.decode()
    parse_message(message)
    
        
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
            time.sleep(2)
        except OSError as e:
            print(e)
            print('err')
            fred.connect()
        except KeyboardInterrupt as e:
            fred.disconnect()
            print('done')
            break
            
start_sending()
