import tkinter as tk
import sys

sys.path.insert(0, './src')

from definitions import attack_dictionary,model_dictionary

from GUI.objects.scroll_list.scroll_list import scroll_list
from GUI.objects.scroll_list.scroll_list_entries.single_input_scroll_list_entries import single_input_scroll_list_entries
from GUI.objects.scroll_list.scroll_list_entries.multi_input_scroll_list_entries import multi_input_scroll_list_entries


def create_hyperparameter_list(right_frame,selected_attack,root,previous_selected_attack,hyperparameter_settings):
    #this is a self calling function which runs in a child thread and watches for changes in the attack selection

    #this if statements makes sure nothing happens when the attack has not been changed since the last run of this function
    #print(selected_attack)
    #print(previous_selected_attack)
    #print("--------------------------")
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


def continue_button_activity_check(root,continue_button,selected_model,selected_attack):
    if selected_model != [None] and selected_attack != [None]:
        continue_button.config(state=tk.NORMAL,bg='gray95')
    root.after(100, lambda: continue_button_activity_check(root,continue_button,selected_model,selected_attack))

def move_to_output_page(root,selected_attack,selected_model,hyperparameter_settings,iteration_size,iteration_number):
    print(selected_attack)
    print(selected_model)
    print(iteration_number.get())
    print(iteration_size.get())

    from GUI.pages.output_page import output_page

    #if (selected_attack != [None]) and (selected_model != [None]):
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
    output_page(root,selected_attack,selected_model,hyperparameter_settings,iteration_size,iteration_number)

def landing_page(root):

    for widget in root.winfo_children():
        widget.destroy()

    selected_attack = [None]
    selected_model = [None]
    hyperparameter_settings = []

    bottom_frame = tk.Frame(root, bg="dimgray", height=200)
    bottom_frame.pack(side = 'top',fill='both', expand=(True))

    # this section defines the bottom left frame and the attack list
    left_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black', width = 500)
    left_list_label_pair_container = tk.Frame(left_frame, bg='dimgray')
    left_label = tk.Label(left_list_label_pair_container,text='attacks:',bg='dimgray',font=('helvetica',22))
    left_label.pack(side = 'top',fill='x', expand=(True),pady=(0,50))
    scroll_list(left_list_label_pair_container,display_width=200,display_height=400,entry_height=2, dictionary = attack_dictionary, variable = selected_attack, entry_function = single_input_scroll_list_entries)
    left_list_label_pair_container.pack(side='top',expand=True,pady =(0,50))
    left_frame.pack(side = 'left',fill='both', expand=(True))

    # this section defines the bottom middle frame and the model list
    middle_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black', width = 500)
    middle_list_label_pair_container = tk.Frame(middle_frame, bg='dimgray')
    middle_label = tk.Label(middle_list_label_pair_container,text='models:',bg='dimgray',font=('helvetica',22))
    middle_label.pack(side = 'top',fill='x', expand=(True),pady=(0,50))
    scroll_list(middle_list_label_pair_container,display_width=200,display_height=400,entry_height=2, dictionary =  model_dictionary, variable = selected_model, entry_function = single_input_scroll_list_entries)
    middle_list_label_pair_container.pack(side='top',expand=True,pady =(0,50))
    middle_frame.pack(side = 'left',fill='both', expand=(True))


    # this section defines the bottom right frame and the parameter setting form
    right_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black', width = 500)
    iteration_size = tk.DoubleVar()
    iteration_number = tk.DoubleVar()
    iteration_size_scale_container = tk.Frame(right_frame, bg = 'dimgray')
    iteration_size_label = tk.Label(iteration_size_scale_container,text='images per iteration:',bg='dimgray',font=('helvetica',14),anchor='w',justify='left')
    iteration_size_scale = tk.Scale(iteration_size_scale_container,orient='horizontal',from_=5,to=250,variable=iteration_size, width = 10, length = 400)

    iteration_size_label.pack(side='top',expand=True,pady =(0,10))
    iteration_size_scale.pack(side='top')

    iteration_number_scale_container = tk.Frame(right_frame, bg = 'dimgray')
    iteration_number_label = tk.Label(iteration_number_scale_container,text='number of iterations:',bg='dimgray',font=('helvetica',14),anchor='w',justify='left')
    iteration_number_scale = tk.Scale(iteration_number_scale_container,orient='horizontal',from_=5,to=25,variable=iteration_number, width = 10, length = 400)

    iteration_number_label.pack(side='top',expand=True,pady =(0,10))
    iteration_number_scale.pack(side='top')



    #right_list_label_pair_container = tk.Frame(right_frame, bg='dimgray')
    right_label = tk.Label(right_frame,text='hyperparameter settings:',bg='dimgray',font=('helvetica',22))
    continue_button = tk.Button(right_frame,text = 'continue',command = lambda: move_to_output_page(root,selected_attack,selected_model,hyperparameter_settings,iteration_size,iteration_number), bg = 'gray30', state = tk.DISABLED)

    # this section creates a callback loop which renders the hyperparameter list only when a valid attack has been chosen.
    root.after(100,lambda: create_hyperparameter_list(right_frame,selected_attack,root,[None],hyperparameter_settings))

    # this section calls back to check whether the continue button should appear disabled

    root.after(100,lambda: continue_button_activity_check(root,continue_button,selected_model,selected_attack))

    iteration_size_scale_container.pack(side='top',pady=(10,0))
    iteration_number_scale_container.pack(side='top',pady=(100,0))
    right_label.pack(side = 'top',pady=(50,0))
    continue_button.pack(side='bottom', pady=(0,50))
    right_frame.pack(side = 'left',fill='both', expand=(True))

