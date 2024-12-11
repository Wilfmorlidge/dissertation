import tkinter as tk
from PIL import Image
import numpy as np
import sys
from definitions import attack_dictionary,model_dictionary

def denormalize_and_save_image(image,ident,type):
    display_2 = Image.fromarray(((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8))
    display_2.save(f'./images/{type}/image_{ident}.png')

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
        if variable[0] != key:
            variable[:] = [None]
            variable[0] = key
            variable.append(value)
        else:
            variable[:] = [None]

        return True
    
    for (key, value) in dictionary.items():
        Button = tk.Button(root,text = key,command= lambda k = key, v = value: button_event(variable,k,v), height = entry_height,width=display_width)
        if interactive == False:
            Button.config(state=tk.DISABLED)
        Button.pack(side = 'top',fill='x', expand=(True))
    root.update_idletasks()

def multi_input_scroll_list_entries(list_frame,display_width,entry_height, dictionary, variable):
    interactive= True

    for (key,value) in dictionary.items():
        bounding_frame = tk.Frame(list_frame)
        label = tk.Label(bounding_frame,text=key)
        Text_widget = tk.Text(bounding_frame, width = display_width // 8, height = entry_height)
        Text_widget.config(state=tk.NORMAL)
        label.pack(side = 'top',fill='x', expand=(True))
        Text_widget.pack(side = 'top',fill='x', expand=(True))
        bounding_frame.pack(side = 'top',fill='x', expand=(True))
        variable.append(Text_widget)
    print(variable)


def scroll_list(root,display_width, display_height ,entry_height, dictionary, variable, multi_input):
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
    canvas.create_window((((display_width/2)),0) , window=list_frame, anchor='center')
    scrollbar = ttk.Scrollbar(object_container, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    if multi_input == True:
        multi_input_scroll_list_entries(list_frame,display_width,entry_height, dictionary, variable)
    else:
        single_input_scroll_list_entries(list_frame,display_width,entry_height, dictionary, variable)

    root.update_idletasks()
    expection_frame = tk.Frame(list_frame,height=1, highlightbackground='dimgray', bg='dimgray')
    if list_frame.winfo_height() < display_height:
        expection_frame.pack(side = 'top',fill='both', expand=(True), pady=(0,(display_height-list_frame.winfo_height())))
    else:
        expection_frame.pack(side = 'top',fill='both', expand=(True))


    object_container.pack(side='left',expand=True)
    canvas.pack(side = 'left')
    scrollbar.pack(side = 'left', fill='y')
    object_container.update_idletasks()
    canvas.yview_moveto(0)


def landing_page():
    selected_attack = [None]
    selected_model = [None]
    iteration_size = 5
    iteration_number = 1
    hyperparameter_settings = []

    def create_hyperparameter_list(right_frame,selected_attack,root,previous_selected_attack,hyperparameter_settings):

        
        if (selected_attack[0] != previous_selected_attack[0]):
            print(selected_attack)
            print(previous_selected_attack)
            for widget in right_frame.winfo_children():
                if hasattr(widget, 'custom_tag') and widget.custom_tag == 'scroll_list':
                    print('the ides of march')
                    widget.destroy()
            if (selected_attack[0] != None):
                hyperparameter_settings = []
                print('capitalism')
                print(selected_attack[1]['hyperparameters'])
                scroll_list(right_frame,display_width=200,display_height=300,entry_height=10, dictionary = selected_attack[1]['hyperparameters'], variable = hyperparameter_settings,multi_input = True)
                root.update_idletasks()
            previous_selected_attack = selected_attack.copy()
        root.after(100,lambda: create_hyperparameter_list(right_frame,selected_attack,root,previous_selected_attack,hyperparameter_settings))

    def show_values(selected_attack,selected_model):
        print(selected_attack)
        print(selected_model)
        print(hyperparameter_settings)


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
    iteration_size_scale = tk.Scale(right_frame,orient='horizontal',from_=5,to=100,variable=iteration_size)
    iteration_number_scale = tk.Scale(right_frame,orient='horizontal',from_=1,to=10,variable=iteration_number)
    continue_button = tk.Button(right_frame,text = 'continue',command = lambda: show_values(selected_attack,selected_model))

    # this section defines the choice of hyperparameters for the trials
    root.after(100,lambda: create_hyperparameter_list(right_frame,selected_attack,root,[None],hyperparameter_settings))

    iteration_size_scale.pack(side='top',pady=(10,0))
    iteration_number_scale.pack(side='top',pady=(10,0))
    continue_button.pack(side='bottom')
    right_frame.pack(side = 'left',fill='both', expand=(True))

    root.mainloop()

if __name__ == "__main__":
    landing_page()