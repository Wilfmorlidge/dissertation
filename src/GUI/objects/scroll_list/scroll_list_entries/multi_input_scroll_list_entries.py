import tkinter as tk


def multi_input_scroll_list_entries(list_frame,display_width,entry_height, dictionary, variable, display_height):
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
        Text_widget.insert(tk.END, value[0])
        variable.append(Text_widget)