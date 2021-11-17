import time
import asyncio
import win32com.client
from logipy import logi_led

class RGBControl:
    def __init__(self) -> None:
        self.auraSdk = win32com.client.Dispatch("aura.sdk.1")
        # self.auraSdk.SwitchMode()
        self.devices = self.auraSdk.Enumerate(0)

    def SetColor(self, color):
        # 0x00BBGGRR
        for dev in self.devices:
            for i in range(dev.Lights.Count):
                dev.Lights(i).color = color
                dev.Apply()

    async def Blink(self, color0, color1, duration):
        self.auraSdk.SwitchMode()
        logi_led.logi_led_init()

        endtime = time.time_ns() + int(duration*1000000000)
        while time.time_ns() < endtime:
            self.SetColor(color0)
            logi_led.logi_led_set_lighting(20, 0, 0)
            await asyncio.sleep(0.1)
            self.SetColor(color1)
            logi_led.logi_led_set_lighting(100, 0, 0)
            await asyncio.sleep(0.1)

        self.Release()
        logi_led.logi_led_shutdown()

    def Release(self):
        self.auraSdk.ReleaseControl(0)