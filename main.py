import PIL.Image
import PIL.ImageTk
import numpy as np

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter.messagebox import showinfo

from SkImage import SkImage

# Upload an image function
def upload():

    filetypes = (
        ('JPG Images', '*.jpg'),
        ('JPEG Images', '*.jpeg'),
        ('PNG Images', '*.png'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Select an image',
        filetypes=filetypes)

    # Set SkImage class attributes
    skIm.path = filename
    skIm.tk_img = PIL.ImageTk.PhotoImage(PIL.Image.open(filename))
    skIm.img = PIL.Image.open(filename)
    skIm.img_origin = PIL.Image.open(filename)
    skIm.np_arr = np.array(skIm.img)
    skIm.non_rotated = skIm.np_arr

    update_image()

    configure_buttons()


# Reset image to original state
def reset_image():
    skIm.img = skIm.img_origin
    skIm.np_arr = np.array(skIm.img)
    skIm.tk_img = PIL.ImageTk.PhotoImage(skIm.img)
    skIm.non_rotated = skIm.np_arr
    skIm.degrees = 0
    update_image()


# REFLECTING
def reflect(means):
    skIm.reflect(means)
    update_image()

def reflect_handler():
    reflect_win = Toplevel(window) # Create new window

    reflect_win.title("Reflect Image")
    reflect_win.geometry("200x100")
 
    Label(reflect_win, text="Horizontally or Vertically?").pack()

    reflect_btn = Button(reflect_win, text="Horizontal", command=lambda: reflect("hor")) # Horizontal Button
    reflect_btn.place(x=50, y=50, anchor="center")

    reflect_btn = Button(reflect_win, text="Vertical", command=lambda: reflect("ver")) # Vertical Button
    reflect_btn.place(x=150, y=50, anchor="center")


# SCALING
def scale(width, height, maintain_aspect, default_ar):
    if maintain_aspect.get():
        height = int(width/default_ar) # Keep original aspect ratio, set height accordingly
    skIm.scale(width, height)
    update_image()

def scale_ratio(maintain_aspect, scale_width, scale_height):
    if maintain_aspect.get():
        scale_height.config(state="disabled")
    else:
        scale_height.config(state="normal")

def scale_handler():
    scale_win = Toplevel(window) # Create new window
    maintain_aspect = IntVar(scale_win, 0, "maintain_aspect")

    scale_win.title("Scale Image")
    scale_win.geometry("400x200")
 
    Label(scale_win, text="How would you like to scale the image").pack()

    # Get default values for dimension of image
    default_x = str(skIm.np_arr.shape[1])
    default_y = str(skIm.np_arr.shape[0])
    default_ar = (skIm.np_arr.shape[1]/skIm.np_arr.shape[0])

    scale_width = Entry(scale_win, width=4)
    scale_width.place(x=170, y=100, anchor="center")
    scale_width.insert(END, default_x)

    x_lbl = Label(scale_win, text="x")
    x_lbl.place(x=200, y=100, anchor="center")

    scale_height = Entry(scale_win, width=4)
    scale_height.place(x=230, y=100, anchor="center")
    scale_height.insert(END, default_y)

    c1 = Checkbutton(scale_win, text='Maintain Aspect Ratio', variable=maintain_aspect,
            command=lambda: scale_ratio(maintain_aspect, scale_width, scale_height))
    c1.place(x=200, y=50, anchor="center")

    scale_btn = Button(scale_win, text="Scale",
            command=lambda: scale(int(scale_width.get()), int(scale_height.get()), maintain_aspect, default_ar))
    scale_btn.place(x=350, y=170, anchor="center")
    

# ROTATING
def rotate(wise, degrees, mode):
    skIm.rotate(wise, degrees, mode.get())
    update_image()

def toggle_wise(wise, clockwise_btn, c_clockwise_btn, rotate_lbl):
    if wise.get():
        clockwise_btn.config(relief="raised", state="normal")
        c_clockwise_btn.config(relief="sunken", state="disabled")
        rotate_lbl.config(text="Rotating Counter-Clockwise by")
        wise.set(0)
    else:
        clockwise_btn.config(relief="sunken", state="disabled")
        c_clockwise_btn.config(relief="raised", state="normal")
        rotate_lbl.config(text="Rotating Clockwise by")
        wise.set(1)

def rotate_handler():
    rotate_win = Toplevel(window) # Create new window
    wise = IntVar(rotate_win, 1, "wise")

    rotate_win.title("Rotate Image")
    rotate_win.geometry("400x200")
 
    Label(rotate_win, text="How would you like to rotate the image").pack()

    clockwise_btn = Button(rotate_win, text="Clockwise", relief="sunken", state="disabled",
            command=lambda: toggle_wise(wise, clockwise_btn, c_clockwise_btn, rotate_lbl)) # Clockwise
    clockwise_btn.place(x=150, y=50, anchor="center")

    c_clockwise_btn = Button(rotate_win, text="Counter", relief="raised",
            command=lambda: toggle_wise(wise, clockwise_btn, c_clockwise_btn, rotate_lbl)) # Counter Clockwise Button
    c_clockwise_btn.place(x=250, y=50, anchor="center")

    rotate_lbl = Label(rotate_win, text="Rotating Clockwise by")
    rotate_lbl.place(x=200, y=80, anchor="center")

    rotate_degree = Entry(rotate_win, width=3) # Entry input for num of degrees
    rotate_degree.place(x=180, y=110, anchor="center")
    rotate_degree.insert(END, 0)

    rotate_lbl2 = Label(rotate_win, text="degrees")
    rotate_lbl2.place(x=230, y=110, anchor="center")

    rotate_cb = ttk.Combobox(rotate_win)
    rotate_cb.place(x=200, y=130, anchor="center")
    rotate_cb['values'] = ('nearest', 'bilinear', 'shear')
    rotate_cb['state'] = 'readonly'

    rotate_btn = Button(rotate_win, text="Rotate",
            command=lambda: rotate(wise.get(), int(rotate_degree.get()), rotate_cb))
    rotate_btn.place(x=350, y=170, anchor="center")



# CROPPING
def crop(crop_left, crop_right, crop_top, crop_bottom):
    if int(crop_left.get()) < 0 or int(crop_right.get()) < 0 or int(crop_top.get()) < 0 or int(crop_bottom.get()) < 0:
        return 
    skIm.crop(int(crop_left.get()), int(crop_right.get()), int(crop_top.get()), int(crop_bottom.get()))
    update_image()

    # Resetting the entry boxes to 0
    crop_left.delete(0, END)
    crop_right.delete(0, END)
    crop_top.delete(0, END)
    crop_bottom.delete(0, END)
    crop_left.insert(END, 0)
    crop_right.insert(END, 0)
    crop_top.insert(END, 0)
    crop_bottom.insert(END, 0)


def crop_handler():
    crop_win = Toplevel(window) # Create new window

    crop_win.title("Crop Image")
    crop_win.geometry("400x200")
 
    Label(crop_win, text="How would you like to crop the image").pack()

    crop_left = Entry(crop_win, width=3) # Entry input for num of pixels to crop
    crop_left.place(x=90, y=50, anchor="center")
    crop_left.insert(END, 0)

    left_lbl = Label(crop_win, text="pixels to crop off LEFT")
    left_lbl.place(x=110, y=50, anchor="w")


    crop_right = Entry(crop_win, width=3) # Entry input for num of pixels to crop
    crop_right.place(x=90, y=75, anchor="center")
    crop_right.insert(END, 0)

    right_lbl = Label(crop_win, text="pixels to crop off RIGHT")
    right_lbl.place(x=110, y=75, anchor="w")


    crop_top = Entry(crop_win, width=3) # Entry input for num of pixels to crop
    crop_top.place(x=90, y=100, anchor="center")
    crop_top.insert(END, 0)

    top_lbl = Label(crop_win, text="pixels to crop off TOP")
    top_lbl.place(x=110, y=100, anchor="w")

    crop_bottom = Entry(crop_win, width=3) # Entry input for num of pixels to crop
    crop_bottom.place(x=90, y=125, anchor="center")
    crop_bottom.insert(END, 0)

    bottom_lbl = Label(crop_win, text="pixels to crop off BOTTOM")
    bottom_lbl.place(x=110, y=125, anchor="w")

    scale_btn = Button(crop_win, text="Crop",
            command=lambda: crop(crop_left, crop_right, crop_top, crop_bottom))
    scale_btn.place(x=350, y=170, anchor="center")


# BRIGHTNESS
def bright(bias):
    skIm.brightness(int(bias.get()))
    update_image()

def bright_handler():
    bright_win = Toplevel(window) # Create new window

    bright_win.title("Brighten Image")
    bright_win.geometry("200x100")

    bright_entry = Entry(bright_win, width=3) # Entry input for value of gain
    bright_entry.place(x=90, y=40, anchor="center")
    bright_entry.insert(END, 0)

    bias_lbl = Label(bright_win, text="bias")
    bias_lbl.place(x=110, y=40, anchor="w")

    bright_btn = Button(bright_win, text="Apply",
            command=lambda: bright(bright_entry))
    bright_btn.place(x=150, y=70, anchor="center")

# CONTRAST
def contrast(gain):
    skIm.contrast(float(gain.get()))
    update_image()

def contrast_handler():
    contrast_win = Toplevel(window) # Create new window

    contrast_win.title("Contrast Image")
    contrast_win.geometry("200x100")

    contrast_entry = Entry(contrast_win, width=3) # Entry input for value of gain
    contrast_entry.place(x=90, y=40, anchor="center")
    contrast_entry.insert(END, 0)

    gain_lbl = Label(contrast_win, text="gain")
    gain_lbl.place(x=110, y=40, anchor="w")

    contrast_btn = Button(contrast_win, text="Apply",
            command=lambda: contrast(contrast_entry))
    contrast_btn.place(x=150, y=70, anchor="center")


# Add and configure buttons
def configure_buttons():

    # Upload Button
    reset_btn = Button(f, text="Reset", command=reset_image)
    reset_btn.place(x=1300, y=150, anchor="center")

    reflect_btn = Button(f, text="Reflect", command=reflect_handler)
    reflect_btn.place(x=100, y=150, anchor="center")

    scale_btn = Button(f, text="Scale", command=scale_handler)
    scale_btn.place(x=100, y=200, anchor="center")

    rotate_btn = Button(f, text="Rotate", command=rotate_handler)
    rotate_btn.place(x=100, y=250, anchor="center")

    crop_btn = Button(f, text="Crop", command=crop_handler)
    crop_btn.place(x=100, y=300, anchor="center")

    brightness_btn = Button(f, text="Brightness", command=bright_handler)
    brightness_btn.place(x=100, y=400, anchor="center")

    contrast_btn = Button(f, text="Contrast", command=contrast_handler)
    contrast_btn.place(x=100, y=450, anchor="center")

    #... all other buttons


# Update the image label
def update_image():
    im_label.configure(image=skIm.tk_img)
    im_label.photo = skIm.tk_img
    im_label.grid(column=2,row=2)
    im_label.pack()
    im_frame.config(width=skIm.np_arr.shape[1], height=skIm.np_arr.shape[0])
    f.update()


# sk Image Class Object
skIm = SkImage()

#Main Window
window = Tk()
window.title("skImage Processor")
window.geometry('1920x1080')

# Main Frame
f = Frame(window, bg="gray", width=1920, height=1080)
f.grid(row=0,column=0,sticky="NW")
# f.grid_propagate(0)
# f.update()


# Title label
l = Label(f, text="Welcome to the skImage Processor", bg="white",  font=("Arial Bold", 50))
l.place(x=960, y=75, anchor="center")


# Upload Button
upload_btn = Button(f, text="Upload Image", command=upload)
upload_btn.place(x=1200, y=150, anchor="center")


# IMAGE FRAME
im_frame = Frame(f, width=600, height=400, bg="white")
im_frame.pack(pady=20,padx=20)
im_frame.place(anchor='center', relx=0.5, rely=0.5)
f.update()

# Create a Label Widget to display the Image
im_label = Label(im_frame, bg="white")
im_label.pack()


window.mainloop()
