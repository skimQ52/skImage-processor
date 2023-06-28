
# The skImage Processor


1.1 - An Introduction to the ‘skImage’ Processor
---
This is a program to be used for digitally processing existing images through an array of different possible operations. Such operations include:
* Geometric Spatial Transformations using various interpolations
* Linear and Power Law mappings
* Generation of Histograms and Histogram Equalization
* Convolutions using preset or custom kernels of any size
* Non-Linear, Order-Statistic Filtering such as minimum, maximum and median filtering


All operations can be performed on both grayscale and colour images, for either PNG or JPEG.


This program operates fully in raster (bitmap), no vector operations are done. Additionally, this program is not designed to create new images, make traditional artwork (though art can be made), or allow users to explicitly draw/create shapes on an existing image.

1.2 - Getting Started
---

Upon starting the program, users are met with a landing page as seen below.
  

To proceed, users must click the Upload Image button in the top right of the application.   


Using the file selection pop up window, users can select a type of image (file extension), and then the image they would like to digitally process. Users can finally select the Open button to load their chosen image into the program. 


After the selected image has been loaded in, users are met with the program's main menu of operations.
  
The button-bar on the left side of the program houses all of the program's main tools.
The button-bar on the right side of the program houses all of the general tools, like saving and resetting.


At any point in operation, users may save (or save as) the image, reset the image to its most recent save state, or upload a new image to operate on (Warning: Unsaved changes will be lost when uploading a new image, or closing the application).


1.3 - Geometric Spatial Transformations  
---

**Reflecting:**
Clicking the Reflect button of the left button-bar will open the Reflecting window. Then, users can choose either to reflect Horizontally or Vertically.  
For example, if the Vertical operation was selected, our cat.jpg flips upside down!


**Scaling:**
Clicking the Scale button will open the Scaling window. Then, users can input the new dimensions they wish to scale the image to. To perfectly maintain the aspect ratio, users can check the Maintain Aspect Ratio checkbox and only the width will need to be inputted. Additionally, users can choose between nearest-neighbour or bilinear interpolation with the flyout menu on the bottom.  


**Rotating:**
Clicking the Rotate button will open the Rotate window. Then, users can choose the direction they wish to rotate the image, the number of degrees they wish to rotate, and finally, the interpolation method. There exists three interpolations for rotation, nearest-neighbour, bilinear, and shear.    


*An image that has been rotated 65 degrees Clockwise with bilinear interpolation.*




**Cropping:**
Clicking the Crop button will open the Crop window. Then, users can input the number of pixels to crop from each side of the image (Left, Right, Top, Bottom).

1.4 - Linear and Power Law Mappings
---

Brightness, Contrast and Gamma of the image are all manipulatable using their designated buttons and windows. In the Brightness window, users can enter a bias level to raise the brightness (positive bias) or lower the brightness (negative bias) by. In the Contrast window, users can enter a gain level to increase the contrast (gain > 1) or decrease the contrast (gain between 0 and 1). Finally in the Gamma window, users can enter a gamma level to adjust the gamma.


1.5 - Histograms and Histogram Equalization
---

Clicking the Histogram button will open the histogram menu, as seen below.  


Here, users can select between the three toggleable options of histograms: Color Image, Normalized, and Cumulative. Then, clicking Show Histogram will display the according histogram for the current image being processed.
  

To illustrate, here is the Normalized, Cumulative histogram generated for the colour image ‘cat.jpg’. 


Additionally, users can perform Histogram Equalization by clicking on its button in the histogram menu, which equalizes this generated histogram and consequently alters the contrast to be ‘statistically better’.  
  

Here we have the same histogram as above as well as the output image after Histogram Equalization has been performed.

1.6 - Convolution
---

Clicking on the Convolution button will open the Convolution menu as seen below.
   
Users can either: enter the values for the size of a custom kernel and click the Custom button, or select one of the preset kernels given on the right. Additionally, users can choose between different border handling behaviour from the bottom dropdown menu: zero padding or truncation.  


If a user were to click the Custom button with 3 x 3 entered into the size entry boxes, an empty kernel like this would appear ready to be filled in.   


Otherwise, if the user selected one of the preset kernels on the right, Gaussian5x5 for example, they would be met with a similar pop-up with predefined values filled into the kernel. Of course, users can alter the presets’ values as they desire.


Once the kernel is completed, and all its values are filled in, the user can click the Apply button to apply the convolution.


1.7 - Order-Statistic Filtering and Adding Noise
---

Users can add noise by clicking the Add Noise button on the left button-bar, which is handy for testing out the different order-statistic filters. Users can add Salt (white), Pepper (Black), Red, Green and Blue noise by clicking on their respective buttons.


