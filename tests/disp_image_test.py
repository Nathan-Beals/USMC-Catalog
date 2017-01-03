try:
    from Tkinter import *
except ImportError:
    from tkinter import *
from PIL import ImageTk, Image
import os

root = Tk()
dir = os.path.dirname(os.path.abspath(__file__))
photos_dir = dir + '/photos/'
photo_loc = photos_dir + 'tiger.jpg'
print photo_loc
size = (150, 128)
img = ImageTk.PhotoImage(Image.open(photo_loc).resize(size, Image.ANTIALIAS))
panel = Label(root, image=img)
panel.pack(side="bottom", fill="both", expand="yes")
root.mainloop()