# import the necessary packages
from tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2

def select_image():
    global panelA, panelB
    image = cv2.imread("star.png",-1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 50, 100)
    # OpenCV represents images in BGR order; however PIL represents
    # # images in RGB order, so we need to swap the channel
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # convert the images to PIL format...
    image = Image.fromarray(image)
    edged = Image.fromarray(edged)
    # ...and then to ImageTk format
    image = ImageTk.PhotoImage(image)
    edged = ImageTk.PhotoImage(edged)
        # if the panels are None, initialize them
    if panelA is None or panelB is None:
        # the first panel will store our original image
        panelA = Label(image=image)
        panelA.image = image
        panelA.pack(side="left", padx=10, pady=10)
        # while the second panel will store the edge map
        panelB = Label(image=edged)
        panelB.image = edged
        panelB.pack(side="right", padx=10, pady=10)
    # otherwise, update the image panels
    else:
        # update the pannels
        panelA.configure(image=image)
        panelB.configure(image=edged)
        panelA.image = image
        panelB.image = edged
root = Tk()
panelA = None
panelB = None
# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
# kick off the GUI
root.mainloop()