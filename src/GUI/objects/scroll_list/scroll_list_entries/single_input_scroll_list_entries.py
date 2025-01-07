import tkinter as tk

def single_input_scroll_list_entries(root,display_width,entry_height,dictionary, variable,display_height):
    interactive= True

    def button_event(b,variable,key,value):
        print('waht is the nature of hope')
        # this sets the value of the variable for the scroll list equal to the value corresponding to the 
        # key for the button clicked on, unless that button has already been clicked, in which case it 
        # resets the value to none

        for button in b:
            if button[1] == key and variable[0] != key:
                button[0].config(bg='gray70',activebackground = 'gray90')

            else:
                button[0].config(bg="gray90",activebackground = 'gray70')


        if variable[0] != key:
            print('bread')
            variable[:] = [None]
            variable[0] = key
            variable.append(value)
        else:
            variable[:] = [None]

        return True
    
    # this creates button objects corresponding to each entry in the dictionary passed though.
    buttons = []
    print(dictionary.items())
    for (key, value) in dictionary.items():

        Button = tk.Button(root,text = key, height = entry_height,width=display_width)
        Button.config(command= lambda b = buttons, k = key, v = value: button_event(b,variable,k,v), bg='gray90',highlightbackground='gray90', activebackground='gray70')
        buttons.append((Button,key))
        if interactive == False:
            Button.config(state=tk.DISABLED)
        Button.pack(side = 'top',fill='x', expand=(True),pady=(0,5))
    root.update_idletasks()