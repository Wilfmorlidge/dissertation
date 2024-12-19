import tkinter as tk
from PIL import Image, ImageTk
from GUI.objects.scroll_list.scroll_list import scroll_list
from GUI.objects.scroll_list.scroll_list_entries.image_display_scroll_list_entries import update_image_display_entries
from GUI.objects.scroll_list.scroll_list_entries.graph_display_scroll_list_entries import graph_display_scroll_list_entries
from GUI.objects.result_display.result_display import result_display
import threading
import queue
from trial_runner.trial_runner_main import back_end_main_loop

def output_page(root,selected_attack,selected_model,hyperparameter_settings,iteration_size,iteration_number):

    image_queue = queue.Queue()
    graph_queue = queue.Queue()


    for widget in root.winfo_children():
        widget.destroy()

    adversarial_attack_thread = threading.Thread(target = lambda: back_end_main_loop(int(iteration_size.get()),int(iteration_number.get()),selected_attack,selected_model,hyperparameter_settings,image_queue,graph_queue))
    adversarial_attack_thread.daemon = True
    adversarial_attack_thread.start()

    top_frame = tk.Frame(root, bg="dimgray", highlightthickness=2, highlightbackground='black', height=200)
    top_frame.pack(side = 'top',fill = tk.X)
    bottom_frame = tk.Frame(root, bg="dimgray", height=200)
    bottom_frame.pack(side = 'top',fill='both', expand=(True))

    # this section defines the bottom left frame and the attack list
    left_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black')
    scroll_list(left_frame,display_width=100,display_height=300,entry_height=33, dictionary = image_queue, variable = None, entry_function = update_image_display_entries)
    left_frame.pack(side = 'left',fill='both', expand=(True))

    middle_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black')
    result_display(middle_frame,display_width=200,display_height=500)
    middle_frame.pack(side = 'left',fill='both', expand=(True))

    right_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black')
    scroll_list(right_frame,display_width=200,display_height=400,entry_height=100, dictionary = graph_queue, variable = int(iteration_number.get()), entry_function = graph_display_scroll_list_entries)
    right_frame.pack(side = 'left',fill='both', expand=(True))

