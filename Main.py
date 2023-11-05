import asyncio
import kasa
from kasa import SmartPlug
from functools import partial
import tkinter as tk
from tkinter import ttk


ips = ""
names = []
states = []
predefined = True

# Unicode for light on and off emojis
on_emoji = "\U0001F311"  # Electric Light Bulb
off_emoji = "\U0001F315"  # You can replace this with a specific light off emoji


async def TurnAllOn():
    for ip in ips:
        plug = SmartPlug(ip)
        await SetState(plug, True)
    await UpdateUsage()
        
async def TurnAllOff():
    for ip in ips:
        plug = SmartPlug(ip)
        await SetState(plug, False)
    await UpdateUsage()

async def Toggle(ip):
    plug = SmartPlug(ip)
    await plug.update()
    state = plug.is_on
    if state:
        await SetState(plug, False)
    else:
        await SetState(plug, True)
    await UpdateUsage()

def SetAllStates(value):
    for i,tog in enumerate(states):
        states[i]=value
        for ip in ips:
            i = ips.index(ip)
            elements[i][1].config(text=f"{f'{on_emoji}' if states[i] else f'{off_emoji}'}",bg="#000000",fg="#FFFFFF")
   



async def UpdateUsage():
    for ip in ips:
        i = ips.index(ip)
        plug = SmartPlug(ip)
        await plug.update()
        state = plug.emeter_realtime
        elements[i][2].config(text=f"{str(state).split(' ')[1].split('=')[1]}W {str(state).split(' ')[3].split('=')[1]}A {str(state).split(' ')[4].split('=')[1].split('>')[0]}Kwh",bg="#000000",fg="#FFFFFF")


def TurnAllOnBtn():
    SetAllStates(True)
    asyncio.run(TurnAllOn())

def TurnAllOffBtn():
    SetAllStates(False)
    asyncio.run(TurnAllOff())

def ToggleBtn(ip):
    i = ips.index(ip)
    states[i] = not states[i]
    elements[i][1].config(text=f"{f'{on_emoji}' if states[i] else f'{off_emoji}'}")
    asyncio.run(Toggle(ip))


async def discover_devices():
    global ips
    global names
    global predefined
    if predefined:
        ips = open("IPs.txt","r").read().splitlines()
    else:
        ips = ""
        disc = kasa.Discover()
        list = await disc.discover()
        ips = "\n".join(list).splitlines()
    for ip in ips:
        device = SmartPlug(ip)
        await device.update()
        name = device.alias
        state = device.is_on
        names.append(name)
        states.append(state)

    
        

async def SetState(plug,state):
    global ips
    await plug.update()
    name = plug.alias
    id = plug.device_id
    type = plug.device_type
    emeter = plug.emeter_realtime
    #print(f"\"{name}\" {'On' if state else 'Off'}")        
    if state:
        await plug.turn_on()
    else:
        await plug.turn_off()

async def main():
    global ips
    await discover_devices()
    
asyncio.run(main())


# Create the main window
root = tk.Tk()
root.title("Smart Py \U0001F98A")
root.configure(bg="#000000")

fullToggles = tk.Frame(root)
fullToggles.pack(side=tk.LEFT, padx=(10, 10), pady=10)
fullToggles.configure(bg="#000000")

#label = tk.Label(root, text="Main Controls")
#label.pack(padx=(10,10),pady=(10,10))
#label.configure(fg="#FFFF00", bg="#000000")

button = tk.Button(fullToggles, text="Turn All On", command=TurnAllOnBtn)
button.pack(pady=10)

button2 = tk.Button(fullToggles, text="Turn All Off", command=TurnAllOffBtn)
button2.pack(pady=10)

def refresh():
    asyncio.run(UpdateUsage())

button3 = tk.Button(fullToggles, text="Refresh", command=refresh)
button3.pack(pady=10)



individualToggles = tk.Frame(root)
individualToggles.pack(side=tk.LEFT, padx=(10, 10), pady=10)
individualToggles.configure(bg="#000000")

usages = tk.Frame(root)
usages.pack(side=tk.LEFT, padx=(10, 10), pady=10)
usages.configure(bg="#000000")

elements = [[tk.Button(individualToggles, text=f"Toggle {names[i]}", command=partial(ToggleBtn, ip)).pack(side=tk.LEFT), tk.Label(individualToggles, text=f"{f'{on_emoji}' if states[i] else f'{off_emoji}'}"),tk.Label(usages,text="0")] for i, ip in enumerate(ips)]
for ip in ips:
    i = ips.index(ip)
    elements[i][1].pack(side=tk.LEFT)
    elements[i][1].config(bg="#000000",fg="#FFFFFF")
    elements[i][2].pack(side=tk.TOP)
    elements[i][2].config(bg="#000000",fg="#FFFFFF")
# Run the main loop
root.mainloop()