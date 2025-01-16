import ast
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def graph_display_scroll_list_entries(list_frame,display_width,entry_height, dictionary, variable, display_height):

    accuracy_frame = tk.Frame(list_frame,height = entry_height, width = display_width,bg='dimgray', highlightbackground='dimgray')
    mean_pertubation_frame = tk.Frame(list_frame,height = entry_height, width = display_width,bg='dimgray', highlightbackground='dimgray')
    GMQ_frame = tk.Frame(list_frame,height = entry_height, width = display_width,bg='dimgray', highlightbackground='dimgray')
    Sharpe_ratio_frame = tk.Frame(list_frame,height = entry_height, width = display_width,bg='dimgray', highlightbackground='dimgray')


    def update_graph_frames(list_frame,display_width,entry_height, dictionary, variable, display_height,accuracy_frame,mean_pertubation_frame,GMQ_frame,Sharpe_ratio_frame):
        flag = 0
        while not dictionary.empty():
            dictionary.get()
            flag = 1

        if flag == 1:
            accuracy_points = []
            mean_pertubation_points = []
            GMQ_points = []
            Sharpe_ratio_points = []

            with open(f"./results/cumulative_metrics.txt", "r") as file:
                # Read all lines into a list
                lines = file.readlines()
            for line in lines:
                values = ast.literal_eval(line)
                accuracy_points.append(values['accuracy'])
                mean_pertubation_points.append(values['mean_pertubation'])
                GMQ_points.append(values['GMQ'])
                Sharpe_ratio_points.append(values['Sharpe_ratio'])

            for widget in accuracy_frame.winfo_children():
                widget.destroy()

            accuracy_label = tk.Label(accuracy_frame,text='accuracy')
            fig = plt.figure()
            dpi = fig.get_dpi()
            fig, ax = plt.subplots(figsize=((display_width/dpi), (entry_height/dpi)))
            ax.plot(accuracy_points)
            ax.set_xlim(0, variable)  # Set x-axis limits
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=accuracy_frame)
            canvas.draw()
            accuracy_label.pack(side='top',fill='both')
            canvas.get_tk_widget().pack(side='top', fill='both', expand=True)
            accuracy_label.metadata = {'y_data':(ax.lines)[0].get_ydata()}

    
            accuracy_frame.pack(side='top', fill='both', expand=True,padx=(0,15),pady=(0,15))

            for widget in mean_pertubation_frame.winfo_children():
                widget.destroy()

            mean_pertubation_label = tk.Label(mean_pertubation_frame,text='mean_pertubation')
            fig = plt.figure()
            dpi = fig.get_dpi()
            fig, ax = plt.subplots(figsize=((display_width/dpi), (entry_height/dpi)))
            ax.plot(mean_pertubation_points)
            ax.set_xlim(0, variable)  # Set x-axis limits
            fig.tight_layout()



            canvas = FigureCanvasTkAgg(fig, master=mean_pertubation_frame)
            canvas.draw()
            mean_pertubation_label.pack(side='top',fill='both')
            canvas.get_tk_widget().pack(side='top', fill='both', expand=True)
            mean_pertubation_label.metadata = {'y_data':(ax.lines)[0].get_ydata()}
    
            mean_pertubation_frame.pack(side='top', fill='both', expand=True,padx=(0,15),pady=(0,15))

            for widget in GMQ_frame.winfo_children():
                widget.destroy()

            GMQ_label = tk.Label(GMQ_frame,text='GMQ')
            fig = plt.figure()
            dpi = fig.get_dpi()
            fig, ax = plt.subplots(figsize=((display_width/dpi), (entry_height/dpi)))
            ax.plot(GMQ_points)
            ax.set_xlim(0, variable)  # Set x-axis limits
            fig.tight_layout()
            print((ax.lines)[0].get_ydata())

            canvas = FigureCanvasTkAgg(fig, master=GMQ_frame)
            canvas.draw()
            GMQ_label.pack(side='top',fill='both')
            canvas.get_tk_widget().pack(side='top', fill='both', expand=True)
            GMQ_label.metadata = {'y_data':(ax.lines)[0].get_ydata()}
    
            GMQ_frame.pack(side='top', fill='both', expand=True,padx=(0,15),pady=(0,15))

            for widget in Sharpe_ratio_frame.winfo_children():
                widget.destroy()

            Sharpe_ratio_label = tk.Label(Sharpe_ratio_frame,text='Sharpe_ratio')
            fig = plt.figure()
            dpi = fig.get_dpi()
            fig, ax = plt.subplots(figsize=((display_width/dpi), (entry_height/dpi)))
            ax.plot(Sharpe_ratio_points)
            ax.set_xlim(0, variable)  # Set x-axis limits
            fig.tight_layout()


            canvas = FigureCanvasTkAgg(fig, master=Sharpe_ratio_frame)
            canvas.draw()
            Sharpe_ratio_label.pack(side='top',fill='both')
            canvas.get_tk_widget().pack(side='top', fill='both', expand=True)
            Sharpe_ratio_label.metadata = {'y_data':(ax.lines)[0].get_ydata()}
    
            Sharpe_ratio_frame.pack(side='top', fill='both', expand=True,padx=(0,15))

        list_frame.after(500, lambda: update_graph_frames(list_frame,display_width,entry_height, dictionary, variable, display_height,accuracy_frame,mean_pertubation_frame,GMQ_frame,Sharpe_ratio_frame))

    list_frame.after(100, lambda: update_graph_frames(list_frame,display_width,entry_height, dictionary, variable, display_height,accuracy_frame,mean_pertubation_frame,GMQ_frame,Sharpe_ratio_frame))

