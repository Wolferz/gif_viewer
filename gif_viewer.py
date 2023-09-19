import tkinter as tk

import PIL.Image
from PIL import ImageTk, Image, ImageSequence
import os

offline_gifs_path: str = "testing/gif/"

master = tk.Tk()
master.state('zoomed')
def resize_image(image: Image, max_width=2048, max_height=1080): # TODO Causes massive color quality drop
    try:
        if img_lbl.winfo_height() < max_height:
            max_height = master.winfo_height()-(ctrl_frm.winfo_height() + rate_entry.winfo_height())
    except NameError:
        pass
    og_width = image.size[0]
    og_height = image.size[1]
    ratio = min(max_width / og_width, max_height / og_height)
    return image.resize((int(og_width * ratio), int(og_height * ratio)),resample=PIL.Image.Resampling.LANCZOS)
def prepare_gif(gif_file: str):
    img_data = Image.open(gif_file)
    frames_list = ImageSequence.all_frames(img_data)
    frame_images = []

    for each_frame in frames_list:
        frame_images.append(ImageTk.PhotoImage(resize_image(each_frame)))

    return frames_list,frame_images

album = []
count = 0


for gif in os.listdir(offline_gifs_path):
    count+=1
    print(count,"/",len(os.listdir(offline_gifs_path)))
    album.append(offline_gifs_path+"/"+gif)

frame = 0

current_gif = 0
next_gif = prepare_gif(album[current_gif])
frame_data, frame_list = next_gif[1], next_gif[0]
playing = True
frame_reset = True
def animate(current_frame):
    global frame_reset
    current_frame +=1
    if frame_reset:
        current_frame = 0
        frame_reset = False

    if current_frame > len(frame_data)-1:
        current_frame = 0
    img_lbl.config(image=frame_data[current_frame])
    if rate_entry.get != 0:
        try:
            delay = int(frame_list[current_frame].info['duration'] / (rate_entry.get()+0.1))
        except KeyError:
            delay = 1
    else:
        delay = 1000
    if delay != 0:
        fr = round(1000 / delay)
    else:
        fr = 0
    data = (str(fr), str(current_frame + 1),str(len(frame_list)), str(current_gif + 1), str(len(album)))
    rate_entry.config(label='FPS: {}    Frame: {}/{}    Image: {}/{}'.format(data[0],data[1],data[2],data[3],data[4]))
    if playing:
        master.after(delay,animate,current_frame)

def change_img(ch):
    global current_gif, frame_data, frame_list, frame_reset, next_gif, playing
    if 0 <= (current_gif + ch) < len(album):
        if playing:
            play_pause()
        current_gif += ch
        next_gif = prepare_gif(album[current_gif])
        rate_entry.set(1)
        frame_list, frame_data, frame_reset = next_gif[0], next_gif[1], True
        master.after(500,play_pause)

def play_pause():
    global playing
    if playing:
        playing = False
        play_btn.config(text='Play')
    else:
        playing = True
        play_btn.config(text="Pause")
        master.after(10,animate,0)


rate_entry = tk.Scale(master,from_=0,to=2,orient=tk.HORIZONTAL,resolution=0.25,tickinterval=0.25,length=300,label='FPS: 0')
rate_entry.set(1)
img_lbl = tk.Label(master, image=frame_data[0])
ctrl_frm = tk.Frame(master)
prev_btn = tk.Button(ctrl_frm, text="Previous", width=30,command=lambda:change_img(-1))
play_btn = tk.Button(ctrl_frm, text='Pause',command=play_pause)
next_btn = tk.Button(ctrl_frm, text="Next", width=30,command=lambda:change_img(1))
prev_btn.pack(side='left')
play_btn.pack(side='left')
next_btn.pack(side='left')
ctrl_frm.pack(side='top')
rate_entry.pack(side='top')
img_lbl.pack(side='top')
master.after(10,animate,frame)
master.mainloop()
