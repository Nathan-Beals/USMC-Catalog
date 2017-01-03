try:                                                                # Error handling for different verisons of python
    import tkinter as tk                                            # Python 3 version
except:
    import Tkinter as tk                                            # Python 2 version

data = [20, 15, 10, 7, 5, 4, 3, 2, 1, 1, 0]                         # Define the data

root = tk.Tk()                                                      # Create a Tk instance
root.title("Tkinter Bar Graph")                                     # Give it a title
c_width = 400                                                       # Define it's width
c_height = 350                                                      # Define it's height
c = tk.Canvas(root, width=c_width, height=c_height, bg= 'white')    # Create a canvas and use the earlier dimensions
c.pack()                                                            # Package everything

                                                                    # The variables below size the bar graph
y_stretch = 15                                                      # The highest y = max_data_value * y_stretch
y_gap = 20                                                          # The gap between lower canvas edge and x axis
x_stretch = 10                                                      # Stretch x wide enough to fit the variables
x_width = 20                                                        # The width of the x-axis
x_gap = 20                                                          # The gap between left canvas edge and y axis
for x, y in enumerate(data):                                        # A quick for loop to calculate the rectangle
                                                                    # coordinates of each bar
    x0 = x * x_stretch + x * x_width + x_gap                        # Bottom left coordinate
    y0 = c_height - (y * y_stretch + y_gap)                         # Top left coordinates
    x1 = x * x_stretch + x * x_width + x_width + x_gap              # Bottom right coordinates
    y1 = c_height #- y_gap                                           # Top right coordinates
    c.create_rectangle(x0, y0, x1, y1, fill="red")                  # Draw the bar
    c.create_text(x0+2, y0, anchor=tk.SW, text=str(y))              # Put the y value above the bar
root.mainloop()