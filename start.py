import asyncio
import GeneralClasses as D

DeviceList = []
DL = DeviceList

async def mainThread():
    DeviceList.append(await D.Device.create_device(D.DT.WIZ_LIGHT,"192.168.0.198"))
    await DL[0].SetState(True)
    await asyncio.sleep(2.5)
    await DL[0].SetState(False)

asyncio.run(mainThread())
