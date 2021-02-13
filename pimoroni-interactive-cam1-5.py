# My pimoroni interactive Camera App
# Version 1.5
# Changes since version 1.1: Preview on/off option added, app now starts with preview window off and
# initial preview window starts at 640x480
# Created By David Peck
# Some of the code has been modified from various web sources
# Created Jan-2021
# App for using Pimoroni Pan/Tilt Hat and V1, V2 of raspberry Pi Camera and the Arducam mini HQ Camera
# File Name: pimoroni-interactive-cam.py

from guizero import App, PushButton, Slider, Text, Combo
import colorsys
import picamera
import time
import pantilthat
import datetime
from time import sleep

# Initialise PanTilt Hat
a = 0 # intitial pan position (center)
b = -20 # intitial tilt position (center)
r = 0 # neopixel red off
g = 0 # neopixel green off
b = 0 # neopixel blue off
w = 0 # neopixel white off

pantilthat.light_mode(pantilthat.WS2812)
pantilthat.light_type(pantilthat.GRBW)
pantilthat.pan(a)    
pantilthat.tilt(b)
pantilthat.set_all(r, g, b, w)
pantilthat.show()

# Initialise Camera
camera = picamera.PiCamera()
win_size = (500, 40, 640, 480)
x = 0 # set zoom to zero
y = 0 # set zoom to zero
video = (1920, 1088)
photo = (2592, 1944)
framerate = 30
rotate = 180
effect_value = "none"
camera.exposure_mode = "auto"
camera.awb_mode = "auto"
camera.rotation = rotate
camera.resolution = photo
camera.zoom = (x, x, y, y)
camera.image_effect = effect_value

# Turn Preview On and update text and buttons
def preview_on():
    global window
    global win_size
    preview_ontxt.bg="lightgreen"
    preview_offtxt.bg="lightgrey"
    camera.start_preview(fullscreen=False, window = (win_size))
    current_size = Text(app, text=str(win_size[2:]), width=12, color="red", grid=[5,2], align="left")

# Turn Preview Off and update text and buttons
def preview_off():
    camera.stop_preview()
    preview_ontxt.bg="lightgrey"
    preview_offtxt.bg="pink"
    current_size = Text(app, text=("OFF"), width=12, color="red", grid=[5,2], align="left")

# Set selected Preview window size
def preview_size():
    global window
    global win_size
    
    if preview_set.value =="640x480":
        win_size = (500, 50, 640, 480)
        camera.start_preview(fullscreen=False, window = (win_size))
        current_size = Text(app, text=str(win_size[2:]), width=12, color="red", grid=[5,2], align="left")
    
    if preview_set.value =="720x576":
        win_size = (500, 40, 720, 576)
        camera.start_preview(fullscreen=False, window = (win_size))       
        current_size = Text(app, text=str(win_size[2:]), width=12, color="red", grid=[5,2], align="left")
        
    if preview_set.value =="720x480":
        win_size = (490, 60, 720, 480)
        camera.start_preview(fullscreen=False, window = (win_size))
        current_size = Text(app, text=str(win_size[2:]), width=12, color="red", grid=[5,2], align="left")
    
    if preview_set.value =="1280x720":
        win_size = (300,30, 1280, 720)
        camera.start_preview(fullscreen=False, window = (win_size))
        current_size = Text(app, text=str(win_size[2:]), width=12, color="red", grid=[5,2], align="left")

# Set camera image rotation
def camera_rotation():
    camera.rotation = rotation_set.value
    current_rotation = Text(app, text=str(camera.rotation), width=10, color="red",grid=[3,13], align="left")  

# Define Zoom Settings
def zoom_set():
        
    if set_zoom.value == "Zoom-0":
        x = 0
        y = 0
        camera.zoom = (x, x, y, y)
        current_zoom = Text(app, text="Zoom-0", width=10, color="red", grid=[2,13], align="left")
    
    if set_zoom.value == "Zoom-1":
        x = 0.25
        y = 0.5
        camera.zoom = (x, x, y, y)
        current_zoom = Text(app, text="Zoom-1", width=10, color="red", grid=[2,13], align="left")
       
    if set_zoom.value == "Zoom-2":
        x = 0.5
        y = 0.25
        camera.zoom = (x, x, y, y)
        current_zoom = Text(app, text="Zoom-2", width=10, color="red", grid=[2,13], align="left")

# Set various Image effects
def set_effects():    
    global effect_value
    
    effect_value = str(effect_set.value)
    camera.image_effect = effect_value
    current_effect = Text(app, text=(camera.image_effect), width=10, color="red", grid=[4,13], align="left")

