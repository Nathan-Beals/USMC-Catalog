import os
try:
    from Tkinter import *
except ImportError:
    from tkinter import *
import ttk
from PIL import ImageTk, Image
import re

execute_dir = os.path.dirname(os.path.abspath(__file__))
for vehicle_file in os.listdir('../vehicles'):
    vehicle_path = os.path.dirname(execute_dir) + '/vehicles/' + vehicle_file + '/'
    vehicle_name = str(vehicle_file)
    img = None
    attr_names = []
    attr_vals = []
    for filename in os.listdir('../vehicles/' + vehicle_file):
        print filename
        # Get vehicle image and save as ImageTk object
        if filename.endswith(".jpg") or filename.endswith(".png"):
            root = Tk()
            image_path = vehicle_path + filename
            size = (150, 128)
            original = Image.open(image_path)
            resized = original.resize(size, Image.ANTIALIAS)
            image = ImageTk.PhotoImage(resized)
        # Parse vehicle attribute text file and extract vehicle attribute values
        elif filename.endswith(".txt"):
            with open(vehicle_path + filename) as f:
                vehicle_attrs = [x.strip('/n').replace(' ', '') for x in f.readlines()]
                attr_names = [attr_line[:attr_line.find("=")] for attr_line in vehicle_attrs]
                attr_vals = [re.findall(r"[-+]?\d*\.\d+|\d+", attr_line) for attr_line in vehicle_attrs]
                for indx, name in enumerate(attr_names):
                    if name == 'video':
                        has_video = vehicle_attrs[indx][vehicle_attrs[indx].find("=")+1:]
                        print has_video
                        attr_vals[indx] = [has_video]
                attr_vals = [val for sublist in attr_vals for val in sublist]
    vehicle = dict(zip(attr_names, attr_vals))
    print vehicle