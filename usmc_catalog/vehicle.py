try:
    from Tkinter import *
except ImportError:
    from tkinter import *
import ttk
import tkFont
from PIL import ImageTk, Image
from winplace import get_win_place
from collections import OrderedDict


class Vehicle(object):

    filterby_pretty_attr_names = ('endurance', 'payload', 'build time', 'range', 'video')
    filterby_real_attr_names = ('endurance', 'payload', 'build_time', 'max_range', 'video')

    filter_options = {'endurance': (('min','max'), ('min', 'hr')),
                      'payload': (('min', 'max'), ('N', 'lbf', 'kg')),
                      'build time': (('min', 'max'),  ('hr', 'min')),
                      'range': (('min', 'max'), ('km', 'mi', 'm', 'ft')),
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
        max_range = performance['range']
        video = performance['video']

        self.endurance = {'name': 'endurance', 'value': endurance, 'unit': 'min'}
        self.payload = {'name': 'payload', 'value': payload, 'unit': 'N'}
        self.build_time = {'name': 'build time', 'value': build_time, 'unit': 'hr'}
        self.max_range = {'name': 'range', 'value': max_range, 'unit': 'km'}
        self.video = {'name': 'video', 'value': video, 'unit': ''}
        self.performance = (self.endurance, self.payload, self.build_time, self.max_range, self.video)
        self.basic_performance = (self.endurance, self.payload, self.build_time, self.video)

    def display_frame(self, master):

        def display_details():
            ViewQuadDetails(master, self)

        # Create mainframe
        mainframe = ttk.Frame(master, borderwidth=2, relief='raised', cursor='hand1')

        # Create label with vehicle name
        vehicle_name = ttk.Label(mainframe, text=self.name, font='Helvetica 10 bold')
        f = tkFont.Font(vehicle_name, vehicle_name.cget("font"))
        f.configure(underline=False)
        vehicle_name.configure(font=f)

        # Create frame where performance metrics will be displayed
        perf_frame = ttk.Frame(mainframe)
        row = 0
        for attr in self.basic_performance:
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

    def full_details_frame(self, master):
        # Create mainframe
        mainframe = ttk.Frame(master, borderwidth=2, cursor='hand1')

        # Create label with vehicle name
        vehicle_name = ttk.Label(mainframe, text=self.name, font='Helvetica 10 bold')
        f = tkFont.Font(vehicle_name, vehicle_name.cget("font"))
        f.configure(underline=False)
        vehicle_name.configure(font=f)

        # Create frame where performance metrics will be displayed
        perf_frame = ttk.Frame(mainframe)
        column = 0
        for attr in self.performance:
            attr_name_label = ttk.Label(perf_frame, text=attr['name'], font="Helvetica 10")
            f = tkFont.Font(attr_name_label, attr_name_label.cget("font"))
            f.configure(underline=True)
            attr_name_label.configure(font=f)
            attr_val_label = ttk.Label(perf_frame, text=str(attr['value']) + ' ' + str(attr['unit']))
            attr_name_label.grid(column=column, row=0, padx='0 5')
            attr_val_label.grid(column=column, row=1)
            column += 1

        # Create label with vehicle image
        image_label = ttk.Label(mainframe, image=self.image)

        # # Grid stuff
        # vehicle_name.grid(column=0, columnspan=2, row=0, pady=10)
        # image_label.grid(column=0, row=1, padx='5', pady='0 10')
        # perf_frame.grid(column=1, row=1, padx='0 5', pady='0 10')

        vehicle_name.pack()
        image_label.pack()
        perf_frame.pack()

        return mainframe


class ViewQuadDetails(Toplevel):
    """
    This class defines the toplevel window that appears when the user selects the "View Details" button on the main GUI.
    It simply displays all of the information pertaining to the selected feasible alternative.
    """

    def __init__(self, master, vehicle):
        Toplevel.__init__(self, master)
        self.master = master
        self.vehicle = vehicle
        xpos, ypos = get_win_place(self)
        self.geometry('+%d+%d' % (xpos, ypos))
        self.mainframe = ttk.Frame(self)
        self.mainframe.pack(fill=BOTH, expand=YES)
        self.title("Vehicle Details")

        # Create subframes and close button
        self.perf_frame = ttk.Frame(self.mainframe, borderwidth=2, padding='5 15 5 10')
        self.perf_frame.pack(pady='15 8', padx=8)
        self.close_button = ttk.Button(self.mainframe, text='Close', command=self.destroy)
        self.close_button.pack(side=RIGHT, padx='0 5', pady='0 5')

        # Create performance frame
        _perf_frame = self.vehicle.full_details_frame(self.perf_frame)
        _perf_frame.pack(side=LEFT)

        self.mainframe.rowconfigure(2, weight=1)