# Simplified IR Transmitter for Raspberry Pi Pico
import time
from machine import Pin, PWM

# Configure pins
ir_pin = Pin(22, Pin.OUT)  # Change to your connected pin
ir_pwm = PWM(ir_pin)
ir_pwm.freq(38000)  # 38kHz carrier frequency


def send_pattern():
    for i in range(5):
        send_burst(40)
        time.sleep_us(500)

def send_burst(cycles):
    burst_us = int(cycles * (1000000/38000))
    ir_pwm.duty_u16(32768)
    time.sleep_us(burst_us)
    ir_pwm.duty_u16(0)

# Main loop
while True:
    print("Sending IR signal...")
    send_pattern()
    