import os
import tkinter as tk
from PIL import Image, ImageTk
import time

def update_image_display_entries(root,display_width,entry_height,dictionary, variable, display_height):


    def construct_entries(root,display_width,entry_height,dictionary, entry, display_height):
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


    def calculate_new_entries(root,display_width,entry_height,dictionary, variable, display_height):
        while not dictionary.empty():
            current_trial = dictionary.get()
            file_count = 0
            for entry in os.listdir( f"./results/trial_{current_trial}/pertubed"):
                # Check if the entry is a file
                if os.path.isfile(os.path.join(f"./results/trial_{current_trial}/pertubed", entry)):
                    file_count += 1

            for counter in range(0,file_count):
                variable[2].append([current_trial,counter])
            

            lazy_load_entries(root,display_width,entry_height,dictionary, variable,display_height)
        root.after(500, lambda: calculate_new_entries(root,display_width,entry_height,dictionary, variable,display_height))



    def lazy_load_entries(root,display_width,entry_height,dictionary, variable, display_height):

        current_widget_height = (variable[0].bbox("all")[1]) -137
        top_padding = 0
        bottom_padding = 0
        entries_to_be_rendered = []

        print(str(len(variable[2])))

        canvas_width = variable[0].winfo_width() 
        canvas_height = variable[0].winfo_height() 
        x_scroll = variable[0].canvasx(0) 
        y_scroll = variable[0].canvasy(0) # Calculate the visible region 
        visible_region = [x_scroll, y_scroll -500, x_scroll + canvas_width, y_scroll + canvas_height + 500]

        print(visible_region)
        print('top of canvas height' + str(current_widget_height))

        counter = 0

        for widget in variable[2]:
            counter += 1
            print(counter)
            print('accessing element')

            if (current_widget_height + entry_height) < visible_region[1]:
                print('this element is too high')
                top_padding += entry_height + 30
                current_widget_height += entry_height + 30
            elif current_widget_height > visible_region[3]:
                print('this element is too low')
                bottom_padding += entry_height + 30
                current_widget_height += entry_height + 30
            else:
                entries_to_be_rendered.append(widget)
                current_widget_height += entry_height + 30

        for widget in root.winfo_children():
            if not(widget.winfo_name() == 'exception_frame'):
                widget.destroy()
        
        print(root.winfo_children())

        top_frame = tk.Frame(root,name='top_frame',bg='green')
        top_frame.pack(side='top', pady=(top_padding,0))

        for entry in entries_to_be_rendered:
            construct_entries(root,display_width,entry_height,dictionary, entry, display_height)


        bottom_frame = tk.Frame(root,name='bottom_frame',bg='blue')
        bottom_frame.pack(side='top', pady=(0,bottom_padding))

        root.update()
        

            




    variable[1].bind("<ButtonRelease-1>", lambda event: lazy_load_entries(root,display_width,entry_height,dictionary, variable,display_height))
    root.after(500, lambda: calculate_new_entries(root,display_width,entry_height,dictionary, variable,display_height))