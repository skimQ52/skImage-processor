import PIL.Image
import PIL.ImageTk
import numpy as np
import math

SIN=lambda x: int(math.sin(x * 3.141592653589 / 180))
COS=lambda x: int(math.cos(x * 3.141592653589 / 180))

class SkImage:

    def __init__(self):
        self.path = ""
        self.img = None
        self.np_arr = None
        self.tk_img = None
        self.img_origin = None
        self.non_rotated = None
        self.degrees = 0

    def reflect(self, direction):

        new_arr = np.copy(self.np_arr)
        if (direction == "hor"): # horizontal reflection
            for i in range(self.np_arr.shape[0]): # height
                for j in range(self.np_arr.shape[1]): # width
                    new_arr[i][(new_arr.shape[1] - 1) - j] = self.np_arr[i][j]

        elif (direction == "ver"): # vertical reflection
            for i in range(self.np_arr.shape[0]): # height
                for j in range(self.np_arr.shape[1]): # width
                    new_arr[(new_arr.shape[0] - 1) - i][j] = self.np_arr[i][j]

        # Update skImage object
        self.np_arr = new_arr
        self.img = PIL.Image.fromarray(new_arr)
        self.tk_img = PIL.ImageTk.PhotoImage(self.img)
        self.non_rotated = self.np_arr


    def scale(self, width, height):

        width_diff = width/self.np_arr.shape[1]
        height_diff = height/self.np_arr.shape[0]
        new_arr = np.empty([height, width, 3], dtype=np.uint8)

        for i in range(height-1):
            for j in range(width-1):
                
                r, g, b = self.img.getpixel((int(j/width_diff), int(i/height_diff)))

                # r = r * (height-1)/(width-1)
                # g = g * (height-1)/(width-1)
                # b = b * (height-1)/(width-1)
                new_arr[i][j] = r, g, b

                # continue

        # Update skImage object
        self.np_arr = new_arr
        self.img = PIL.Image.fromarray(new_arr)
        self.tk_img = PIL.ImageTk.PhotoImage(self.img)
        self.non_rotated = self.np_arr


    def shear_at_point(self, angle, x, y):
        # |1  -tan(𝜃/2) |  |1        0|  |1  -tan(𝜃/2) | 
        # |0      1     |  |sin(𝜃)   1|  |0      1     |

        # shear 1
        tangent=math.tan(angle/2)
        new_x=round(x-y*tangent)
        new_y=y
        
        # shear 2
        new_y=round(new_x*math.sin(angle)+new_y)

        # shear 3
        new_x=round(new_x-new_y*tangent)
        
        return new_y, new_x


    def rotate(self, wise, degrees, mode):

        # In the case counter clockwise was selected, negate the degrees
        if wise == 0:
            degrees = -1 * degrees

        # Add to total degrees to take into account previous rotations
        self.degrees += degrees

        # Keep the total degrees low, anything higher than 359 has an equivalent
        if self.degrees > 360:
            self.degrees = self.degrees % 360
        
        # Convert to radians for math functions sin and cos
        angle = math.radians(self.degrees)

        # Convinient definitions so code isn't too messy
        cosine = math.cos(angle)
        sine = math.sin(angle)

        # Calculate the height and the width of the image (after rotation)
        new_h = round(abs(self.non_rotated.shape[0] * cosine)+abs(self.non_rotated.shape[1] * sine)) + 1 # add 1 so new height/width always > 0
        new_w = round(abs(self.non_rotated.shape[1] * cosine)+abs(self.non_rotated.shape[0] * sine)) + 1

        # Get centre of old image and new image        
        centre_h = round(((self.non_rotated.shape[0] + 1)/2) - 1)
        centre_w = round(((self.non_rotated.shape[1] + 1)/2) - 1)
        new_centre_h = round(((new_h + 1)/2) - 1)
        new_centre_w = round(((new_w + 1)/2) - 1)
            
        # New image np array with exactly the correct width and height after rotation
        if mode != "bilinear":
            new_arr = np.zeros([new_h, new_w, self.non_rotated.shape[2]], dtype=np.uint8)
        else: # Bilinear uses same size
            new_arr = np.zeros([self.non_rotated.shape[0], self.non_rotated.shape[1], self.non_rotated.shape[2]], dtype=np.uint8)


        # Nearest neighbour or Shear
        if mode != "bilinear":
            for i in range(self.non_rotated.shape[0]):
                for j in range(self.non_rotated.shape[1]):
                    # Get pixel with respect to centre of image
                    y = self.non_rotated.shape[0] - i - centre_h - 1
                    x = self.non_rotated.shape[1] - j - centre_w - 1

                    if mode == "shear":
                        # Applying shear Transformation                     
                        new_y, new_x = self.shear_at_point(angle,x,y)

                    else:
                        # co-ordinate of pixel with respect to the rotated image, Nearest Neighbour? moght be needed for both
                        new_y = round(-x * sine + y * cosine)
                        new_x = round(x * cosine + y * sine)

                    # Centre also changes, need to change new x and y according to the new centre
                    new_y = new_centre_h - new_y
                    new_x = new_centre_w - new_x

                    # error prevention before updating new np array
                    if 0 <= new_x < new_w and 0 <= new_y < new_h and new_x >= 0 and new_y >=0:
                        new_arr[new_y, new_x, :] = self.non_rotated[i, j, :]

        # Bilinear Interpolation
        else:
            img = PIL.Image.fromarray(self.non_rotated)
            for i in range(self.non_rotated.shape[0]):
                for j in range(self.non_rotated.shape[1]):
                    # Get pixel with respect to centre of image
                    y = self.non_rotated.shape[0] - i - centre_h - 1
                    x = self.non_rotated.shape[1] - j - centre_w - 1

                    new_y = (-x * sine) + (y * cosine) # true values floating point (not rounded)
                    new_x = (x * cosine) + (y * sine)

                    new_y = centre_h - new_y
                    new_x = centre_w - new_x

                    # get 4 points values
                    x0 = math.floor(new_x)
                    y0 = math.floor(new_y)
                    x1 = math.ceil(new_x)
                    y1 = math.ceil(new_y)

                    #
                    if x0 < 0 or x1 < 0 or x0 >= self.non_rotated.shape[1] or x1 >= self.non_rotated.shape[1] or y0 < 0 or y1 < 0 or y0 >= self.non_rotated.shape[0] or y1 >= self.non_rotated.shape[0]:
                        continue

                    # Get 4 corners
                    tl_r, tl_g, tl_b = img.getpixel((x0, y0))
                    tr_r, tr_g, tr_b = img.getpixel((x1, y0))
                    bl_r, bl_g, bl_b = img.getpixel((x0, y1))
                    br_r, br_g, br_b = img.getpixel((x1, y1))


                    # Performing bilinear interpolation for each rgb
                    s = new_x - x0
                    t = new_y - y0

                    # Equation 1
                    ft_r = (1 - s) * tl_r + (s * tr_r)
                    ft_g = (1 - s) * tl_g + (s * tr_g)
                    ft_b = (1 - s) * tl_b + (s * tr_b)

                    # Equation 2
                    fb_r = (1 - s) * bl_r + (s * br_r)
                    fb_g = (1 - s) * bl_g + (s * br_g)
                    fb_b = (1 - s) * bl_b + (s * br_b)

                    # Equation 3
                    red = round(((1 - t) * ft_r) + (t * fb_r))
                    green = round(((1 - t) * ft_g) + (t * fb_g))
                    blue = round(((1 - t) * ft_b) + (t * fb_b))

                    # caps on rgb
                    if red < 0: red = 0
                    if red > 255: red = 255
                    if green < 0: green = 0
                    if green > 255: green = 255
                    if blue < 0: blue = 0
                    if blue > 255: blue = 255

                    new_arr[i, j] = red, green, blue


        # Update skImage object (dont update non_rotated image)
        self.np_arr = new_arr
        self.img = PIL.Image.fromarray(new_arr)
        self.tk_img = PIL.ImageTk.PhotoImage(self.img)



    def crop(self, left, right, top, bottom):
        # Create new image with proper (reduced) size
        new_arr = np.empty([self.np_arr.shape[0] - (top+bottom), self.np_arr.shape[1] - (left+right), 3], dtype=np.uint8)

        for i in range(top, (self.np_arr.shape[0] - bottom)): # Shift starting index according to amount of pixels to remove from top, until amount to remove from bot
            for j in range(left, (self.np_arr.shape[1] - right)): # Shift starting index according to amount of pixels to remove from left, until amount to remove from right
                new_arr[i-top][j-left] = self.np_arr[i][j]

        # Update skImage object
        self.np_arr = new_arr
        self.img = PIL.Image.fromarray(new_arr)
        self.tk_img = PIL.ImageTk.PhotoImage(self.img)
        self.non_rotated = self.np_arr
                

    # ------------------------- Linear Mappings -----------------------------
    
    def brightness(self, bias):

        for i in range(self.np_arr.shape[0]):
            for j in range(self.np_arr.shape[1]):

                r, g, b = self.img.getpixel((j, i))

                # Add bias to each rgb
                r += bias
                g += bias
                b += bias

                # Checks to see if in valid range
                if r > 255:
                    r = 255
                elif r < 0:
                    r = 0
                if g > 255:
                    g = 255
                elif g < 0:
                    g = 0
                if b > 255:
                    b = 255
                elif b < 0:
                    b = 0

                self.np_arr[i][j] = r, g, b

        # Update skImage object
        self.img = PIL.Image.fromarray(self.np_arr)
        self.tk_img = PIL.ImageTk.PhotoImage(self.img)
        self.non_rotated = self.np_arr


    def contrast(self, gain):

        # invalid value
        if gain == 0:
            return

        for i in range(self.np_arr.shape[0]):
            for j in range(self.np_arr.shape[1]):

                r, g, b = self.img.getpixel((j, i))

                # Add bias to each rgb
                r *= gain
                g *= gain
                b *= gain

                # Checks to see if in valid range
                if r > 255:
                    r = 255
                elif r < 0:
                    r = 0
                if g > 255:
                    g = 255
                elif g < 0:
                    g = 0
                if b > 255:
                    b = 255
                elif b < 0:
                    b = 0

                self.np_arr[i][j] = r, g, b
        
        # Update skImage object
        self.img = PIL.Image.fromarray(self.np_arr)
        self.tk_img = PIL.ImageTk.PhotoImage(self.img)
        self.non_rotated = self.np_arr
                    