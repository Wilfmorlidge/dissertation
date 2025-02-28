import os
import tkinter as tk
from PIL import Image, ImageTk
import time


def update_image_display_entries(root,display_width,entry_height,dictionary, variable, display_height):

    def load_current_page_of_entries(root,display_width,entry_height,dictionary, variable, display_height,page_number):
        for widget in root.winfo_children():
            if not(widget.winfo_name() == 'exception_frame') and not(widget.winfo_name() == 'page_button_container'):
                widget.destroy()



        for counter in range((150*page_number),min((len(variable[2])-1),((150*page_number)+150))):
            construct_entry(root,display_width,entry_height,dictionary, variable[2][counter], display_height)



    def construct_entry(root,display_width,entry_height,dictionary, entry, display_height):
        container_container = tk.Frame(root,bg='dimgray')
        listing_container = tk.Frame(container_container, height = int(entry_height * 1/5))
        listing = tk.Label(listing_container,text=f"{entry[0]}:{entry[1]}")

        image_container = tk.Frame(container_container, height = int(entry_height * 4/5))

        unpertubed_image = Image.open( f"./results/trial_{entry[0]}/unpertubed/image_{entry[1]}.png")
        unpertubed_image = unpertubed_image.resize((int(display_width/3) -30,int(entry_height * 4/5)-30))
        unpertubed_image = ImageTk.PhotoImage(unpertubed_image)
        unpertubed_label = tk.Label(image_container,image = unpertubed_image)
        unpertubed_label.image = unpertubed_image

        pertubation_image = Image.open( f"./results/trial_{entry[0]}/pertubation/image_{entry[1]}.png")
        pertubation_image = pertubation_image.resize((int(display_width/3) -30,int(entry_height * 4/5)-30))
        pertubation_image = ImageTk.PhotoImage(pertubation_image)
        pertubation_label = tk.Label(image_container,image = pertubation_image)
        pertubation_label.image = pertubation_image

        pertubed_image = Image.open( f"./results/trial_{entry[0]}/pertubed/image_{entry[1]}.png")
        pertubed_image = pertubed_image.resize((int(display_width/3)-30,int(entry_height * 4/5)-30))
        pertubed_image = ImageTk.PhotoImage(pertubed_image)
        pertubed_label = tk.Label(image_container,image = pertubed_image)
        pertubed_label.image = pertubed_image

        listing.pack(side='left')
        listing_container.pack(side='top',fill='x', expand=(True))
           
        unpertubed_label.pack(side = 'left',padx=(10,0),pady=(22.5,22.5))
        pertubation_label.pack(side = 'left',padx=(5,5),pady=(22.5,22.5))
        pertubed_label.pack(side = 'left',padx=(0,10),pady=(22.5,22.5))
        image_container.pack(side = 'top')
        container_container.pack(side='top',expand=True,fill='x',pady=(0,30),padx=(22.5,22.5))


    def calculate_new_entries(root,display_width,entry_height,dictionary, variable, display_height,page_number):
        while not dictionary.empty():
            current_trial = dictionary.get()
            file_count = 0
            for entry in os.listdir( f"./results/trial_{current_trial}/pertubed"):
                # Check if the entry is a file
                if os.path.isfile(os.path.join(f"./results/trial_{current_trial}/pertubed", entry)):
                    file_count += 1

            for counter in range(0,file_count):
                variable[2].append([current_trial,counter])
            
            load_current_page_of_entries(root,display_width,entry_height,dictionary, variable,display_height,page_number[0])
        root.after(500, lambda: calculate_new_entries(root,display_width,entry_height,dictionary, variable,display_height,page_number))



    def lazy_load_entries(root,display_width,entry_height,dictionary, variable, display_height):

        current_widget_height = (variable[0].bbox("all")[1]) -137
        top_padding = 0
        bottom_padding = 0
        entries_to_be_rendered = []


        canvas_width = variable[0].winfo_width() 
        canvas_height = variable[0].winfo_height() 
        x_scroll = variable[0].canvasx(0) 
        y_scroll = variable[0].canvasy(0) # Calculate the visible region 
        visible_region = [x_scroll, y_scroll -500, x_scroll + canvas_width, y_scroll + canvas_height + 500]


        counter = 0

        for widget in variable[2]:
            counter += 1


            if (current_widget_height + entry_height) < visible_region[1]:
                top_padding += entry_height + 30
                current_widget_height += entry_height + 30
            elif current_widget_height > visible_region[3]:
                bottom_padding += entry_height + 30
                current_widget_height += entry_height + 30
            else:
                entries_to_be_rendered.append(widget)
                current_widget_height += entry_height + 30

        for widget in root.winfo_children():
            if not(widget.winfo_name() == 'exception_frame'):
                widget.destroy()
        

        top_frame = tk.Frame(root,name='top_frame',bg='green')
        top_frame.pack(side='top', pady=(top_padding,0))



        for entry in entries_to_be_rendered:
            construct_entry(root,display_width,entry_height,dictionary, entry, display_height)


        bottom_frame = tk.Frame(root,name='bottom_frame',bg='blue')
        bottom_frame.pack(side='top', pady=(0,bottom_padding))

        root.update()
        


    def increase_page_number(root,display_width,entry_height,dictionary, variable,display_height,page_number):
        if ((page_number[0]+1)*150) <= len(variable[2]):
            page_number[0] += 1
            load_current_page_of_entries(root,display_width,entry_height,dictionary, variable,display_height,page_number[0])


    def decrease_page_number(root,display_width,entry_height,dictionary, variable,display_height,page_number):
        if page_number[0] > 0:
            page_number[0] += -1
            load_current_page_of_entries(root,display_width,entry_height,dictionary, variable,display_height,page_number[0])
            
    page_number = [0]


    frame = tk.Frame(root,name='page_button_container')
    frame.pack(side='bottom')

    left_button = tk.Button(frame, text="<<",command = lambda: decrease_page_number(root,display_width,entry_height,dictionary, variable,display_height,page_number))
    left_button.pack(side='left')

    right_button = tk.Button(frame, text=">>",command = lambda: increase_page_number(root,display_width,entry_height,dictionary, variable,display_height,page_number))
    right_button.pack(side='left')


    #variable[1].bind("<ButtonRelease-1>", lambda event: lazy_load_entries(root,display_width,entry_height,dictionary, variable,display_height))
    root.after(500, lambda: calculate_new_entries(root,display_width,entry_height,dictionary, variable,display_height,page_number))