# Set Exposure mode
def set_exposure():
    exposure_value = str(exposure_set.value)
    camera.exposure_mode = exposure_value
    current_exposure = Text(app, text=(camera.exposure_mode), width=10, color="red", grid=[5,13], align="left")

# Set white balance
def set_awb():
    awb_value = str(awb_set.value)
    camera.awb_mode = awb_value
    current_awb = Text(app, text=(camera.awb_mode), width=10, color="red", grid=[6,13], align="left")

# Define Camera Recording Resolution 
def record_res():
    global photo
    global video
    global window
    global win_size
    
    if res_record.value =="V1-photo":
        photo = (2592, 1944)
        camera.resolution= photo
        photores_txt = Text(app, text=str(camera.resolution),width=10, color="red", grid=[1,8], align="left") 
        camera_type_txt = Text(app, text=" V1-Camera", color="red", grid=[1,9], align="left")
        preview_ontxt.bg="lightgreen"
        preview_offtxt.bg="lightgrey"
        camera.start_preview(fullscreen=False, window = (win_size))
        current_size = Text(app, text=str(win_size[2:]), width=12, color="red", grid=[5,2], align="left")
    
    if res_record.value =="V2-photo":
        photo = (3280,2464)
        camera.resolution= photo
        photores_txt = Text(app, text=str(camera.resolution), width=10, color="red", grid=[1,8], align="left") 
        camera_type_txt = Text(app, text=" V2-Camera", color="red", grid=[1,9], align="left")
        preview_ontxt.bg="lightgreen"
        preview_offtxt.bg="lightgrey"
        camera.start_preview(fullscreen=False, window = (win_size))
        current_size = Text(app, text=str(win_size[2:]), width=12, color="red", grid=[5,2], align="left")
    
    if res_record.value == "HQ-photo":
        photo = (4056, 3040)
        camera.resolution= photo
        photores_txt = Text(app, text=str(camera.resolution), width=10, color="red", grid=[1,8], align="left") 
        camera_type_txt = Text(app, text=" HQ-Camera", color="red", grid=[1,9], align="left")
        preview_ontxt.bg="lightgreen"
        preview_offtxt.bg="lightgrey"
        camera.start_preview(fullscreen=False, window = (win_size))
        current_size = Text(app, text=str(win_size[2:]), width=12, color="red", grid=[5,2], align="left")
        
    if res_record.value =="1080p":
        video = (1920, 1080)
        framerate = 30
        camera.resolution = video
        vidres_txt = Text(app, text= str(camera.resolution), width=10,  color="red", grid=[2,8], align="left")
        vidframe_txt = Text(app, text=str(framerate) + " fps", width=10, color="red", grid=[2,9], align="left")
        preview_ontxt.bg="lightgreen"
        preview_offtxt.bg="lightgrey"
        camera.start_preview(fullscreen=False, window = (win_size))
        current_size = Text(app, text=str(win_size[2:]), width=12, color="red", grid=[5,2], align="left")
        
    
    if res_record.value =="720p":
        video = (1280, 720)
        camera.resolution = video
        framerate = 60
        vidres_txt = Text(app, text=str(camera.resolution), width=10, color="red", grid=[2,8], align="left")
        vidframe_txt = Text(app, text=str(framerate) + " fps", width=10, color="red", grid=[2,9], align="left")
        preview_ontxt.bg="lightgreen"
        preview_offtxt.bg="lightgrey"
        camera.start_preview(fullscreen=False, window = (win_size))
        current_size = Text(app, text=str(win_size[2:]), width=12, color="red", grid=[5,2], align="left")
        
    
    if res_record.value =="576p":
        video = (720, 576)
        camera.resolution = video
        framerate = 25
        vidres_txt = Text(app, text=str(camera.resolution), width=10, color="red", grid=[2,8], align="left")
        vidframe_txt = Text(app, text=str(framerate) + " fps", width=10, color="red", grid=[2,9], align="left")
        preview_ontxt.bg="lightgreen"
        preview_offtxt.bg="lightgrey"
        camera.start_preview(fullscreen=False, window = (win_size))
        current_size = Text(app, text=str(win_size[2:]), width=12, color="red", grid=[5,2], align="left")
       
    
    if res_record.value =="480p":
        video = (720, 480)
        camera.resolution = video
        framerate = 60
        vidres_txt = Text(app, text=str(camera.resolution), width=10, color="red", grid=[2,8], align="left")
        vidframe_txt = Text(app, text=str(framerate) + " fps", width=10, color="red", grid=[2,9], align="left")
        preview_ontxt.bg="lightgreen"
        preview_offtxt.bg="lightgrey"
        camera.start_preview(fullscreen=False, window = (win_size))
        current_size = Text(app, text=str(win_size[2:]), width=12, color="red", grid=[5,2], align="left")
     
    current_res = Text(app, text=str(camera.resolution), width=10, color="red", grid=[1,13], align="left") 

