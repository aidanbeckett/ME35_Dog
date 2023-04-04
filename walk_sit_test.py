from machine import Pin, PWM, ADC
import time

pwm_1 = PWM(Pin(26))
pwm_2 = PWM(Pin(27))
pwm_1.freq(100)
pwm_2.freq(100)

while True:
    pwm_1.duty_u16(65000)
    time.sleep_ms(100)
    pwm_1.duty_u16(0)
    time.sleep_ms(2000)
    pwm_2.duty_u16(65000)
    time.sleep_ms(100)
    pwm_2.duty_u16(0)
