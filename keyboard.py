from logipy import logi_led
import time
import ctypes

# logi_led.load_dll('./LogitechLEDLib.lib')
logi_led.logi_led_init()
# logi_led.logi_led_flash_lighting(100, 0, 0, 5000, 100)
logi_led.logi_led_pulse_lighting(100, 0, 0, 5000, 500)
print('test')
time.sleep(5)
logi_led.logi_led_flash_lighting(100, 0, 0, 5000, 500)
time.sleep(5)
logi_led.logi_led_shutdown()
# logi_led.logi_led_flash_lighting()