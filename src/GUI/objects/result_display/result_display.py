import tkinter as tk
import ast

def result_display(root,display_height, display_width):


    object_container = tk.Frame(root, height = display_height, width=display_width)


    def update_main_body(object_container):

        for widget in object_container.winfo_children():
            widget.destroy()

        with open(f"./results/cumulative_metrics.txt", "r") as file:
            # Read all lines into a list
            lines = file.readlines()
            current_cumulative_values = ast.literal_eval(lines[-1])
        
        accuracy_container = tk.Frame(object_container)

        accuracy_label = tk.Label(accuracy_container, text='accuracy')
        accuracy_display = tk.Label(accuracy_container,text=str(current_cumulative_values['accuracy']))

        accuracy_label.pack(side='top')
        accuracy_display.pack(side='top')

        mean_pertubation_container = tk.Frame(object_container)
        mean_pertubation_label = tk.Label(mean_pertubation_container,text='mean pertubation')
        mean_pertubation_display = tk.Label(mean_pertubation_container,text=str(current_cumulative_values['mean_pertubation']))

        mean_pertubation_label.pack(side='top')
        mean_pertubation_display.pack(side='top')

        GMQ_container = tk.Frame(object_container)
        GMQ_label = tk.Label(GMQ_container,text='GMQ')
        GMQ_display = tk.Label(GMQ_container,text=str(current_cumulative_values['GMQ']))

        GMQ_label.pack(side='top')
        GMQ_display.pack(side='top')

        Sharpe_ratio_container = tk.Frame(object_container)
        Sharpe_ratio_label = tk.Label(Sharpe_ratio_container,text='Sharpe ratio')
        Sharpe_ratio_display = tk.Label(Sharpe_ratio_container,text=str(current_cumulative_values['Sharpe_ratio']))

        Sharpe_ratio_label.pack(side='top')
        Sharpe_ratio_display.pack(side='top')

        accuracy_container.pack(side = 'top',fill='both', expand=(True))
        mean_pertubation_container.pack(side = 'top',fill='both', expand=(True))
        GMQ_container.pack(side = 'top',fill='both', expand=(True))
        Sharpe_ratio_container.pack(side = 'top',fill='both', expand=(True))

        object_container.pack(side='left',expand=True)

        root.after(500,lambda: update_main_body(object_container))

    root.after(100,lambda: update_main_body(object_container))


 