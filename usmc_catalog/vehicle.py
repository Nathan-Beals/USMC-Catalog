try:
    from Tkinter import *
except ImportError:
    from tkinter import *
import ttk
import tkFont
from PIL import ImageTk, Image
from winplace import get_win_place
from collections import OrderedDict
from tools import convert_unit
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter


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
        endurance_std_val = convert_unit(endurance[0], endurance[1], 'min')
        payload = performance['payload']
        payload_std_val = convert_unit(payload[0], payload[1], 'lbf')
        build_time = performance['build_time']
        build_time_std_val = convert_unit(build_time[0], build_time[1], 'hr')
        max_range = performance['range']
        max_range_std_val = convert_unit(max_range[0], max_range[1], 'mi')
        video = performance['video']

        self.endurance = {'name': 'endurance', 'value': endurance_std_val, 'unit': 'min'}
        self.payload = {'name': 'payload', 'value': payload_std_val, 'unit': 'lbf'}
        self.build_time = {'name': 'build time', 'value': build_time_std_val, 'unit': 'hr'}
        self.max_range = {'name': 'range', 'value': max_range_std_val, 'unit': 'mi'}
        self.video = {'name': 'video', 'value': video[0], 'unit': video[1]}
        self.performance = (self.endurance, self.payload, self.build_time, self.max_range, self.video)
        self.basic_performance = (self.endurance, self.payload, self.build_time, self.video)

    def display_frame(self, master):

        def display_details():
            ViewVehicleDetails(master, self)

        def display_performance():
            ViewVehiclePerformance(master, self)

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
            try:
                attr_val_label = ttk.Label(perf_frame, text="%.2f" % attr['value']+' '+attr['unit'])
            except TypeError:
                attr_val_label = ttk.Label(perf_frame, text=str(attr['value'])+' '+attr['unit'])
            attr_name_label.grid(column=0, row=row, sticky=W)
            row += 1
            attr_val_label.grid(column=0, row=row, sticky=W)
            row += 1

        # Create label with vehicle image
        image_label = ttk.Label(mainframe, image=self.image)

        # Create buttons frame
        button_frame = ttk.Frame(mainframe, padding=5)
        button_frame.grid(column=0, columnspan=2, row=2, pady='0 5')

        # Create vehicle details and vehicle performance buttons
        vehicle_details_button = ttk.Button(button_frame, text='Vehicle Details', command=display_details)
        vehicle_details_button.pack(padx=5, pady=5, side=LEFT)
        vehicle_performance_button = ttk.Button(button_frame, text='Performance', command=display_performance)
        vehicle_performance_button.pack(padx=5, pady=5, side=LEFT)

        # Grid stuff
        vehicle_name.grid(column=0, columnspan=2, row=0, pady=10)
        image_label.grid(column=0, row=1, padx='5', pady='0 10')
        perf_frame.grid(column=1, row=1, padx='0 5', pady='0 10')
        vehicle_details_button.grid(column=0, columnspan=1, row=2, pady='0 10', sticky=E)
        vehicle_performance_button.grid(column=1, columnspan=1, row=2, pady='0 10')

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


class ViewVehicleDetails(Toplevel):
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


class ViewVehiclePerformance(Toplevel):
    def __init__(self, master, vehicle):
        Toplevel.__init__(self, master)
        self.master = master
        self.vehicle = vehicle
        self.title('Vehicle Performance Tradespace')

        # Place window
        xpos, ypos = get_win_place(self)
        self.geometry('+%d+%d' % (xpos, ypos))

        # Create mainframe and subframes
        self.mainframe = ttk.Frame(self, padding=5)
        self.surfaceplot_frame = SurfacePlot(self, self.vehicle)
        self.button_frame = ttk.Frame(self.mainframe, padding=5)

        # Create button frame widgets
        self.close_button = ttk.Button(self.button_frame, text='Close', command=self.destroy)
        self.close_button.pack(side=RIGHT, padx='3 5')

        self.mainframe.pack()
        self.surfaceplot_frame.pack(fill=BOTH, expand=1)
        self.button_frame.pack(fill=Y, side=RIGHT)


class SurfacePlot(ttk.Frame):
    def __init__(self, master, vehicle):
        ttk.Frame.__init__(self, master, padding=5)
        self.master = master
        self.vehicle = vehicle
        mass = vehicle.mm
        velocity = vehicle.VV
        power = vehicle.power

        # Create plot frame
        self.plot_frame = ttk.Frame(self, padding=5)

        # Create plot frame widgets
        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.ax3d = self.fig.add_subplot(111, projection='3d')

        self.ax3d.set_axisbelow(True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.show()
        Axes3D.mouse_init(self.ax3d)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        # Plot vehicle information
        self.surf = self.ax3d.plot_surface(mass, velocity, power, rstride=1, cstride=1, cmap=mpl.cm.RdBu, linewidth=0, antialiased=False)

        self.ax3d.set_xlabel('Mass (g)')
        self.ax3d.set_ylabel('Forward Speed (m/s)')

        self.ax3d.zaxis.set_major_locator(LinearLocator(10))
        self.ax3d.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        self.fig.colorbar(self.surf, shrink=0.5, aspect=5)
        self.canvas.show()

        # Create toolbar for the envelope plot
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.plot_frame)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        # Pack plot frame
        self.plot_frame.pack(fill=BOTH, expand=YES)