# Record Video
def video_record():
    global video
    camera.resolution = video
    camera.framerate = framerate
    vid_record.text="Recording   "
    vid_record.bg="pink"
    vid_record.text_color="red"
    record_stop.text_color="red"
    record_stop.text="press to Stop"
    date = datetime.datetime.now().strftime('%d-%m-%Y_%H.%M.%S')
    camera.start_recording('/home/pi/Videos/video_' + date + '.h264') 
    
# Stop Video Record    
def record_stop():
    vid_record.text="Video Record"
    vid_record.text_color="black"
    vid_record.bg="lightblue"
    record_stop.text_color="black"
    record_stop.text="Record Stop"
    camera.stop_recording()
  
# Capture Image (Take Photo)    
def image_capture():
    camera.resolution=photo
    date = datetime.datetime.now().strftime('%d-%m-%Y_%H.%M.%S')
    camera.capture('/home/pi/Pictures/image_' + date + '.jpg') 
    
# Adjust Pan and Tilt Position        
def set_pan_tilt():
        global a
        a = pan_set.value    
        b = tilt_set.value
        pantilthat.pan(a)    
        pantilthat.tilt(b)
        
# Set Neopixel Color and Intensity
def color_set():
    global r
    global g
    global b
    global w
    
    r = red_select.value
    g = green_select.value
    b = blue_select.value
    w = white_select.value
    
    pantilthat.set_all(r, g, b, w)
    pantilthat.show()

# Reset Pan and Tilt Position
def position_reset():
    pan_set.value = 0
    tilt_set.value = -20


# Exit Program
def exit_program():
    pantilthat.set_all(0, 0, 0, 0)
    pantilthat.show()
    pantilthat.pan(0)    
    pantilthat.tilt(-20)
    exit()


# GUI Setings
app = App(bg ="lightgrey",  title="Pimoroni Interactive Cam V1.5", width=1050,  height=400, layout="grid")

pan_txt = Text(app, text="R           Pan             L", width=17, grid=[1,0], align="left")
pan_txt.text_color="blue"

position_txt = Text(app, text="Postition", width=10, color="blue", grid=[0,1], align="left")

pan_set = Slider(app, command=set_pan_tilt, start=-90, end=90, width=150, height=15, grid=[1,1], align="left") # sets pan value
pan_set.value = 0
pan_set.bg="yellow"

reset_position = PushButton(app, command=position_reset, text="Position Reset", width=14, grid=[2,1], align="left")
reset_position.text_color="blue"

tilt_txt = Text(app, text="U         Tilt               D", width=17, grid=[3,0], align="left")
tilt_txt.text_color="blue"

tilt_set = Slider(app, command=set_pan_tilt, start=-90, end=90, width=150, height=15, grid=[3,1], align="left") # sets tilt value
tilt_set.value = -20
tilt_set.bg="yellow"

lights_txt = Text(app, text="Lighting", width=10, color="blue", grid=[0,4], align="left")

red_txt = Text(app, text="          RED", width=10, grid=[1,3], align="left") #
red_txt.bg="lightgrey"

green_txt = Text(app, text="        GREEN", width=10, grid=[2,3], align="left")
green_txt.bg="lightgrey"

blue_txt = Text(app, text="        BLUE", width=10, grid=[3,3], align="left")
blue_txt.bg="lightgrey"

white_txt = Text(app, text="         WHITE", width=10, grid=[4,3], align="left")
white_txt.bg="lightgrey"

red_select = Slider(app, command=color_set, start=0, end=255, width=150, grid=[1,4], align="left") # sets red neopixel
red_select.bg="pink"

green_select = Slider(app, command=color_set, start=0, end=255, width=150, grid=[2,4], align="left") # sets green neopixel
green_select.bg="lightgreen"

blue_select = Slider(app, command=color_set, start=0, end=255, width=150, grid=[3,4], align="left") # sets blue neopixel
blue_select.bg="lightblue"

white_select = Slider(app, command=color_set, start=0, end=255, width=150, grid=[4,4], align="left") # sets white neopixel
white_select.bg="white"

pad_txt = Text(app, text="       ", grid=[0,5], align="left")

options_txt = Text(app, text="Options", width=10, color="blue", grid=[0,7], align="left")

pic_capture = PushButton(app, command=image_capture, text="Take Photo", width=10, grid=[1,7], align="left") # capture image
pic_capture.bg="lightblue"

photores_txt = Text(app, text="  2592x1944", color="green", width=10, grid=[1,8], align="left") # displays image resolution

camera_type_txt = Text(app, text=" V1-Camera", color="green", width=10, grid=[1,9], align="left")

