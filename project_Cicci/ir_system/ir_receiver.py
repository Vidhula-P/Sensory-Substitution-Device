# Simplified IR Receiver for Raspberry Pi Pico
import time
from machine import Pin, Timer
from mcp4822_dds import MCP4822, DAC_DDS

# Define isr gpio port, sound_duration
ISR_GPIO = 5
SOUND_DURATION = 1000 #ms
FREQ_START = 261.63  # Middle C


signal_detected = False
last_signal_detected = False
count_0 = 0
STATE = -1

# Configure pins
ir_pin = Pin(16, Pin.IN)  # Change to your connected pin

# Setup GPIO pin for ISR timing visualization
isr_gpio = Pin(ISR_GPIO, Pin.OUT)
isr_gpio.value(0)

# DAC setup (edit pin numbers as needed)
dac = MCP4822(spi_bus=1, cs_pin_num=12, sck_pin_num=10, mosi_pin_num=11)
dds = DAC_DDS(dac, channel=0, effective_sample_rate=2337)

# IR signal detection timer

def check_ir(ir_timer):
    global signal_detected, last_signal_detected, STATE, count_0
    isr_gpio.value(1)

    # Determine ir signal detection

    signal_detected = (ir_pin.value() == 0)

    # Trigger the sound if signal detected

    if signal_detected and (STATE == -1) and not last_signal_detected:
        STATE = 1
        count_0 = 0
        dds.start(FREQ_START)
        
    last_signal_detected = signal_detected    
    isr_gpio.value(0)

def alarm(alarm_timer):
    global count_0, STATE, signal_detected
    if STATE == 1:
        count_0 += 1 
        # When signal is not detected and already enough time to creat sound, trigger stop
        if (count_0 >= SOUND_DURATION) and not(signal_detected):
            dds.stop()
            STATE = -1
            count_0 = 0

# Setup Timers
ir_timer = Timer()
ir_timer.init(mode=Timer.PERIODIC, period=1, callback=check_ir)

alarm_timer = Timer()
alarm_timer.init(mode=Timer.PERIODIC, period=1, callback=alarm)

while True:
    
    time.sleep(1)