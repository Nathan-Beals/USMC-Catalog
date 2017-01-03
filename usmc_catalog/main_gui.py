#! /usr/bin/env python

try:
    from Tkinter import *
except ImportError:
    from tkinter import *
import ttk
import tkFont
from PIL import ImageTk, Image

from winplace import get_win_place
import os
from vehicle import Vehicle
import tools


class CatalogGUI(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master, padding=3)
        # master.report_callback_exception = self.report_callback_exception
        self.master = master

        # Create subframes within mainframe (i.e., self)
        self.active_filter_frame = ActiveFilters(self)
        self.filter_control_frame = FilterControls(self)
        self.vehicle_alternative_frame = VertScrolledFrame(self)
        self.button_frame = Buttons(self)

        # Grid subframes
        self.filter_control_frame.grid(column=0, row=0, columnspan=2, sticky=(N, S, E, W), pady='5 10')
        self.active_filter_frame.grid(column=0, row=1, sticky=(N, S, E, W), padx='3 10')
        self.vehicle_alternative_frame.grid(column=1, row=1, rowspan=2, sticky=(N, S, E, W))
        self.button_frame.grid(column=0, row=2, sticky=(S, E, W))

        # Manage mainframe resizing
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)


class VertScrolledFrame(ttk.Frame):
    """
    Class for vertical scrolled frame. This blueprint for this code was written by stackOverflow user Gonzo.
    """

    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=self.canvas.yview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = AlternativesSheet(self.canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=NW)

        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)

    # track changes to the canvas and frame width and sync them,
    # also updating the scrollbar
    def _configure_interior(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the inner frame's width to fill the canvas
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())


class AlternativesSheet(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master, width=500, height=300, padding='10 0 10 0', borderwidth=1, relief='ridge')
        self.master = master
        self.current_object_selection = IntVar()

        # Load available vehicles
        self.alternatives = []
        execute_dir = os.path.dirname(os.path.abspath(__file__))
        for vehicle_file in os.listdir('vehicles'):
            vehicle_path = os.path.dirname(execute_dir) + '/vehicles/' + vehicle_file + '/'
            vehicle_name = str(vehicle_file)
            image = None
            attr_names = []
            attr_vals = []
            for filename in os.listdir('vehicles/' + vehicle_file):
                # Get vehicle image and save as ImageTk object
                if filename.endswith(".jpg") or filename.endswith(".png"):
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
                                attr_vals[indx] = [has_video]
                        attr_vals = [val for sublist in attr_vals for val in sublist]
            performance = dict(zip(attr_names, attr_vals))
            self.alternatives.append(Vehicle(vehicle_name, image, performance))

        # Populate alternatives sheet
        self.resort_alt_sheet()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def resort_alt_sheet(self):
        active_filters = self.master.master.master.active_filter_frame.active_filters
        sortby_attr = self.master.master.master.filter_control_frame.sortby_attr

        for widget in self.children.values():
            widget.destroy()

        # Find feasible alternatives based on active filters
        feasible_alternatives = []
        for alternative in self.alternatives:
            if self.apply_filters(alternative, active_filters):
                feasible_alternatives.append(alternative)

        # Sort feasible alternatives based on the sortby_attr
        feasible_alternatives = sorted(feasible_alternatives, key=lambda alt: getattr(alt, sortby_attr), reverse=True)

        row = 0
        column = 0
        for count, alternative in enumerate(feasible_alternatives):
            display_frame = alternative.display_frame(self)

            if count % 2 != 0:
                display_frame.grid(column=column, row=row, pady=10)
                column = 0
                row += 1
            else:
                display_frame.grid(column=column, row=row, pady=10)
                column = 1

    def apply_filters(self, alternative, filters):
            # Filters are of the form (attribute name, min_or_max, value, unit). If attribute name is video then
            # min_or_max is None, value is True, and unit is None.
            for this_filter in filters:
                # Get alternative attribute value in metric
                alternative_attr_val = getattr(alternative, this_filter[0])
                alternative_attr_val = tools.convert_unit(alternative_attr_val['value'], alternative_attr_val['unit'],
                                                          'std_metric')
                # Convert given filter value to metric.
                try:
                    filter_val_metric = tools.convert_unit(this_filter[2], this_filter[3], 'std_metric')
                except tools.ConversionError:
                    filter_val_metric = this_filter[2]
                print "alternative_attr_val = " + str(alternative_attr_val)
                print "filter_val_metric = " + str(filter_val_metric)
                if this_filter[1] == 'min' and not alternative_attr_val >= filter_val_metric:
                    return False
                elif this_filter[1] == 'max' and not alternative_attr_val <= filter_val_metric:
                    return False
            return True


