# Simplified IR Transmitter for Raspberry Pi Pico
import time
from machine import Pin, PWM

# Configure pins
ir_pin = Pin(22, Pin.OUT)  # Change to your connected pin
ir_pwm = PWM(ir_pin)
ir_pwm.freq(38000)  # 38kHz carrier frequency
led = Pin(25, Pin.OUT)  # Onboard LED for visual feedback

def send_simple_code():
    # Simple pattern: 10ms on, 10ms off, repeated 5 times
    for _ in range(5):
        # Turn on IR LED (with carrier)
        ir_pwm.duty_u16(32768)  # 50% duty cycle
        led.value(1)  # Visual feedback
        time.sleep_ms(10)
        
        # Turn off IR LED
        ir_pwm.duty_u16(0)
        led.value(0)
        time.sleep_ms(10)
    
    # End with a longer pause
    time.sleep_ms(100)

# Main loop
while True:
    print("Sending IR signal...")
    send_simple_code()
    time.sleep_ms(500)  # Send every 0.5 seconds