vid_record = PushButton(app, command=video_record, text="Video Record", width=10, grid=[2,7], align="left") # starts video recording
vid_record.text_color="black"
vid_record.bg="lightblue"

vidres_txt = Text(app, text="   1920x1080", width=10, color="green", grid=[2,8], align="left")
vidframe_txt = Text(app, text="      " + str(framerate) + " fps", width=10, color="green", grid=[2,9], align="left")

record_stop = PushButton(app, command=record_stop, text="Record Stop", width=10, grid=[3,7], align="left") # stop video recording
record_stop.bg="lightblue"

preview_txt = Text(app, text="Preview On/Off", color="blue", width=20, grid=[4,6], align="left")
preview_ontxt = PushButton(app, command=preview_on, width=5, text="On", grid=[4,7], align="right")
preview_ontxt = PushButton(app, command=preview_on, width=5, text="On", grid=[4,7], align="right")
preview_ontxt.text_color="blue"

preview_offtxt = PushButton(app, command=preview_off, width=5, text="Off", grid=[4,7], align="left")
preview_offtxt.text_color="blue"
preview_offtxt.bg="pink"

pad_txt = Text(app, text="       ", grid=[0,10], align="left")

preview_txt = Text(app, text="Preview", width=10, color="blue", grid=[1,11], align="left")

res_record= Combo(app, command=record_res, options=["V1-photo", "V2-photo", "HQ-photo", "1080p", "720p", "576p", "480p"], width=6, grid=[1,12], align="left") # sets video resolution
res_record.text_color="blue"
current_res = Text(app, text="2592x1944", width=10, color="green", grid=[1,13], align="left")

zoom_txt = Text(app, text="Zoom", width=10, color="blue", grid=[2,11], align="left")
set_zoom = Combo(app, command=zoom_set, options=["Zoom-0", "Zoom-1", "Zoom-2"], width=6, grid=[2,12], align="left") # sets zoom level
set_zoom.text_color="blue"
current_zoom = Text(app, text="Zoom-0", color="green", width=10, grid=[2,13], align="left")

rotate_txt = Text(app, text="Rotation  ", color="blue", width=10, grid=[3,11], align="left")
rotation_set = Combo(app, command=camera_rotation, options=["180", "90", "0"], width=6, grid=[3,12], align="left")
rotation_set.text_color="blue"
current_rotation = Text(app, text=str(camera.rotation), width=10, color="green",grid=[3,13], align="left")

effects_txt = Text(app, text="Effects", width=12, color="blue", grid=[4,11], align="left")
effect_set = Combo(app, command=set_effects, options=["none", "negative", "solarize", "sketch", "denoise", "emboss", "oilpaint", "hatch", "gpen", "pastel", "watercolor", "film", "blur", "saturation", "colorswap", "washedout", "posterise", "colorpoint", "cartoon", "deinterlace1", "deinterlace2"], width=10, grid=[4,12], align="left")
effect_set.text_color="blue"
current_effect = Text(app, text=str(camera.image_effect), width=10, color="green", grid=[4,13], align="left")

exposure_txt = Text(app, text="Exposure",  width=10, grid=[5,11], align="left")
exposure_txt.text_color="blue"
exposure_set = Combo(app, command=set_exposure, options=["auto", "off", "night", "nightpreview", "backlight", "spotlight", "sports", "snow", "beach", "verylong", "fixedfps", "antishake", "fireworks"], width=10, grid=[5,12], align="left")
exposure_set.text_color="blue"
current_exposure = Text(app, text=str(camera.exposure_mode), width=10, color="green", grid=[5,13], align="left")
                        
awb_txt = Text(app, text="AWB", width=10, grid=[6,11], align="left")
awb_txt.text_color="blue"
awb_set = Combo(app, command=set_awb, options=["auto", "off", "sunlight", "cloudy", "shade", "tungsten", "fluorescent", "incandescent", "flash", "horizon"], width=10, grid=[6,12], align="left")
awb_set.text_color="blue"
current_awb = Text(app, text=(camera.awb_mode), width=10, color="green", grid=[6,13], align="left")

Preview_wintxt = Text(app, text="Preview Size", width=12, color="blue", grid=[5,0], align="left")
preview_set = Combo(app, command=preview_size, options=["640x480", "720x480", "720x576", "1280x720"], width=8, grid=[5,1], align="left")
preview_set.text_color="blue"
current_size = Text(app, text="OFF", width=12, color="green", grid=[5,2], align="left")

exit_prog = PushButton(app, command=exit_program, text="Quit Program", width=15, grid=[6,1], align="left")
exit_prog.text_color="blue"
exit_prog.bg="pink"

app.display()