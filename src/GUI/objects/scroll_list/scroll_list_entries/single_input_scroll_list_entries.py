import tkinter as tk

def single_input_scroll_list_entries(root,display_width,entry_height,dictionary, variable,display_height):
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