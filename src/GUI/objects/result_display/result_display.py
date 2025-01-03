import tkinter as tk
import ast

def result_display(root,display_height, display_width):


    object_container = tk.Frame(root, height = display_height, width=display_width,bg='dimgray')


    def update_main_body(object_container):

        for widget in object_container.winfo_children():
            widget.destroy()

        with open(f"./results/cumulative_metrics.txt", "r") as file:
            # Read all lines into a list
            lines = file.readlines()
            current_cumulative_values = ast.literal_eval(lines[-1])
        
        accuracy_container = tk.Frame(object_container,bg='dimgray')

        accuracy_label = tk.Label(accuracy_container, text='accuracy',bg='dimgray',font=('helvetica',20))
        accuracy_display = tk.Label(accuracy_container,text=str(current_cumulative_values['accuracy']),bg='dimgray',fg='white',font=('helvetica',20))

        accuracy_label.pack(side='top',pady=(0,25))
        accuracy_display.pack(side='top')

        mean_pertubation_container = tk.Frame(object_container,bg='dimgray')
        mean_pertubation_label = tk.Label(mean_pertubation_container,text='mean pertubation',bg='dimgray',font=('helvetica',20))
        mean_pertubation_display = tk.Label(mean_pertubation_container,text=str(current_cumulative_values['mean_pertubation']),bg='dimgray',fg='white',font=('helvetica',20))

        mean_pertubation_label.pack(side='top',pady=(0,25))
        mean_pertubation_display.pack(side='top')

        GMQ_container = tk.Frame(object_container,bg='dimgray')
        GMQ_label = tk.Label(GMQ_container,text='GMQ',bg='dimgray',font=('helvetica',20))
        GMQ_display = tk.Label(GMQ_container,text=str(current_cumulative_values['GMQ']),bg='dimgray',fg='white',font=('helvetica',20))

        GMQ_label.pack(side='top',pady=(0,25))
        GMQ_display.pack(side='top')

        Sharpe_ratio_container = tk.Frame(object_container,bg='dimgray')
        Sharpe_ratio_label = tk.Label(Sharpe_ratio_container,text='Sharpe ratio',bg='dimgray',font=('helvetica',20))
        Sharpe_ratio_display = tk.Label(Sharpe_ratio_container,text=str(current_cumulative_values['Sharpe_ratio']),bg='dimgray',fg='white',font=('helvetica',20))

        Sharpe_ratio_label.pack(side='top',pady=(0,25))
        Sharpe_ratio_display.pack(side='top')

        accuracy_container.pack(side = 'top',fill='both', expand=(True),pady=(0,50))
        mean_pertubation_container.pack(side = 'top',fill='both', expand=(True),pady=(0,50))
        GMQ_container.pack(side = 'top',fill='both', expand=(True),pady=(0,50))
        Sharpe_ratio_container.pack(side = 'top',fill='both', expand=(True),pady=(0,50))

        object_container.pack(side='left',expand=True)

        root.after(500,lambda: update_main_body(object_container))

    root.after(100,lambda: update_main_body(object_container))


 