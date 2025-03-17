#!/usr/bin/env python3
from os import environ, getcwd as cwd
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import os, sys, tkinter as tk, asyncio, kasa, pygame.mixer, signal
from distutils import dir_util
from tkinter import PhotoImage, Button, Label, Canvas, Tk, ttk, simpledialog
from PIL import Image, ImageTk, ImageOps
from functools import partial

SOUND = False

async def sendMessage(text):
    print(text)

async def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)
   
def run_async_task(coroutine):
    """Run the given coroutine in the asyncio event loop."""
    asyncio.run_coroutine_threadsafe(coroutine, asyncio.get_event_loop()) 
    
def cleanup():
    pygame.mixer.quit()
    sys.exit()

def quitGame(event):
    cleanup()

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