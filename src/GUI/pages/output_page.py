import tkinter as tk
from PIL import Image, ImageTk
from GUI.objects.scroll_list.scroll_list import scroll_list
from GUI.objects.scroll_list.scroll_list_entries.image_display_scroll_list_entries import update_image_display_entries
from GUI.objects.scroll_list.scroll_list_entries.graph_display_scroll_list_entries import graph_display_scroll_list_entries
from GUI.objects.result_display.result_display import result_display
from GUI.objects.progress_bar.progress_bar import progress_bar
import threading
from threading import Event
import queue
from trial_runner.trial_runner_main import back_end_main_loop



def output_page(root,selected_attack,selected_model,hyperparameter_settings,iteration_size,iteration_number):

    def window_exit(root,thread_killing_event):
        thread_killing_event.set()
        root.destroy()

    def move_to_landing_page(root,thread_killing_event):
        thread_killing_event.set()
        from GUI.pages.landing_page import landing_page
        landing_page(root)


    image_queue = queue.Queue()
    graph_queue = queue.Queue()
    progress_bar_queue = queue.Queue()


    for widget in root.winfo_children():
        widget.destroy()

    thread_killing_event = Event()

    adversarial_attack_thread = threading.Thread(target = lambda: back_end_main_loop(int(iteration_size.get()),int(iteration_number.get()),selected_attack,selected_model,hyperparameter_settings,image_queue,graph_queue,progress_bar_queue,thread_killing_event))
    adversarial_attack_thread.daemon = True
    adversarial_attack_thread.start()

    root.protocol("WM_DELETE_WINDOW", lambda: window_exit(root,thread_killing_event))

    top_frame = tk.Frame(root, bg="dimgray", highlightthickness=2, highlightbackground='black', height=200)
    progress_bar(top_frame,object_height=100,object_width=1000,iteration_number=int(iteration_number.get()),progress_bar_queue=progress_bar_queue)

    top_frame.pack(side = 'top',fill = tk.X)
    bottom_frame = tk.Frame(root, bg="dimgray", height=200)
    bottom_frame.pack(side = 'top',fill='both', expand=(True))

    # this section defines the bottom left frame and the attack list
    left_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black')
    left_list_label_pair_container = tk.Frame(left_frame, bg='dimgray')
    left_label = tk.Label(left_list_label_pair_container,text='images:',bg='dimgray',font=('helvetica',22))
    left_label.pack(side = 'top',fill='x', expand=(True),pady=(0,50))

    scroll_list(left_list_label_pair_container,display_width=450,display_height=500,entry_height=150, dictionary = image_queue, variable = None, entry_function = update_image_display_entries)
    left_list_label_pair_container.pack(side='top',expand=True,pady =(0,50))
    left_frame.pack(side = 'left',fill='both', expand=(True))

    middle_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black')
    result_display(middle_frame,display_width=500,display_height=800)
    middle_frame.pack(side = 'left',fill='both', expand=(True))

    right_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black')
    right_list_label_pair_container = tk.Frame(right_frame, bg='dimgray')
    right_label = tk.Label(right_list_label_pair_container,text='cumulative metrics:',bg='dimgray',font=('helvetica',22))
    right_label.pack(side = 'top',fill='x', expand=(True),pady=(0,50))
    scroll_list(right_list_label_pair_container,display_width=300,display_height=400,entry_height=100, dictionary = graph_queue, variable = int(iteration_number.get()), entry_function = graph_display_scroll_list_entries)
   
    return_button = tk.Button(right_frame,text = 'return',command = lambda: move_to_landing_page(root,thread_killing_event))
    right_list_label_pair_container.pack(side='top',expand=True,pady =(0,50))
    return_button.pack(side = 'top',pady=(0,50))
    right_frame.pack(side = 'left',fill='both', expand=(True))



