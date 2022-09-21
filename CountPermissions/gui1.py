"""
see hello3.py for using frames.
This script shows how to use frames for Matplotlib plots in TKinter.
"""
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
  FigureCanvasTkAgg,
  NavigationToolbar2Tk
)

color1='light yellow'
color2='white' #'light yellow'
color3 = 'pink'
color4 = "#007fff"


def add_notebook_in_frame(container):
    notebook_widget = ttk.Notebook(container, style='notebook_frame.TFrame')

    notebook_widget.pack(fill="both", expand=True)

    # Tab #1
    tab_1 = ttk.Frame(notebook_widget)
    for index in [0, 1]:
        tab_1.columnconfigure(index=index, weight=1)
        tab_1.rowconfigure(index=index, weight=1)
    notebook_widget.add(tab_1, text="Tab 1")

    # Label
    label = ttk.Label(
        tab_1,
        text="Azure theme for ttk",
        justify="center",
        font=("-size", 15, "-weight", "bold"),
    )
    label.grid(row=1, column=0, pady=10, columnspan=2)

    # Tab #2
    tab_2 = ttk.Frame(notebook_widget, style='notebook_tabs.TFrame')
    notebook_widget.add(tab_2, text="Tab 2")

    # Tab #3
    tab_3 = ttk.Frame(notebook_widget)
    notebook_widget.add(tab_3, text="Tab 3")

    # t1 = ttk.Frame(notebook_widget)
    # t2 = ttk.Frame(notebook_widget)
    # notebook_widget.add(t1, text='Notebook tab1')
    # notebook_widget.add(t2, text='Notebook tab2')
    # notebook_widget.pack(expand=1, fill="both")
    return notebook_widget


def create_2_frames(container):
    frame1 = ttk.Frame(container, borderwidth=1, relief='solid', name='up_frame', style='upper_frame.TFrame')
    frame2 = ttk.Frame(container, borderwidth=0, relief='solid', name='down_frame')
    #frame2 = ttk.LabelFrame(container, text="םישרת", borderwidth=1, relief='solid', name='down_frame', style='any_name.TFrame')
    frame1.grid(row=0, column=0,
               sticky='nsew',
               padx=5, pady=5  # this put space between container and containee (here:root window and the frame)
               )
    frame2.grid(row=1, column=0,
               sticky='nsew',
               padx=5, pady=5  # this put space between container and containee (here:root window and the frame)
               )
    container.columnconfigure(0, weight=1)
    container.rowconfigure(0, weight=1)
    container.columnconfigure(0, weight=1)
    container.rowconfigure(1, weight=2)

    # return both frames
    return frame1, frame2


def create_widgets(container):
    val = "    " + "ספר היבוא והמכס"[::-1]
    hello_label = ttk.Label(container, text=val, font=("TkDefaultFont", 64)
                            , background=color3, foreground='black'
                            )#, wraplength=600, background='orange')

    hello_label.grid(row=0, column=0, #columnspan=4,
                     padx=5, pady=10, sticky=(tk.W + tk.E))



def get_hardcoded_values():
    d1 = {'0101': 214, '0102': 219, '0103': 2, '0104': 1547, '0105': 1, '0107': 13, '0109': 37, '0110': 4,
          '0201': 261, '0202': 15, '0203': 6, '0204': 401, '0209': 147, '0210': 81, '0212': 124, '0213': 4,
          '0214': 11, '0215': 124, '0217': 39, '0218': 20, '0219': 1509, '0221': 16, '0222': 21, '0302': 54,
          '0303': 15, '0305': 36, '0307': 5, '0308': 324, '0309': 3, '0310': 49, '0311': 231, '0315': 70,
          '0319': 457, '0325': 1884, '0402': 1886, '0501': 1, '0602': 24, '0603': 35, '0604': 11, '0701': 583,
          '0702': 284, '0703': 99, '0704': 164, '0705': 582, '0706': 30, '0708': 15, '0709': 6, '0710': 143,
          '0713': 1, '0715': 11, '0804': 9, '1001': 18, '1101': 11, '1201': 3, '1203': 21, '1204': 1, '1301': 98,
          '2101': 3, '2301': 311, '2303': 281, '2402': 1883}
    d2 = {'0101': 181, '0102': 189, '0103': 2, '0104': 1405, '0105': 1, '0107': 12, '0109': 28, '0110': 4,
          '0201': 234, '0202': 14, '0203': 2, '0204': 373, '0209': 130, '0210': 64, '0212': 120, '0213': 4,
          '0214': 11, '0215': 92, '0217': 32, '0218': 16, '0219': 1373, '0221': 9, '0222': 14, '0302': 51,
          '0303': 10, '0305': 35, '0307': 5, '0308': 277, '0309': 3, '0310': 45, '0311': 186, '0315': 57,
          '0319': 387, '0325': 1714, '0402': 1716, '0501': 0, '0602': 19, '0603': 28, '0604': 10, '0701': 500,
          '0702': 248, '0703': 97, '0704': 140, '0705': 499, '0706': 29, '0708': 15, '0709': 4, '0710': 122,
          '0713': 1, '0715': 10, '0804': 9, '1001': 17, '1101': 2, '1201': 3, '1203': 17, '1204': 0, '1301': 87,
          '2101': 3, '2301': 277, '2303': 252, '2402': 1713}
    return d1, d2


