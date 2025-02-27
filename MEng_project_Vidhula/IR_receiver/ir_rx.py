# Simplified IR Receiver for Raspberry Pi Pico
import time
from machine import Pin

# Configure pins
ir_pin = Pin(16, Pin.IN)  # Change to your connected pin
led = Pin(25, Pin.OUT)  # Onboard LED for visual feedback

# Simple detection loop
last_state = ir_pin.value()
last_change = time.ticks_ms()
signal_detected = False

print("IR Receiver started. Waiting for signals...")

while True:
    current_state = ir_pin.value()
    
    # If state changed, record it
    if current_state != last_state:
        time_since_change = time.ticks_diff(time.ticks_ms(), last_change)
        last_change = time.ticks_ms()
        last_state = current_state
        
        # If we see rapid changes (activity), count as signal
        if time_since_change < 30:  # Less than 30ms between changes
            if not signal_detected:
                print("IR signal detected!")
                led.value(1)  # Turn on LED
                signal_detected = True
    
    # Reset detection after some time without changes
    if signal_detected and time.ticks_diff(time.ticks_ms(), last_change) > 200:
        led.value(0)  # Turn off LED
        signal_detected = False
    
    # Small delay to prevent overwhelming the CPU
    time.sleep_ms(5)