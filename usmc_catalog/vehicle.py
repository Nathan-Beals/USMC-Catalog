try:
    from Tkinter import *
except ImportError:
    from tkinter import *
import ttk
import tkFont
from PIL import ImageTk, Image


class Vehicle(object):

    filterby_pretty_attr_names = ('endurance', 'payload', 'build time', 'video')
    filterby_real_attr_names = ('endurance', 'payload', 'build_time', 'video')

    filter_options = {'endurance': (('min','max'), ('min', 'hr')),
                      'payload': (('min', 'max'), ('N', 'lbf', 'kg')),
                      'build time': (('min', 'max'),  ('hr', 'min')),
                      'video': (('True', 'False'), ())}

    @classmethod
    def filter_options_frame(cls, master, attr):
        mainframe = ttk.Frame(master)
        if attr == 'video':
            lbl1 = ttk.Label(mainframe, text='is')
        else:
            lbl1 = ttk.Label(mainframe, text='set')
        cb1 = ttk.Combobox(mainframe, state='readonly', values=cls.filter_options[attr][0])
        lbl2 = ttk.Label(mainframe, text='to')
        attr_val = DoubleVar()
        entry = ttk.Entry(mainframe, width=6, textvariable=attr_val)
        cb2 = ttk.Combobox(mainframe, state='readonly', values=cls.filter_options[attr][1])

        lbl1.grid(column=0, row=0, padx='0 5')
        cb1.grid(column=1, row=0, padx='0 5')

        if attr == 'video':
            return mainframe
        else:
            lbl2.grid(column=2, row=0, padx='0 5')
            entry.grid(column=3, row=0, padx='0 2')
            cb2.grid(column=4, row=0, padx='0 10')
        return mainframe, (cb1, attr_val, cb2)

    def __init__(self, name, image, performance):
        self.name = name
        self.image = image

        endurance = performance['endurance']
        payload = performance['payload']
        build_time = performance['build_time']
        video = performance['video']

        self.endurance = {'name': 'endurance', 'value': endurance, 'unit': 'min'}
        self.payload = {'name': 'payload', 'value': payload, 'unit': 'N'}
        self.build_time = {'name': 'build time', 'value': build_time, 'unit': 'hr'}
        self.video = {'name': 'video', 'value': video, 'unit': ''}
        self.performance = (self.endurance, self.payload, self.build_time, self.video)

    def display_frame(self, master):

        def display_details():
            return

        # Create mainframe
        mainframe = ttk.Frame(master, borderwidth=2, relief='raised')

        # Create label with vehicle name
        vehicle_name = ttk.Label(mainframe, text=self.name, font='Helvetica 10 bold')
        f = tkFont.Font(vehicle_name, vehicle_name.cget("font"))
        f.configure(underline=False)
        vehicle_name.configure(font=f)

        # Create frame where performance metrics will be displayed
        perf_frame = ttk.Frame(mainframe)
        row = 0
        for attr in self.performance:
            attr_name_label = ttk.Label(perf_frame, text=attr['name'], font="Helvetica 10")
            f = tkFont.Font(attr_name_label, attr_name_label.cget("font"))
            f.configure(underline=True)
            attr_name_label.configure(font=f)
            attr_val_label = ttk.Label(perf_frame, text=str(attr['value']) + ' ' + str(attr['unit']))
            attr_name_label.grid(column=0, row=row, sticky=W)
            row += 1
            attr_val_label.grid(column=0, row=row, sticky=W)
            row += 1

        # Create label with vehicle image
        image_label = ttk.Label(mainframe, image=self.image)

        # Create vehicle details button
        vehicle_details_button = ttk.Button(mainframe, text='Vehicle Details', command=display_details)

        # Grid stuff
        vehicle_name.grid(column=0, columnspan=2, row=0, pady=10)
        image_label.grid(column=0, row=1, padx='5', pady='0 10')
        perf_frame.grid(column=1, row=1, padx='0 5', pady='0 10')
        vehicle_details_button.grid(column=0, columnspan=2, row=2, pady='0 10')

        return mainframe


