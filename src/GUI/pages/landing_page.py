import tkinter as tk
import threading
import queue
import sys

sys.path.insert(0, './src')

from definitions import attack_dictionary,model_dictionary

from trial_runner.trial_runner_main import back_end_main_loop
from GUI.objects.scroll_list.scroll_list import scroll_list
from GUI.objects.scroll_list.scroll_list_entries.single_input_scroll_list_entries import single_input_scroll_list_entries
from GUI.objects.scroll_list.scroll_list_entries.multi_input_scroll_list_entries import multi_input_scroll_list_entries
from GUI.objects.window.window import window
from GUI.pages.output_page import output_page


def create_hyperparameter_list(right_frame,selected_attack,root,previous_selected_attack,hyperparameter_settings):
    #this is a self calling function which runs in a child thread and watches for changes in the attack selection

    #this if statements makes sure nothing happens when the attack has not been changed since the last run of this function
    if (selected_attack[0] != previous_selected_attack[0]):
        # where the attack has changed the current hyeprparameter list is deleted
        for widget in right_frame.winfo_children():
            if hasattr(widget, 'custom_tag') and widget.custom_tag == 'scroll_list':
                widget.destroy()
        # where another attack has been selected, instead of the current attack being de-selected, then a new hyperparameter list is made
        if (selected_attack[0] != None):
            # this resets the hyperparameter setting list so it does not contain none-existent text fields
            if hyperparameter_settings[:] != []:
                hyperparameter_settings[:] = []
            # this creates a multi input scroll list and captures the text fields within said list as the values for hyperparameter settings
            scroll_list(right_frame,display_width=200,display_height=300,entry_height=10, dictionary = selected_attack[1]['hyperparameters'], variable = hyperparameter_settings, entry_function= multi_input_scroll_list_entries)
            root.update_idletasks()
        previous_selected_attack = selected_attack.copy()
    root.after(100,lambda: create_hyperparameter_list(right_frame,selected_attack,root,previous_selected_attack,hyperparameter_settings))


def move_to_output_page(root,selected_attack,selected_model,hyperparameter_settings,iteration_size,iteration_number):
    print(selected_attack)
    print(selected_model)
    print(iteration_number.get())
    print(iteration_size.get())

    if (selected_attack != [None]) and (selected_model != [None]):
    #this resolves the values of the hyperparameter_settings text fields into actual float values for the hyperparameters.
        for i in range(len(hyperparameter_settings)):
            # this gets the value in text field i and converts it into a list of floats (under the assumption that the entry to the field is in csv float format)
            # then splits the string into substrings via commas and converts the substrings to floats
            value = hyperparameter_settings[i].get(0.0,'end')
            if value.strip() == "":
                hyperparameter_settings[i] = []
            else:
                hyperparameter_settings[i] = [float(x) for x in value.split(',')]
        print(hyperparameter_settings)
        output_queue = queue.Queue()
        adversarial_attack_thread = threading.Thread(target = lambda: back_end_main_loop(int(iteration_size.get()),int(iteration_number.get()),selected_attack,selected_model,hyperparameter_settings,output_queue))
        adversarial_attack_thread.daemon = True
        adversarial_attack_thread.start()
        output_page(root,output_queue)

def landing_page():
    selected_attack = [None]
    selected_model = [None]
    hyperparameter_settings = []

    root = tk.Tk()

    # this section defines the root and the background frame
    window(root)
    top_frame = tk.Frame(root, bg="dimgray", highlightthickness=2, highlightbackground='black', height=200)
    top_frame.pack(side = 'top',fill = tk.X)
    bottom_frame = tk.Frame(root, bg="dimgray", height=200)
    bottom_frame.pack(side = 'top',fill='both', expand=(True))

    # this section defines the bottom left frame and the attack list
    left_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black')
    scroll_list(left_frame,display_width=200,display_height=300,entry_height=10, dictionary = attack_dictionary, variable = selected_attack, entry_function = single_input_scroll_list_entries)
    left_frame.pack(side = 'left',fill='both', expand=(True))

    # this section defines the bottom middle frame and the model list
    middle_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black')
    scroll_list(middle_frame,display_width=100,display_height=200,entry_height=5, dictionary =  model_dictionary, variable = selected_model, entry_function = single_input_scroll_list_entries)
    middle_frame.pack(side = 'left',fill='both', expand=(True))


    # this section defines the bottom right frame and the parameter setting form
    right_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black')
    iteration_size = tk.DoubleVar()
    iteration_number = tk.DoubleVar()
    iteration_size_scale = tk.Scale(right_frame,orient='horizontal',from_=5,to=100,variable=iteration_size)
    iteration_number_scale = tk.Scale(right_frame,orient='horizontal',from_=1,to=10,variable=iteration_number)
    continue_button = tk.Button(right_frame,text = 'continue',command = lambda: move_to_output_page(root,selected_attack,selected_model,hyperparameter_settings,iteration_size,iteration_number))

    # this section creates a callback loop which renders the hyperparameter list only when a valid attack has been chosen.
    root.after(100,lambda: create_hyperparameter_list(right_frame,selected_attack,root,[None],hyperparameter_settings))

    iteration_size_scale.pack(side='top',pady=(10,0))
    iteration_number_scale.pack(side='top',pady=(10,0))
    continue_button.pack(side='bottom')
    right_frame.pack(side = 'left',fill='both', expand=(True))

    root.mainloop()

if __name__ == "__main__":
    landing_page()