class FilterControls(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master, padding=3)
        self.master = master
        self.sortby_attr = Vehicle.filterby_real_attr_names[0]

        self.sortby_label = ttk.Label(self, text='Sort by')
        self.sortby_combobox = ttk.Combobox(self, state='readonly', values=Vehicle.filterby_pretty_attr_names)
        self.sortby_combobox.bind("<<ComboboxSelected>>", lambda event: self.set_sortby_attr(event))
        self.sortby_combobox.current(0)

        self.filter_attr_label = ttk.Label(self, text='Filter catalog by')
        self.filter_attr_cb = ttk.Combobox(self, state='readonly', values=Vehicle.filterby_pretty_attr_names)
        self.filter_attr_cb.bind("<<ComboboxSelected>>", lambda event: self.refresh_options(event))
        self.filter_attr_cb.current(0)

        self.filter_options_frame, self.filter_options_data = \
            Vehicle.filter_options_frame(self, self.filter_attr_cb.get())

        self.save_filter_button = ttk.Button(self, text='Save Filter', command=self.save_filter)

        self.sortby_label.grid(column=0, row=0, padx='5')
        self.sortby_combobox.grid(column=1, row=0, padx='0 30')
        self.filter_attr_label.grid(column=2, row=0, padx='0 5')
        self.filter_attr_cb.grid(column=3, row=0, padx='0 5')
        self.filter_options_frame.grid(column=4, row=0, padx='0 10')
        self.save_filter_button.grid(column=5, row=0, padx='0 5')

    def refresh_options(self, event=None):
        self.filter_options_frame.destroy()
        filterby_attr = self.filter_attr_cb.get()
        self.filter_options_frame, self.filter_options_data = Vehicle.filter_options_frame(self, filterby_attr)
        self.filter_options_frame.grid(column=4, row=0, padx='0 10')

    def save_filter(self):
        cb1_data = self.filter_options_data[0].get()
        attr_val = self.filter_options_data[1].get()
        cb2_data = self.filter_options_data[2].get()

        filter_attr = \
            Vehicle.filterby_real_attr_names[Vehicle.filterby_pretty_attr_names.index(self.filter_attr_cb.get())]
        if filter_attr == 'video':
            this_filter = (filter_attr, None, cb1_data, None)
        else:
            minormax = cb1_data
            attr_val = attr_val
            attr_unit = cb2_data
            this_filter = (filter_attr, minormax, attr_val, attr_unit)
        self.master.active_filter_frame.set_filter(this_filter)

    def set_sortby_attr(self, event=None):
        self.sortby_attr = \
            Vehicle.filterby_real_attr_names[Vehicle.filterby_pretty_attr_names.index(self.sortby_combobox.get())]
        self.master.vehicle_alternative_frame.interior.resort_alt_sheet()


class ActiveFilters(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master, padding=3, borderwidth=1, relief='ridge')
        self.master = master
        # The format of a filter is a tuple with (attribute name, min_or_max, value, unit)
        self.active_filters = []
        self.sortby_attr = 'endurance'

        # Create actual frame and widgets
        self.active_filters_label = ttk.Label(self, text='Active filters', font='Helvetica 10 bold')
        f = tkFont.Font(self.active_filters_label, self.active_filters_label.cget("font"))
        f.configure(underline=False)
        self.active_filters_label.configure(font=f)

        self.remove_all_label = ttk.Label(self, text='Remove all')
        self.remove_all_button = ttk.Button(self, text='X', command=self.remove_all_filters, width=1)

        self.active_filter_list = ttk.Frame(self)
        self.refresh_frame()

        # Grid widgets
        self.active_filters_label.grid(column=0, row=0, padx='5 15', pady='10', sticky=(N, W))
        self.remove_all_label.grid(column=1, row=0, pady=10, sticky=(N, E))
        self.remove_all_button.grid(column=2, row=0, padx='5 10', pady=6, sticky=(N, E))
        self.active_filter_list.grid(column=0, row=1, columnspan=3, padx=5, sticky=(N, S, E, W))

    def refresh_frame(self):

        for widget in self.active_filter_list.children.values():
            widget.destroy()

        if not self.active_filters:
            text = 'No active filters'
            no_filters_label = ttk.Label(self.active_filter_list, text=text)
            no_filters_label.grid(column=0, row=0, sticky=W)
            return
        for indx, this_filter in enumerate(self.active_filters):
            if this_filter[0] == 'build_time':
                pretty_attr_name = 'build time'
            else:
                pretty_attr_name = this_filter[0]
            constraint_minmax = ''
            if this_filter[1] is not None:
                constraint_minmax = ' ' + this_filter[1]
            constraint_val = '%.3f' % this_filter[2]
            constraint_unit = ''
            if this_filter[3] is not None:
                constraint_unit = ' ' + this_filter[3]

            display_str = pretty_attr_name + constraint_minmax + ' is ' + constraint_val + constraint_unit
            display_label = ttk.Label(self.active_filter_list, text=display_str)
            remove_button = ttk.Button(self.active_filter_list, text='X', command=lambda i=indx: self.remove_filter(i),
                                       width=1)
            display_label.grid(column=0, row=indx, padx='0 3')
            remove_button.grid(column=1, row=indx)

    def set_filter(self, this_filter):
        #  Maybe convert unit to metric std before adding to list?
        self.active_filters.append(this_filter)
        self.refresh_frame()
        self.master.vehicle_alternative_frame.interior.resort_alt_sheet()

    def remove_filter(self, index):
        del self.active_filters[index]
        self.master.vehicle_alternative_frame.interior.resort_alt_sheet()
        self.refresh_frame()
        return

    def remove_all_filters(self):
        self.active_filters = []
        self.master.vehicle_alternative_frame.interior.resort_alt_sheet()
        self.refresh_frame()
        return


class Buttons(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master, padding=3)
        self.master = master

        self.export_vehicle_button = ttk.Button(self, text='Export Vehicle', command=self.export_vehicle)
        self.export_vehicle_button.pack()

    def export_vehicle(self):
        return


def main():
    """
    This is the main function that creates the root Tk window. The mainframe variable is an instance of the QuadGUI
    frame class defined above. The QuadGUI instance will be the parent widget for the rest of the application.
    """
    # First add the directory (in this case masr_design_tool) of the component classes (battery, sensor, propeller, etc)
    # to the system path so that Python can find the modules when it needs to import them.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    root = Tk()
    xpos, ypos = get_win_place(root)
    root.geometry('+%d+%d' % (xpos, ypos))
    root.title("Small UAS Catalog")
    mainframe = CatalogGUI(root)
    mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    #root.protocol('WM_DELETE_WINDOW', mainframe.alternatives_frame.close_tool)
    root.mainloop()


if __name__ == '__main__':
    main()