import PIL.Image
import PIL.ImageTk
import numpy as np

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter.messagebox import showinfo
from fractions import Fraction
from decimal import Decimal

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
    if len(skIm.np_arr.shape) == 2: # Convert to RGB (even if grayscale) for simplicity
        skIm.np_arr = np.stack((skIm.np_arr,)*3, axis=-1)
        skIm.img = PIL.Image.fromarray(skIm.np_arr)
    skIm.non_rotated = skIm.np_arr

    update_image()

    configure_buttons()


# Reset image to original state
def reset_image():
    skIm.img = skIm.img_origin
    skIm.np_arr = np.array(skIm.img)
    skIm.tk_img = PIL.ImageTk.PhotoImage(skIm.img)
    if len(skIm.np_arr.shape) == 2: # Convert to RGB (even if grayscale) for simplicity
        skIm.np_arr = np.stack((skIm.np_arr,)*3, axis=-1)
        skIm.img = PIL.Image.fromarray(skIm.np_arr)
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
def scale(width, height, maintain_aspect, default_ar, mode):
    if maintain_aspect.get():
        height = int(width/default_ar) # Keep original aspect ratio, set height accordingly
    skIm.scale(width, height, mode.get())
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

    scale_cb = ttk.Combobox(scale_win, width=8)
    scale_cb.place(x=200, y=150, anchor="center")
    scale_cb['values'] = ('nearest', 'bilinear')
    scale_cb['state'] = 'readonly'
    scale_cb.current(1) # default to bilinear

    scale_btn = Button(scale_win, text="Scale",
            command=lambda: scale(int(scale_width.get()), int(scale_height.get()), maintain_aspect, default_ar, scale_cb))
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

    rotate_cb = ttk.Combobox(rotate_win, width=8)
    rotate_cb.place(x=200, y=150, anchor="center")
    rotate_cb['values'] = ('nearest', 'bilinear', 'shear')
    rotate_cb['state'] = 'readonly'
    rotate_cb.current(1) # default to bilinear

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

    crop_btn = Button(crop_win, text="Crop",
            command=lambda: crop(crop_left, crop_right, crop_top, crop_bottom))
    crop_btn.place(x=350, y=170, anchor="center")


# BRIGHTNESS
def bright(bias):
    skIm.brightness(int(bias.get()))
    update_image()

def bright_handler():
    bright_win = Toplevel(window) # Create new window

    bright_win.title("Brightness")
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
    contrast_win.title("Contrast")
    contrast_win.geometry("200x100")

    contrast_entry = Entry(contrast_win, width=3) # Entry input for value of gain
    contrast_entry.place(x=90, y=40, anchor="center")
    contrast_entry.insert(END, 0)

    gain_lbl = Label(contrast_win, text="gain")
    gain_lbl.place(x=110, y=40, anchor="w")

    contrast_btn = Button(contrast_win, text="Apply",
            command=lambda: contrast(contrast_entry))
    contrast_btn.place(x=150, y=70, anchor="center")


# GAMMA
def gamma(level):
    skIm.gamma(float(level.get()))
    update_image()

def gamma_handler():
    gamma_win = Toplevel(window)
    gamma_win.title("Gamma")
    gamma_win.geometry("200x100")

    gamma_entry = Entry(gamma_win, width=3) # Entry input for value of gain
    gamma_entry.place(x=90, y=40, anchor="center")
    gamma_entry.insert(END, 0)

    level_lbl = Label(gamma_win, text="level")
    level_lbl.place(x=110, y=40, anchor="w")

    gamma_btn = Button(gamma_win, text="Apply",
            command=lambda: gamma(gamma_entry))
    gamma_btn.place(x=150, y=70, anchor="center")


# HISTOGRAM
def histogram(rgb_img, normalized, culmulative):
    skIm.histogram(rgb_img.get(), normalized.get(), culmulative.get())