class CanvasPlotView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.figure = Figure(figsize=(6, 4), dpi=100, layout='tight')   # layout='tight' is mandatory in order to see x labels correctly!
        #self.figure = Figure(figsize=(16, 4), dpi=100) # it seems that the figsize args change nothing!
        self.canvas_tkagg = FigureCanvasTkAgg(self.figure, master=self)
        canvas = self.canvas_tkagg.get_tk_widget()
        canvas.pack(fill='both', expand=True)

    def draw_something_else(self, legend_str_without, legend_str_with):
        d1, d2 = get_hardcoded_values()
        self.axes = self.figure.add_subplot(1, 1, 1)
        #pl = plt.bar(d1.keys(), d1.values(), width=0.5, linewidth=2, label=legend_str_without[::-1])
        self.axes.bar(d1.keys(), d1.values(), label=legend_str_without[::-1])
        self.axes.bar(d2.keys(), d2.values(), label=legend_str_with[::-1])
        self.axes.set_title("כמה פריטי מכס צריכים אישור זה"[::-1], fontsize=15)
        self.axes.set_xlabel('קוד אישור'[::-1], fontsize=15)
        self.axes.set_ylabel('מספר פריטים'[::-1], fontsize=15)
        # self.axes.set_visible(False) This remove the graph from view
        self.axes.set_xticklabels(d1.keys(), rotation=90)
        self.axes.legend()


def show_yield_chart(container, *_):
    chart = CanvasPlotView(container)

    # Note: the sticky="news" is mandatory if we want the frame to stick to all 4 sides of the container
    # padx=15, pady=15 put space between container and containee (here:root window and the frame)
    chart.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    container.columnconfigure(0, weight=1)
    container.rowconfigure(0, weight=1)

    legend_str_without, legend_str_with = ( "כולל ללא הצהרות יבוא", "רק עם הצהרות יבוא" )
    chart.draw_something_else(legend_str_without, legend_str_with)


def tab_in_notebook(notebook_widget, tab_number):
    notebook_tab = list(notebook_widget.children.items())[tab_number][1]  # the tab_number tab in the notebook
    return notebook_tab


class MyApplication(tk.Tk):
    """Hello World Main Application"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tk.call("source", "Azure-ttk-theme/azure.tcl")
        self.tk.call("set_theme", "dark")

        self.title("ספר היבוא והמכס")
        self.geometry("1200x800")
        self.resizable(width=True, height=True)
        #add_window_attributes(self)

        s = ttk.Style()
        # The following line, if uncommented, causes the tabs to lose the azure style!
        # but if commented, we don't get the background colors!!
        #s.configure('TFrame', background=color1)   # 1st arg must be the string TFrame (different string for each widget type!)
        s.configure('upper_frame.TFrame', background=color3)
        s.configure('notebook_frame.TFrame', background=color1)
        s.configure('notebook_tabs.TFrame', background=color4)

        frame = ttk.Frame(self, borderwidth=1, relief='solid', name='root_frame', style='notebook_frame.TFrame')
#                          , style='TFrame')

        frame.grid(row=0, column=0,
                   sticky='nsew',
                   # Note: the sticky="news" is mandatory if we want the frame to stick to all 4 sides of the container
                   padx=5, pady=5  # this put space between container and containee (here:root window and the frame)
                   )
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        up_frame, down_frame = create_2_frames(frame)
        create_widgets(up_frame)
        notebook_widget = add_notebook_in_frame(down_frame)
        notebook_frame_2 = tab_in_notebook(notebook_widget, 1)     # the 2nd tab in the notebook
        notebook_widget.select(1)
        #self.update()
        show_yield_chart(notebook_frame_2)

        self.bind('<Escape>', lambda e: self.destroy())


if __name__ == "__main__":
    myApp = MyApplication()

    myApp.mainloop()
