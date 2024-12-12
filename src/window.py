import tkinter as tk
from PIL import Image
import numpy as np
import sys
from definitions import attack_dictionary,model_dictionary
from main import back_end_main_loop
import threading

from tkinter import ttk

def window(root):
    #this component defines the aesthetic attributes of the window and the application background
    root.title('adversarial trial runner')
    root.geometry("1500x750")
    root.resizable(False, False)
    root.attributes('-topmost', 1)
    root.configure(bg='dimgray')
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

def single_input_scroll_list_entries(root,display_width,entry_height,dictionary, variable):
    interactive= True

    def button_event(variable,key,value):
        # this sets the value of the variable for the scroll list equal to the value corresponding to the 
        # key for the button clicked on, unless that button has already been clicked, in which case it 
        # resets the value to none
        if variable[0] != key:
            variable[:] = [None]
            variable[0] = key
            variable.append(value)
        else:
            variable[:] = [None]

        return True
    
    # this creates button objects corresponding to each entry in the dictionary passed though.
    for (key, value) in dictionary.items():
        Button = tk.Button(root,text = key,command= lambda k = key, v = value: button_event(variable,k,v), height = entry_height,width=display_width)
        if interactive == False:
            Button.config(state=tk.DISABLED)
        Button.pack(side = 'top',fill='x', expand=(True))
    root.update_idletasks()

def multi_input_scroll_list_entries(list_frame,display_width,entry_height, dictionary, variable):
    interactive= True

    # this creates a set of text fields and passes them as the value for a mutable list
    # allowing references to the fields to be accessed from the parent process, thus allowing
    # a subset of their values to be retrieved from same.
    for (key,value) in dictionary.items():
        bounding_frame = tk.Frame(list_frame)
        label = tk.Label(bounding_frame,text=key)
        Text_widget = tk.Text(bounding_frame, width = display_width // 8, height = entry_height)
        Text_widget.config(state=tk.NORMAL)
        label.pack(side = 'top',fill='x', expand=(True))
        Text_widget.pack(side = 'top',fill='x', expand=(True))
        bounding_frame.pack(side = 'top',fill='x', expand=(True))
        variable.append(Text_widget)


def scroll_list(root,display_width, display_height ,entry_height, dictionary, variable, multi_input):
    #this section puts the frame containing the scroll list entries into a scrollable canvas, and updates the canvases configure to make it 
    # changes shape with the frame.
    object_container = tk.Frame(root,height = 50, width = display_width, bg='dimgray', highlightbackground='dimgray')
    object_container.custom_tag = 'scroll_list'
    canvas = tk.Canvas(object_container, width = (display_width-4), height = display_height, bg='dimgray', highlightbackground='dimgray')
    list_frame = tk.Frame(canvas, bg="dimgray", highlightbackground='dimgray')
    list_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
    )
    canvas.update_idletasks()

    # this places the frame as a window in the canvas, and assigns a scroll bar
    canvas.create_window((((display_width/2)),0) , window=list_frame, anchor='center')
    scrollbar = ttk.Scrollbar(object_container, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)


    # this determines what kind of entries will be in the scroll list, and then calls the appropriate function
    # this doesn't feel very exstensible so i will try to refactor it after i have finished a first pass at the entire
    # front end
    if multi_input == True:
        multi_input_scroll_list_entries(list_frame,display_width,entry_height, dictionary, variable)
    else:
        single_input_scroll_list_entries(list_frame,display_width,entry_height, dictionary, variable)

    root.update_idletasks()
    #once the list is initially rendered, this section calculates if the list entries have a combined height of less than the screen
    # and pads under them if they do, thus preventing users from scrolling down when they can already see the whole list.
    exception_frame = tk.Frame(list_frame,height=1, highlightbackground='dimgray', bg='dimgray')
    if list_frame.winfo_height() < display_height:
        exception_frame.pack(side = 'top',fill='both', expand=(True), pady=(0,(display_height-list_frame.winfo_height())))
    else:
        exception_frame.pack(side = 'top',fill='both', expand=(True))

    # this finalises the geoemtry manager positions for the objects
    object_container.pack(side='left',expand=True)
    canvas.pack(side = 'left')
    scrollbar.pack(side = 'left', fill='y')
    object_container.update_idletasks()
    canvas.yview_moveto(0)


def landing_page():
    selected_attack = [None]
    selected_model = [None]
    hyperparameter_settings = []

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
                scroll_list(right_frame,display_width=200,display_height=300,entry_height=10, dictionary = selected_attack[1]['hyperparameters'], variable = hyperparameter_settings,multi_input = True)
                root.update_idletasks()
            previous_selected_attack = selected_attack.copy()
        root.after(100,lambda: create_hyperparameter_list(right_frame,selected_attack,root,previous_selected_attack,hyperparameter_settings))

    def move_to_output_page(selected_attack,selected_model,hyperparameter_settings,iteration_size,iteration_number,root):
        print(selected_attack)
        print(selected_model)
        print(iteration_number.get())
        print(iteration_size.get())
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
        adversarial_attack_thread = threading.Thread(target = lambda: back_end_main_loop(int(iteration_size.get()),int(iteration_number.get()),selected_attack,selected_model,hyperparameter_settings))
        adversarial_attack_thread.start()



    root = tk.Tk()

    # this section defines the root and the background frame
    window(root)
    top_frame = tk.Frame(root, bg="dimgray", highlightthickness=2, highlightbackground='black', height=200)
    top_frame.pack(side = 'top',fill = tk.X)
    bottom_frame = tk.Frame(root, bg="dimgray", height=200)
    bottom_frame.pack(side = 'top',fill='both', expand=(True))

    # this section defines the bottom left frame and the attack list
    left_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black')
    scroll_list(left_frame,display_width=200,display_height=300,entry_height=10, dictionary = attack_dictionary, variable = selected_attack, multi_input = False)
    left_frame.pack(side = 'left',fill='both', expand=(True))

    # this section defines the bottom middle frame and the model list
    middle_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black')
    scroll_list(middle_frame,display_width=100,display_height=200,entry_height=5, dictionary =  model_dictionary, variable = selected_model, multi_input = False)
    middle_frame.pack(side = 'left',fill='both', expand=(True))


    # this section defines the bottom right frame and the parameter setting form
    right_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black')
    iteration_size = tk.DoubleVar()
    iteration_number = tk.DoubleVar()
    iteration_size_scale = tk.Scale(right_frame,orient='horizontal',from_=5,to=100,variable=iteration_size)
    iteration_number_scale = tk.Scale(right_frame,orient='horizontal',from_=1,to=10,variable=iteration_number)
    continue_button = tk.Button(right_frame,text = 'continue',command = lambda: move_to_output_page(selected_attack,selected_model,hyperparameter_settings,iteration_size,iteration_number,root))

    # this section defines the choice of hyperparameters for the trials
    root.after(100,lambda: create_hyperparameter_list(right_frame,selected_attack,root,[None],hyperparameter_settings))

    iteration_size_scale.pack(side='top',pady=(10,0))
    iteration_number_scale.pack(side='top',pady=(10,0))
    continue_button.pack(side='bottom')
    right_frame.pack(side = 'left',fill='both', expand=(True))

    root.mainloop()

if __name__ == "__main__":
    landing_page()