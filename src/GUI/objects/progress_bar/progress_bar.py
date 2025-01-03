import tkinter as tk
from tkinter import ttk
import time


def progress_bar(root, object_height, object_width, iteration_number, progress_bar_queue):
    progress = 0
    object_container =  object_container = tk.Frame(root,height = object_height, width = object_width, bg='dimgray', highlightbackground='dimgray')
    start_time = round(time.time())

    def update_progress_bar(object_container,progress,start_time,iteration_number,progress_bar_queue, completion_flag):


        while not progress_bar_queue.empty():
            progress_bar_queue.get()
            progress += 1

        for widget in object_container.winfo_children():
                widget.destroy()

        current_time = round(time.time())


        if (progress >= iteration_number) and (completion_flag == 0):
            completion_flag = 1
            start_time = current_time - start_time


        if completion_flag == 0:
            title = tk.Label(object_container,text=f"Running trials ({progress + 1}|{iteration_number})",bg='dimgray',font=('Helvetica',26))
        else: 
            title = tk.Label(object_container,text=f"trials complete",bg='dimgray',font=('Helvetica',26))

        s = ttk.Style()
        s.theme_use('classic')
        s.configure("red.Horizontal.TProgressbar", background='black', throughcolor='lightblue1')

        progress_bar = ttk.Progressbar(object_container,orient='horizontal',mode='determinate',length=object_width,style="red.Horizontal.TProgressbar")

        progress_bar['value'] = ((progress/iteration_number) * 100)

        if completion_flag == 0:
            sub_title = tk.Label(object_container,text=f" current elapsed time : {current_time - start_time}", name = 'sub_title',bg='dimgray',font=('Helvetica',14))
        else:
            sub_title = tk.Label(object_container,text=f"total elapsed time : {start_time}", name = 'sub_title',bg='dimgray',font=('Helvetica',14))

        title.pack(side = 'top',fill='x', expand=(True))
        progress_bar.pack(side = 'top',fill='x', expand=(True))
        sub_title.pack(side = 'top',fill='x', expand=(True))

        object_container.after(1000,lambda: update_progress_bar(object_container,progress,start_time,iteration_number,progress_bar_queue,completion_flag))


    object_container.after(100,lambda: update_progress_bar(object_container,progress,start_time,iteration_number,progress_bar_queue, completion_flag = 0))

    object_container.pack(side='top',expand=True)