Users can click the Order-Statistic button in order to remove any noise in the image. The Minimum filter is great for eliminating salt noise, the Maximum filter is great for eliminating pepper noise, and the Median filter is competent to remove both, as well as some RGB noise.
Section 2 - Technical Discussion


2.1 - How the program is set up
---

This Digital Image Processing program relies on the original class of ‘SkImage’ which holds and manipulates images. Each operation has its own respective method definitions to pursue the operations. A main driver file creates an object of this defined class, and creates GUIs for each operation to possess the ability to call the class methods and manipulate the image. A grayscale image can be defined using a 2-Dimensional Array, or a matrix, where each dimension is defined by the size (or resolution) of the image. Additionally, each value at some (x, y) coordinate within the image has some ‘l’ value which denotes the intensity at that pixel (a value from 0 to 255, where 0 is black and 255 is white). Meanwhile, for RGB colour images, there are 3 channels of intensity instead, one for each Red, Green and Blue. To keep things simple, this program treats grayscale images as RGB colour images, where all RGB values remain equal.


2.2 - Bilinear Interpolation
---

Bilinear Interpolation is used in both rotation and scaling of an image within this program. In both operations, it is the ‘best’ interpolation method (shear and bilinear are comparable for rotation). It needs to be done when a pixel ‘ends up’ in a value ‘between’ 4 possible, integer pixel locations (see the figure). Using these 4 corners around the pixel, we can calculate its proper intensity. There are three main equations performed in bilinear interpolation, and each equation is performed individually on each RGB channel:
* Equation 1: ft = (1 - s) * top_left + (s * top_right)
* Equation 2: fb = (1 - s) * bottom_left + (s * bottom_right)
* Equation 3: value = nint(((1 - t) * ft) + (t * fb))
* Where s = x - x1, t = y - y1, top_left (top_right etc..) are the intensity values of the corresponding RGB channel of the corner pixel, and value is the corresponding final RGB intensity after interpolation.






2.3 - Geometric Spatial Transformations
---

**Rotation:**
This program applies rotations from a maintained non-rotated version of the image, so that the mandatory (zero) padding around the image remains minimal. The program first checks the direction on the rotation. If the user rotated the image counter clockwisely, then, the degrees must be negated (multiplied by -1) in order to rotate the other way. Afterwards, the degrees to be rotated are added to the total degrees rotated of the SkImage object (which starts at 0 if no rotations have been made). To maintain efficiency, if the total degrees has surpassed 360, the program sets the total degrees to its value modulo 360, since it is equivalent. Then, the rotation is applied to the maximum values of the height and width (the sizes of the image array) in order to get the maximum values of the new image array after rotation (the size of the new image). With that, the program iterates through each pixel of the non-rotated version of the image, and performs the rotation in building the new image array using any of the three interpolation types:
* Nearest-neighbour: Calculates the new x and y values of the current pixel using rounded output of the formula:
y’ = -x * sin(θ) + y * cos(θ)
x’ = x * cos(θ) + y * sin(θ)
        (Where θ is the degree of rotation, and x’ and y’ are the final x and y values)
* Bilinear interpolation: Calculates the new x and y values of the pixel using the same formula as above, then applies Bilinear Interpolation (See section 2.2 - Bilinear Interpolation).
* Shearing: runs the specific x and y coordinates through three rounds of shearing in order to perform the rotation and have a more aesthetically pleasing appearance.
   * Shear 1: x’ = x - y * tan(θ/2)
   * Shear 2: y’ = x’ * sin(θ) + y
   * Shear 3: x’’ = x’ - y’ * tan(θ/2)
        (Where θ is the degree of rotation, x’’ and y’ are the final x and y values)
The program sets the new image array’s pixel at the new x and y values to the current, non-rotated pixel.


**Scaling:**
To scale an image, the program first creates a new image array that is the size of the desired scaling, whether it be smaller or larger. Then, the difference in height and difference in width is calculated, by dividing the new values by the old values. With these differences, the program iterates through all of the new image array’s coordinates/pixels, and can either set the according r, g, b intensities to what their proper values were closest to from the original image with nearest-neighbour interpolation, or use bilinear interpolation (See section 2.2 - Bilinear Interpolation).


**Reflecting:**
To reflect an image, the program iterates through each and every value (pixel) within the 2D image array and builds a new image array where the pixels are reflected accordingly. If the image is to be reflected vertically, the current pixel would be set at the vertically opposite side of the new image array being built. That is, the height of the image subtracted by the current height. The same applies if the image was to be reflected horizontally, using width parameters instead.


**Cropping:**
To crop an image, the program creates a new image array that is the size of the old one, with the height subtracted by the amount of pixels to be cropped vertically, and the width subtracted by the amount of pixels to be cropped horizontally. Then, it simply iterates through the range of pixels that are not being cropped and builds the new image array.


