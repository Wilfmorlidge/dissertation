import os
import tkinter as tk
from PIL import Image, ImageTk
import time

def update_image_display_entries(root,display_width,entry_height,dictionary, variable, display_height):


    def create_new_entries(root,display_width,entry_height,dictionary, variable, display_height):
        while not dictionary.empty():
            current_trial = dictionary.get()
            file_count = 0
            for entry in os.listdir( f"./results/trial_{current_trial}/pertubed"):
                # Check if the entry is a file
                if os.path.isfile(os.path.join(f"./results/trial_{current_trial}/pertubed", entry)):
                    file_count += 1

            for counter in range(0,file_count):
                container_container = tk.Frame(root,bg='dimgray')


                listing_container = tk.Frame(container_container, height = int(entry_height * 1/5))
                listing = tk.Label(listing_container,text=f"{current_trial}:{counter}")

                image_container = tk.Frame(container_container, height = int(entry_height * 4/5))

                unpertubed_image = Image.open( f"./results/trial_{current_trial}/unpertubed/image_{counter}.png")
                unpertubed_image = unpertubed_image.resize((int(display_width/3) -30,int(entry_height * 4/5)-30))
                unpertubed_image = ImageTk.PhotoImage(unpertubed_image)
                unpertubed_label = tk.Label(image_container,image = unpertubed_image)
                unpertubed_label.image = unpertubed_image

                pertubation_image = Image.open( f"./results/trial_{current_trial}/pertubation/image_{counter}.png")
                pertubation_image = pertubation_image.resize((int(display_width/3) -30,int(entry_height * 4/5)-30))
                pertubation_image = ImageTk.PhotoImage(pertubation_image)
                pertubation_label = tk.Label(image_container,image = pertubation_image)
                pertubation_label.image = pertubation_image

                pertubed_image = Image.open( f"./results/trial_{current_trial}/pertubed/image_{counter}.png")
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
                variable[2].append(container_container)
        root.after(500, lambda: create_new_entries(root,display_width,entry_height,dictionary, variable,display_height))



    def lazy_load_entries(root,display_width,entry_height,dictionary, variable, display_height,top_frame,bottom_frame):

        current_widget_height = (variable[0].bbox("all")[1]) -137
        top_padding = 0
        bottom_padding = 0
        entries_to_be_rendered = []

        canvas_width = variable[0].winfo_width() 
        canvas_height = variable[0].winfo_height() 
        x_scroll = variable[0].canvasx(0) 
        y_scroll = variable[0].canvasy(0) # Calculate the visible region 
        visible_region = [x_scroll, y_scroll -150, x_scroll + canvas_width, y_scroll + canvas_height + 150]

        print(visible_region)
        print('top of canvas height' + str(current_widget_height))

        for widget in variable[2]:
            print(variable[2])
            print('beginning run')
            if not(widget.winfo_name() == 'exception_frame') and not(widget.winfo_name() == 'top_frame') and not(widget.winfo_name() == 'bottom_frame'):
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
            try:
                widget.pack_forget()
            except:
                nothing = None
        
        top_frame.pack(side='top', pady=(top_padding,0))

        for widget in entries_to_be_rendered:
            widget.pack(side='top',expand=True,fill='x',pady=(0,30),padx=(22.5,22.5))

        bottom_frame.pack(side='top', pady=(0,bottom_padding))

        root.update()
        

            


    top_frame = tk.Frame(root,name='top_frame',bg='green')
    bottom_frame = tk.Frame(root,name='bottom_frame',bg='blue')

    variable[1].bind("<ButtonRelease-1>", lambda event: lazy_load_entries(root,display_width,entry_height,dictionary, variable,display_height,top_frame,bottom_frame))
    root.after(500, lambda: create_new_entries(root,display_width,entry_height,dictionary, variable,display_height))