try:
    from Tkinter import *
except ImportError:
    from tkinter import *
import ttk
import tkFont
#from PIL import ImageTk, Image
from winplace import get_win_place
#from collections import OrderedDict
from tools import convert_unit
#import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
#from matplotlib.backend_bases import key_press_handler
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
#from mpl_toolkits.mplot3d import Axes3D
#from matplotlib.ticker import LinearLocator, FormatStrFormatter
from powerfuns import power_models
#from pylab import meshgrid, cm, imshow, contour, clabel, colorbar, axis, title, show
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
#import matplotlib.pyplot as plt


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
        empty_weight = performance['weight']
        empty_weight_std_val = convert_unit(empty_weight[0], empty_weight[1], 'lbf')
        try:
            battery_capacity = performance['battery_capacity']
            battery_capacity_std_val = convert_unit(battery_capacity[0], battery_capacity[1], 'Wh')
        except KeyError:
            battery_capacity = None

        self.endurance = {'name': 'endurance', 'value': endurance_std_val, 'unit': 'min'}
        self.payload = {'name': 'payload', 'value': payload_std_val, 'unit': 'lbf'}
        self.build_time = {'name': 'build time', 'value': build_time_std_val, 'unit': 'hr'}
        self.max_range = {'name': 'range', 'value': max_range_std_val, 'unit': 'mi'}
        self.video = {'name': 'video', 'value': video[0], 'unit': video[1]}
        self.empty_weight = {'name': 'weight', 'value': empty_weight_std_val, 'unit': 'lbf'}
        if battery_capacity:
            self.battery_capacity = {'name': 'battery capacity', 'value': battery_capacity_std_val, 'unit': 'Wh'}
        else:
            self.battery_capacity = {'name': 'battery capacity', 'value': 'not available', 'unit': ''}
        self.performance = (self.endurance, self.payload, self.build_time, self.max_range, self.video,
                            self.empty_weight, self.battery_capacity)
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
                attr_val_label = ttk.Label(perf_frame, text="%.1f" % attr['value']+' '+attr['unit'])
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
            if type(attr['value']) is float:
                attr_val_label = ttk.Label(perf_frame, text="%0.2f" % attr['value'] + ' ' + str(attr['unit']))
            else:
                attr_val_label = ttk.Label(perf_frame, text=str(attr['value']) + ' ' + str(attr['unit']))
            attr_name_label.grid(column=column, row=0, padx='0 5')
            attr_val_label.grid(column=column, row=1)
            column += 1

        # Create label with vehicle image
        image_label = ttk.Label(mainframe, image=self.image)

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
        xpos, ypos = get_win_place(self)
        self.geometry('+%d+%d' % (xpos, ypos))
        self.mainframe = ttk.Frame(self)
        self.mainframe.pack(fill=BOTH, expand=YES)
        self.title(self.vehicle.name)

        if power_models[self.vehicle.name] is None:
            self.not_avail_label = ttk.Label(self.mainframe, text='Detailed Vehicle Performance Not Available')
            self.not_avail_label.pack(padx=100, pady=75)
            self.close_button = ttk.Button(self.mainframe, text='Close', command=self.destroy)
            self.close_button.pack(side=RIGHT, padx='3 5')
            self.mainframe.pack()
        else:
            # Create subframes
            self.surfaceplot_frame = SurfacePlot(self.mainframe, self.vehicle)
            self.tradespace_frame = TradeSpaceFrame(self.mainframe, self.vehicle)
            self.button_frame = ttk.Frame(self, padding=5)

            # Create button frame widgets
            self.close_button = ttk.Button(self.button_frame, text='Close', command=self.destroy)
            self.close_button.pack(side=RIGHT, padx='3 5')

            # Pack stuff
            self.surfaceplot_frame.pack(side=LEFT, fill=BOTH, expand=1)
            self.tradespace_frame.pack(side=LEFT, fill=BOTH, expand=0)
            self.mainframe.pack(fill=BOTH, expand=1)
            self.button_frame.pack(fill=Y)