def histogram_equ(rgb_img, normalized, culmulative):
    skIm.histogram_equ()
    update_image()
    rgb_img.set(1)
    normalized.set(1)
    culmulative.set(1)
    skIm.histogram(rgb_img.get(), normalized.get(), culmulative.get()) # Update / Add histogram

def histogram_handler():
    histo_win = Toplevel(window)
    histo_win.title("Histogram")
    histo_win.geometry("400x200")

    rgb_img = IntVar(histo_win, 0, "rgb_img")
    normalized = IntVar(histo_win, 0, "normalized")
    culmulative = IntVar(histo_win, 0, "culmulative")

    c1 = Checkbutton(histo_win, text='Colour Image', variable=rgb_img)
    c1.place(x=200, y=50, anchor="center")

    c2 = Checkbutton(histo_win, text='Normalized', variable=normalized)
    c2.place(x=200, y=70, anchor="center")

    c3 = Checkbutton(histo_win, text='Culmulative', variable=culmulative)
    c3.place(x=200, y=90, anchor="center")

    histo_btn = Button(histo_win, text="Show Histogram",
            command=lambda: histogram(rgb_img, normalized, culmulative))
    histo_btn.place(x=200, y=130, anchor="center")

    histo_equ_btn = Button(histo_win, text="Histogram Equalization", 
            command=lambda: histogram_equ(rgb_img, normalized, culmulative))
    histo_equ_btn.place(x=200, y=170, anchor="center")


# CONVOLUTION
def convolution(values, mode):

    kernel = np.zeros([len(values), len(values[0])])
    for i in range(len(values)): # Num Rows
        for j in range(len(values[i])):
            kernel[i][j] = float(Fraction(values[i][j].get()))

    skIm.convolution(kernel, mode.get())
    update_image()

def convolve_handler(kernel, mode, preset, m, n):

    convolve_win = Toplevel(window)
    convolve_win.title("Convolution")
    # Dynamicaly set size of window according to size of kernel
    convolve_win.geometry(str((m*30)+100)+"x"+str((n*30)+100))

    values = []
    entries = []
    
    # Building Kernel
    x_pad = 0
    y_pad = 0

    for i in range(n): # mxn kernel, n is height
        values.append([])
        entries.append([])
        for j in range(m):
            values[i].append(StringVar())
            entries[i].append(Entry(convolve_win, textvariable=values[i][j], width=3))
            entries[i][j].place(x=50 + x_pad, y=50 + y_pad, anchor="center")
            if preset: entries[i][j].insert(END, kernel[i][j])
            x_pad += 30
        y_pad += 30
        x_pad = 0
    
    convolve_btn = Button(convolve_win, text="Apply", 
            command=lambda: convolution(values, mode))
    convolve_btn.place(x=(m*30), y=(n*30)+65, anchor="w")


def convolve_preset(preset, mode):

    kernel = np.empty(0) # kernel starts at nothing

    # PRESETS
    if preset == "mean":
        kernel = np.array([["1/9", "1/9", "1/9"], ["1/9", "1/9", "1/9"], ["1/9", "1/9", "1/9"]])
    elif preset == "sharpen":
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    elif preset == "laplacian":
        kernel = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
    elif preset == "gaussian":
        kernel = np.array([["1/16", "1/8", "1/16"], ["1/8", "1/4", "1/8"], ["1/16", "1/8", "1/16"]])
    elif preset == "gaussian5":
        kernel = np.array([["1/256", "4/256", "6/256", "4/256", "1/256"], 
                           ["4/256", "16/256", "24/256", "16/256", "4/256"], 
                           ["6/256", "24/256", "36/256", "24/256", "6/256"],
                           ["4/256", "16/256", "24/256", "16/256", "4/256"], 
                           ["1/256", "4/256", "6/256", "4/256", "1/256"]])
    else:
        kernel = np.zeros((3, 3)) # failsafe, zeros

    # Call convolve function to create kernel visible for user with preset filled in  
    convolve_handler(kernel, mode, True, kernel.shape[0], kernel.shape[1])
    
