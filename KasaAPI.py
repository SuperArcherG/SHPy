import kasa
from kasa import SmartPlug
from kasa import IotProtocol

async def GetStatus(ip):
    plug = SmartPlug(ip)
    await plug.update()
    state = plug.is_on
    return state