class TradeSpaceFrame(ttk.Frame):
    def __init__(self, master, vehicle):
        ttk.Frame.__init__(self, master, padding=5)
        self.master = master
        self.vehicle = vehicle
        max_payload = self.vehicle.payload['value']    # Maximum payload in lbf
        self.power_fun = power_models[self.vehicle.name]

        # Create mainframe
        self.mainframe = ttk.Frame(self, padding=5)

        # Create payload selection widgets
        self.payload_label = ttk.Label(self.mainframe, text='Specify Payload', font=('Helvetica', 16))
        self.payload_label.pack(pady='20 5')

        self.payload_frame = ttk.Frame(self.mainframe)

        self.payload_scale = ttk.Scale(self.payload_frame, orient=HORIZONTAL, length=150, from_=0, to=max_payload,
                                       command=self.payload_change)
        self.payload_scale.pack(side=LEFT)

        self.payload_var = StringVar()
        self.payload_var.set(self.payload_scale.get())

        self.payload_val_label = ttk.Label(self.payload_frame, textvariable=self.payload_var, width=4)
        self.payload_val_label.pack(side=LEFT, padx=3)

        self.payload_unit_label = ttk.Label(self.payload_frame, text='pounds', font=('Helvetica', 12))
        self.payload_unit_label.pack(side=LEFT)

        self.payload_frame.pack()

        # Create maximum range widgets
        self.max_range_label = ttk.Label(self.mainframe, text='Maximum Range', font=('Helvetica', 16))
        self.max_range_label.pack(pady='40 5')

        self.max_range_frame = ttk.Frame(self.mainframe)

        self.max_range_var = DoubleVar()
        self.max_range_var.set(0)
        self.vel_max_range_var = DoubleVar()
        self.vel_max_range_var.set(0)

        self.max_range_label = ttk.Label(self.max_range_frame, textvariable=self.max_range_var, width=4)
        self.max_range_label.pack(side=LEFT)
        self.max_range_unit_label = ttk.Label(self.max_range_frame, text='miles at', font=('Helvetica', 12))
        self.max_range_unit_label.pack(side=LEFT, padx=5)

        self.vel_max_range_label = ttk.Label(self.max_range_frame, textvariable=self.vel_max_range_var, width=4)
        self.vel_max_range_label.pack(side=LEFT)
        self.vel_max_range_unit_label = ttk.Label(self.max_range_frame, text='mph cruise speed', font=('Helvetica', 12))
        self.vel_max_range_unit_label.pack(side=LEFT, padx='5 0')

        self.max_range_frame.pack()

        # Create maximum endurance widgets
        self.max_endurance_label = ttk.Label(self.mainframe, text='Maximum Endurance', font=('Helvetica', 16))
        self.max_endurance_label.pack(pady='40 5')

        self.max_endurance_frame = ttk.Frame(self.mainframe)

        self.max_endurance_var = DoubleVar()
        self.max_endurance_var.set(0)
        self.vel_max_endurance_var = DoubleVar()
        self.vel_max_endurance_var.set(0)

        self.max_endurance_val_label = ttk.Label(self.max_endurance_frame, textvariable=self.max_endurance_var, width=4)
        self.max_endurance_val_label.pack(side=LEFT)
        self.max_endurance_unit_label = ttk.Label(self.max_endurance_frame, text='minutes at', font=('Helvetica', 12))
        self.max_endurance_unit_label.pack(side=LEFT, padx=5)

        self.vel_max_endurance_label = ttk.Label(self.max_endurance_frame, textvariable=self.vel_max_endurance_var,
                                                 width=4)
        self.vel_max_endurance_label.pack(side=LEFT)
        self.vel_max_endurance_unit_label = ttk.Label(self.max_endurance_frame, text='mph cruise speed', font=('Helvetica', 12))
        self.vel_max_endurance_unit_label.pack(side=LEFT, padx='5 0')

        self.max_endurance_frame.pack()

        # Pack mainframe
        self.mainframe.pack()

    def payload_change(self, e=None):
        """
        Event function that updates the gui when the specified payload is changed via the scale.
        :param e:
        :return:
        """
        payload_value = self.payload_scale.get()
        # Update the payload display label
        value_string = "%0.2f" % payload_value
        self.payload_var.set(value_string)

        # Calculate power required for max range and endurance for the given payload
        self.power_fun = power_models[self.vehicle.name]
        this_mass = convert_unit(payload_value + self.vehicle.empty_weight['value'], 'lbf', 'kg') * 1000
        power, mm, VV, m, V = self.power_fun(m=this_mass)
        index_max_endurance = power.argmin()
        power_max_endurance = power[index_max_endurance]
        velocity_max_endurance = VV[index_max_endurance]
        index_max_range = (power/VV).argmin()
        power_max_range = power[index_max_range]
        velocity_max_range = VV[index_max_range]
        max_range = (self.vehicle.battery_capacity['value']/power_max_range) * velocity_max_range * 2.23694    # Max range in miles
        max_endurance = self.vehicle.battery_capacity['value']/power_max_endurance * 60   # Max endurance in minutes

        self.max_range_var.set("%0.2f" % max_range)
        self.vel_max_range_var.set("%0.1f" % velocity_max_range)

        self.max_endurance_var.set("%0.1f" % max_endurance)
        self.vel_max_endurance_var.set("%0.1f" % (velocity_max_endurance * 2.23694))


class SurfacePlot(ttk.Frame):
    def __init__(self, master, vehicle):
        ttk.Frame.__init__(self, master, padding=5)
        self.master = master
        self.vehicle = vehicle
        self.power_fun = power_models[self.vehicle.name]

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
        power, mass_range, velocity_range, mm, VV = self.power_fun()    # mass range in grams, vel range in m/s, power in W
        payload = mass_range - convert_unit(self.vehicle.empty_weight['value'], self.vehicle.empty_weight['unit'], 'kg') * 1000
        payload[payload<0] = 0
        payload *= 0.00220462   # convert grams to lbf
        velocity_range *= 2.23694   # convert m/s to miles per hour
        self.surf = self.ax3d.plot_surface(payload, velocity_range, power, rstride=1, cstride=1, cmap=mpl.cm.RdBu, linewidth=0, antialiased=False)

        self.ax3d.set_xlabel('Payload (lbf)')
        self.ax3d.set_ylabel('Forward Speed (mph)')
        self.ax3d.set_zlabel('Power Required (W)')

        self.ax3d.zaxis.set_major_locator(LinearLocator(10))
        self.ax3d.zaxis.set_major_formatter(FormatStrFormatter('%.0f'))

        self.fig.colorbar(self.surf, shrink=0.5, aspect=5)
        self.canvas.show()

        # Create toolbar for the envelope plot
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.plot_frame)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        # Pack plot frame
        self.plot_frame.pack(fill=BOTH, expand=YES)