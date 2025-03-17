import asyncio
from asyncio.windows_events import NULL
from enum import Enum
import stat
from kasa import Discover, SmartDevice
from pywizlight import wizlight, PilotBuilder, discovery

class DeviceType(Enum):
    KASA_PLUG = "KasaPlug"
    WIZ_LIGHT = "Wiz"
DT = DeviceType

class Device:
    def __init__(self, device_type, ip_address):
        self.device_type = device_type
        self.ip_address = ip_address

    async def INIT(self, device_type, ip_address):
        self.device_type = device_type
        self.ip_address = ip_address
        if device_type == DT.KASA_PLUG:
            self.kasaDevice = await Discover.discover_single(ip_address)
        elif device_type == DT.WIZ_LIGHT:
            self.wizDevice = wizlight(self.ip_address)
    
    # Create an async method to initialize the device
    @classmethod
    async def create_device(cls, device_type, ip_address):
        # Create an instance
        device = cls(device_type, ip_address)
        # Run the async INIT method
        await device.INIT(device_type, ip_address)
        return device
        
    def __str__(self):
        return f"Device Type: {self.device_type}, IP Address: {self.ip_address}"
    
    def TYPE(self):
        return self.device_type
    
    def IP(self):
        return self.ip_address
    
    # KASA SUPPORT

    async def GetState(self):
        if self.device_type == DT.KASA_PLUG:
            plug = self.kasaDevice
            await plug.update()
            status = plug.is_on
            return status
        elif self.device_type == DT.WIZ_LIGHT:
            light = self.wizDevice
            state = await light.updateState()
            status = state.get_state()
            return status
        
    async def SetState(self,STATE):
        if self.device_type == DT.KASA_PLUG:
            plug = self.kasaDevice
            await plug.turn_on() if STATE else await plug.turn_off()

        elif self.device_type == DT.WIZ_LIGHT:
            light = self.wizDevice
            await light.turn_on() if STATE else await light.turn_off()

    async def ToggleState(self):
        STATE = await self.GetState()
        await self.SetState(not STATE)
        
    async def SetBrightness(self,brightness):
        if self.device_type == DT.WIZ_LIGHT:
            light = self.wizDevice
            timeout = 10
            await asyncio.wait_for(light.turn_on(PilotBuilder(brightness = brightness * 255)), timeout)
        return NULL
    
    async def SetColor(self):
        return NULL
    