def convolution_handler():
    convolution_win = Toplevel(window)
    convolution_win.title("Configure Convolution")
    convolution_win.geometry("400x200")

    # Custom Convolution Kernel Size
    width_entry = Entry(convolution_win, width=2) # Entry input for the width of the kernel
    width_entry.place(x=40, y=40, anchor="center")
    width_entry.insert(END, 3) # Default of 3

    x_lbl = Label(convolution_win, text="x")
    x_lbl.place(x=60, y=40, anchor="center")

    height_entry = Entry(convolution_win, width=2) # Entry input for the height of the kernel
    height_entry.place(x=80, y=40, anchor="center")
    height_entry.insert(END, 3) # Default of 3

    border_cb = ttk.Combobox(convolution_win, width=8)
    border_cb.place(x=200, y=150, anchor="center")
    border_cb['values'] = ('truncate', 'zero')
    border_cb['state'] = 'readonly'
    border_cb.current(1) # default to zero

    kernel = np.empty((int(height_entry.get()), int(width_entry.get()))) # Empty kernel for custom convolutions
    custom_btn = Button(convolution_win, text="Custom", 
            command=lambda: convolve_handler(kernel, border_cb, preset=False, m=int(height_entry.get()), n=int(width_entry.get())))
    custom_btn.place(x=25, y=70, anchor="w")

    # Presets
    presets_lbl = Label(convolution_win, text="Presets", underline="7")
    presets_lbl.place(x=320, y=10, anchor="center")

    mean = Button(convolution_win, text="Mean", 
            command=lambda: convolve_preset("mean", border_cb))
    mean.place(x=320, y=30, anchor="center")

    sharpen = Button(convolution_win, text="Sharpen", 
            command=lambda: convolve_preset("sharpen", border_cb))
    sharpen.place(x=320, y=60, anchor="center")

    laplacian = Button(convolution_win, text="Laplacian", 
            command=lambda: convolve_preset("laplacian", border_cb))
    laplacian.place(x=320, y=90, anchor="center")

    gaussian = Button(convolution_win, text="Gaussian", 
            command=lambda: convolve_preset("gaussian", border_cb))
    gaussian.place(x=320, y=120, anchor="center")

    gaussian5 = Button(convolution_win, text="Gaussian5x5", 
            command=lambda: convolve_preset("gaussian5", border_cb))
    gaussian5.place(x=320, y=150, anchor="center")


# ORDER STATISTIC FILTERING
def order_stat(mode):
    skIm.order_filter(mode)
    update_image()

def order_stat_handler():
    order_stat_win = Toplevel(window)
    order_stat_win.title("Order Statistic Filtering")
    order_stat_win.geometry("400x200")

    minimum = Button(order_stat_win, text="Minimum", 
            command=lambda: order_stat("min"))
    minimum.place(x=100, y=100, anchor="center")

    maximum = Button(order_stat_win, text="Maximum", 
            command=lambda: order_stat("max"))
    maximum.place(x=200, y=100, anchor="center")

    median = Button(order_stat_win, text="Median", 
            command=lambda: order_stat("med"))
    median.place(x=300, y=100, anchor="center")

# Add and configure buttons
def configure_buttons():

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

    gamma_btn = Button(f, text="Gamma", command=gamma_handler)
    gamma_btn.place(x=100, y=500, anchor="center")

    histogram_btn = Button(f, text="Histogram", command=histogram_handler)
    histogram_btn.place(x=100, y=600, anchor="center")

    convolution_btn = Button(f, text="Convolution", command=convolution_handler)
    convolution_btn.place(x=100, y=700, anchor="center")

    order_stat_btn = Button(f, text="Order Statistic", command=order_stat_handler)
    order_stat_btn.place(x=100, y=800, anchor="center")

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

# Mainloop for window/program
window.mainloop()
