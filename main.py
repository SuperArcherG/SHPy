#!/usr/bin/env python3
from os import environ, getcwd as cwd
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import os, sys, tkinter as tk, asyncio, kasa, pygame.mixer, signal
from distutils import dir_util
from tkinter import PhotoImage, Button, Label, Canvas, Tk, ttk, simpledialog
from PIL import Image, ImageTk, ImageOps
from kasa import SmartPlug
from functools import partial

async def sendMessage(text):
    print(text)

async def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

async def rename_device(i):
    current_string = label_vars[i].get()
    new_string = simpledialog.askstring("Rename String", "Enter a new name:", initialvalue=current_string)
    if new_string:
        label_vars[i].set(new_string)
        #print(label_vars[i].get())
        asyncio.run(rename_devicea(label_vars[i].get(),i))
        await sendMessage(text=f"Renamed device \"{current_string}\" to \"{new_string}\"")
        await restart_program()
        

async def rename_devicea(name,i):
    device = SmartPlug(ips[i])
    await device.update()
    await device.set_alias(name)
   
def run_async_task(coroutine):
    """Run the given coroutine in the asyncio event loop."""
    asyncio.run_coroutine_threadsafe(coroutine, asyncio.get_event_loop()) 
    
def cleanup():
    pygame.mixer.quit()
    sys.exit()

# def signal_handler(sig, frame):
#     #print(f"Received signal: {sig}")
#     cleanup()

# signal.signal(signal.SIGINT, signal_handler)

# def ToggleID(id):
#     return

def quitGame(event):
    cleanup()

# def set_brightness(brightness):
#     brightness = '/sys/class/backlight/intel_backlight/brightness'
#     max_brightness = '/sys/class/backlight/intel_backlight/max_brightness'

#     if not os.path.exists(brightness) or not os.path.exists(max_brightness):
#         print("Brightness control file(s) not found.")
#         return
#     try:
#         with open(max_brightness, 'w') as max_brightness_file:
#             max_brightness_file.read

#         with open(brightness, 'w') as brightness_file:
#             brightness_file.write(str(brightness))
#         print(f'Screen brightness set to {brightness}')
#     except Exception as e:
#         print(f'Error setting brightness: {e}')

# set_brightness(19200)
# sys.exit()

ips = ""
names = []
useage = []
states = []
useage_display_state = 0
predefined = True

async def Toggle(ip,i):
    plug = SmartPlug(ip)
    await plug.update()
    state = plug.is_on
    if state:
        await SetState(plug, False,i=i)
    else:
        await SetState(plug, True, i=i)
    await UpdateUsage()

async def UpdateImages():
    global ips
    print(ips)
    for i,ip in enumerate(ips):
        plug = SmartPlug(ip)
        await plug.update()
        print(i)
        await SetState(plug, plug.is_on, i)
  

async def ToggleBtn(ip,i):
    play(blip_sound_path)
    i = ips.index(ip)
    states[i] = not states[i]
    await Toggle(ip,i)

def syncUpdateUsage(event):
    syncUpdateUseage2()
    
def syncUpdateUseage2():
    print("Updating Useage")
    asyncio.run(UpdateUsage())
 
async def UpdateUsage():
    for ip in ips:
        i = ips.index(ip)
        plug = SmartPlug(ip)
        await plug.update()
        energy_module = plug.modules["Energy"]  # Access the Energy module
        state = await energy_module.get_status()    # Use the appropriate method to fetch real-time data
        print(f"Updating Useage {i} {ip}")
        useage[i] = [f"{str(state).split(' ')[1].split('=')[1]}W",f"{str(state).split(' ')[3].split('=')[1]}A",f"{str(state).split(' ')[4].split('=')[1].split('>')[0]}Kwh"]
        elements[i][2].config(text=useage[i][useage_display_state],bg="#000000",fg="#FFFFFF")
    root.update()