2.4 - Linear and Power Law Mappings
---
Linear mappings are a fairly simple concept and this program's implementation is no different. For both brightness, contrast, and gamma the program iterates through all pixels of the image array, and either:
* Adds the bias value to each RGB channel for adjusting the brightness
* Multiplies the gain value to each RGB channel for adjusting the contrast.
* Applies the power law function using the given gamma level, defined as:
          , where L-1 is 255, and u is R, G and/or B.
(Note that the max value is 255, and the minimum value is 0, for any RGB.)


2.5 - Histograms and Histogram Equalization
---
**Histogram Generation:**
This program provides three main toggleable options in generating histograms. Firstly, users can decide to treat their operating image as a grayscale or as a colour image. If grayscale is chosen, the average of the 3 RGB channels are taken, (which does nothing for an actual grayscale image). If a colour image is chosen, 3 different histograms are generated (on the same graph) for each RGB channel (grayscale images will have their 3 channels all identical). Secondly, users can generate normalized histograms, such that the counts/values of the histogram are divided by the resolution of the image (M * N) in order to represent the probabilities of the pixels. Finally, users can generate cumulative histograms, such that the counts/values of the histogram have all of the preceding counts added to it.

**Histogram Equalization:**
This program performs histogram equalization by first calculating the cumulative normalized histogram of each RGB channel. Then, with these, to perform histogram equalization, a new image array is built where the values of pixels are set to their according values of RGB in the cumulative normalized histogram, each multiplied by 255.


2.6 - Convolution and Order-Statistic Filtering
---
Convolution is performed in this program by accepting some defined kernel from user input. The program verifies if the inputted kernel is separable (there exists an h1 and an h2 such that h1h2 = the kernel) by verifying if it is a square matrix and if the matrix rank is equal to 1. If the kernel is separable, the program splits the kernel into the two h1 and h2, and convolves each onto the image. Otherwise, in the case the kernel is not separable, the program convolves with the original kernel. In performing convolution, for each pixel of the image array, a window of its respective 8-neighbours (all of the pixels that can be reached by 1 unit of chessboard distance), as well as the pixel itself is defined. With this window, each RGB channel of all pixels in the window are multiplied with each correlating value in the kernel (top left of kernel * top left of window etc..), and then added to a total sum for each RGB which become the new values of the current pixel. The handling of the border is contingent on the user's selection between truncation: convolution ‘ignores’ the borders, where a full window can’t be created, or zero padding: convolution assumes edges are padded with 0’s in creating windows. After each pixel has been processed, they must be normalized to visible output (values between 0 and 255). This is done by acquiring the max and min values of RGB of the entire image array, then for each RGB channel, set the values as:
        New = (value - min) * 255 / (max - min)
Where value is the current intensity of the channel, min is the minimum value of the channel and max is the maximum value of the channel.
Order-Statistic Filtering is performed in a similar manner to convolution, yet the process is simpler. For each pixel of the image array, a window of its respective 8-neighbours (all of the pixels that can be reached by 1 unit of chessboard distance), as well as the pixel itself is defined. With this window, each RGB channel of all pixels in the window are added together and divided by 3 in order to get the average intensity. For min and max filtering, the min and max values respectively are found from within the window, and the current pixel is set to whichever is appropriate. For median filtering, the average intensities are sorted, and the current pixel is set to the intensity of the middle/median value of this sorted list.


Discussion of Results and Future Work
---

While I had a lot of fun developing and creating this project, there were some unsatisfactory shortcomings. To start, the biggest thing that I believe this program is missing is alternatives to zero padding in geometric spatial transformations. In rotation, there is bound to be zero padding left over in the output image, and so implementing circular and reflected indexing for rotation in particular would make this project feel much more whole. Another significant thing that I would like to add is more border handling options for convolution. As of now, there are only 2 possible options in either truncation or assuming zero padding. While these are functional, they are not optimal and having alternatives such as reflected indexing would be a great addition. Lastly, with respect to additions to existing functionalities, implementing a better solution for removing RGB noise from an image would be great to add. With the current implementation, median filtering removes most, if not all of the RGB noise in a given image, but often there is some left over within the edges in the image. Another thing that I had interest in implementing into this image processing program was performing object detection using a neural network model. I dabbled with implementing modern machine learning models like YOLACT and Detectron2, however setting them up removed the simplicity of running this program, and it also tarnished its simple identity. Finally, there exists some inconsistencies and small hurdles users of this program may face. Many of which are caused by GUI bugs and mishaps. For example, with the several ‘dropdown’ menus that exist throughout the program. For an unknown reason, users may experience lackluster dropdown options placed around their screen. Smoothing out these edges would go a long way and would be an important thing to focus on in improving this program.