async def discover_devices():
    global ips
    global names
    global useage
    global predefined
    if predefined:
        await sendMessage(text=f"Loading Predefined IPs")
        ips = open("IPs.txt","r").read().splitlines()
    else:
        await sendMessage(text=f"Discovering Devices")
        ips = ""
        disc = kasa.Discover()
        list = await disc.discover()
        ips = "\n".join(list).splitlines()
        await sendMessage(text=f"Devices Found: {ips}")
    for ip in ips:
        device = SmartPlug(ip)
        await device.update()
        name = device.alias
        state = device.is_on
        names.append(name)
        states.append(state)
        useage.append(["N/A","N/A","N/A"])

async def main():
    await sendMessage(text=f"Starting Program")
    global ips
    await discover_devices()
    await initiateIconManager()

async def initiateIconManager():
    await sendMessage(text=f"Starting Icon Manager")
    for ip in ips:
        dir = cwd()+"/sip/"+str(ip)
        if os.path.exists(dir):
            #print("Exists",ip)
            return
        else:
            file = open(dir, 'w')
            file.write("0")
            file.close()
            print("Created",ip)

def play(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

# commandsForIR = {
#     "FF6897" : ToggleID(0), #0
#     "FF30CF" : ToggleID(1), #1
#     "FF18E7" : ToggleID(2), #2
#     "FF7A85" : ToggleID(3), #3
#     "FF10EF" : ToggleID(4), #4
#     "FF38C7" : ToggleID(5), #5
#     "FF5AA5" : ToggleID(6), #6
#     "FF42BD" : ToggleID(7), #7
#     "FF4AB5" : ToggleID(8), #8
#     "FF52AD" : ToggleID(9)  #9
# }

asyncio.run(main())

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

scale = 1
window_width = round(480 * scale)
window_height = round(800 * scale)
xsize,ysize= window_width,window_height

root = Tk()
root.overrideredirect(True)
root.title("SHPy")
pygame.mixer.init()

canvas = Canvas(root, width=window_width, height=window_height)
canvas.pack()

root.geometry(f"{window_width}x{window_height}")

background_image_path = cwd() + "/Assets/BG.png"
button_image_path = cwd() + "/Assets/b.png"
power_image_path = cwd() + "/Assets/pow.png"
frame_image_path = cwd() + "/Assets/SmallFrame.png"
plon_image_path = cwd() + "/Assets/0on.png"
ploff_image_path = cwd() + "/Assets/0off.png"
lon_image_path = cwd() + "/Assets/1on.png"
loff_image_path = cwd() + "/Assets/1off.png"
fon_image_path = cwd() + "/Assets/2on.png"
foff_image_path = cwd() + "/Assets/2off.png"
unknown_image_path = cwd() + "/Assets/q.png"
edit_image_path = cwd() + "/Assets/edit.png"
question_image_path = cwd() + "/Assets/q.png"
blip_sound_path = cwd() + "/Assets/blip.wav"
startup_sound_path = cwd() + "/Assets/startup.mp3"

buttonsize = round(window_width/8)
iconsize = round(window_width/8/2)
powsize = round(window_width/6)
framesize = round(0.8*window_width),round(0.8*window_height)
framePos = round(window_width * 4/7), window_height // 2
framePosOffset = (round(window_width * 4/7 - framesize[0]/2), window_height // 2 - round(framesize[1]/2))

button_image = ImageTk.PhotoImage(Image.open(button_image_path).resize((buttonsize,buttonsize)))
plon_image = ImageTk.PhotoImage(Image.open(plon_image_path).resize((iconsize,iconsize)))
ploff_image = ImageTk.PhotoImage(Image.open(ploff_image_path).resize((iconsize,iconsize)))
lon_image = ImageTk.PhotoImage(Image.open(lon_image_path).resize((iconsize,iconsize)))
loff_image = ImageTk.PhotoImage(Image.open(loff_image_path).resize((iconsize,iconsize)))
fon_image = ImageTk.PhotoImage(Image.open(fon_image_path).resize((iconsize,iconsize)))
foff_image = ImageTk.PhotoImage(Image.open(foff_image_path).resize((iconsize,iconsize)))
unknown_image = ImageTk.PhotoImage(Image.open(unknown_image_path).resize((iconsize,iconsize)))
power_image = ImageTk.PhotoImage(Image.open(power_image_path).resize((powsize,powsize)))
frame_image = ImageTk.PhotoImage(Image.open(frame_image_path).resize(framesize))
background_image = ImageTk.PhotoImage(Image.open(background_image_path).resize((xsize, ysize)))
edit_image = ImageTk.PhotoImage(Image.open(edit_image_path).resize((iconsize, iconsize)))
question_image = ImageTk.PhotoImage(Image.open(question_image_path).resize((iconsize,iconsize)))


iconsbyid = {
    0 : {
        "on" : plon_image,
        "off" : ploff_image
    },
    1 : {
        "on" : lon_image,
        "off" : loff_image
    },
    2 : {
        "on" : fon_image,
        "off" : foff_image
    },
}
async def SetState(plug,state,i = 0):
    global ips
    await plug.update()
    name = plug.alias
    id = plug.device_id
    type = plug.device_type
    emeter = plug.emeter_realtime
    await sendMessage(text=f"Setting {name}{id} to {state} : Device Type: {type}, Emeter: {emeter}")
    dir = cwd()+"/sip/"+str(ips[i])
    file = open(dir, 'r')
    iconid = int(file.read()[0])
    imageSet = iconsbyid[iconid]
    #print(f"\"{name}\" {'On' if state else 'Off'}")        
    if state:
        elements[i][0].config(image=imageSet["on"])
        await plug.turn_on()
    else:
        elements[i][0].config(image=imageSet["off"])
        await plug.turn_off()

def create_toggle_command(ip, i):
    def toggle():
        loop = asyncio.get_event_loop()
          # Schedule the coroutine
    return toggle

def ToggleBtnAsyncFix(ip,i):
    asyncio.run(ToggleBtn(ip,i))

canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
canvas.create_image(round(window_width * 4/7), window_height // 2, anchor=tk.CENTER, image=frame_image)
loop.run_until_complete(sendMessage("Loading UI"))
elements = [
    [
        Button(canvas, image = unknown_image, width=buttonsize,height=buttonsize, command=partial(ToggleBtnAsyncFix,ip, i),borderwidth=0, highlightthickness=0,bg="#5b6d99"), # type: ignore
        Label(text=f"{names[i]}",bg="#15555A",font=("Source Code Pro", round(25*scale),"bold"),fg="#00ffff"),
        Label(text=f"{useage[i][useage_display_state]}",bg="#15555A",font=("Source Code Pro", round(25*scale),"bold"),fg="#00ffff"),
        # Button(canvas, image = edit_image, command=partial(rename_device,i),bg="#00ffff",borderwidth=0, highlightthickness=0) # type: ignore
    ]
    for i,ip in enumerate(ips)
]
for i,ip in enumerate(ips):
    elements[i][0].place(x=framePosOffset[0]+buttonsize/2+20*scale,y=framePosOffset[1]+buttonsize/2+20*scale+(buttonsize+15*scale)*i, anchor="center")
    elements[i][1].place(x=0,y=0, anchor="center")
    #canvas.coords(elements[i][2],framePosOffset[0]+buttonsize/2+15,80)
    root.update()
    elements[i][1].place(x=framePosOffset[0]+buttonsize/2+buttonsize+elements[i][1].winfo_width()/2,y=framePosOffset[1]+buttonsize/2+20*scale+(buttonsize+15*scale)*i, anchor="center")
    elements[i][2].place(x=framePosOffset[0]+buttonsize/2+buttonsize+elements[i][1].winfo_width()+iconsize/2,y=framePosOffset[1]+iconsize/2+20*scale+(buttonsize+15*scale)*i)
label_vars = [tk.StringVar(value=f"{names[i]}") for i,ip in enumerate(ips)]

loop.run_until_complete(UpdateImages())
play(startup_sound_path)


button = canvas.create_image(window_width,0,anchor=tk.NE,image=power_image)
canvas.tag_bind(button, "<Button-1>", quitGame)

button2 = canvas.create_image(0,0,anchor=tk.NW,image=question_image)
canvas.tag_bind(button2, "<Button-2>", syncUpdateUsage)

loop.run_until_complete(sendMessage("Successfully Loaded!"))
loop.run_until_complete(sendMessage("Running Main Loop"))
root.mainloop()