import os
import tkinter as tk
from PIL import Image, ImageTk

def update_image_display_entries(root,display_width,entry_height,dictionary, variable, display_height):
    print('this is stupid')
    while not dictionary.empty():
        current_trial = dictionary.get()
        print('this is the current dictionary' + str(current_trial))
        file_count = 0
        for entry in os.listdir( f"./results/trial_{current_trial}/pertubed"):
            # Check if the entry is a file
            if os.path.isfile(os.path.join(f"./results/trial_{current_trial}/pertubed", entry)):
                file_count += 1

        for counter in range(0,file_count):
            container_container = tk.Frame(root,bg='dimgray',name='container_container')


            listing_container = tk.Frame(container_container, height = int(entry_height * 1/5),name='listing_container')
            listing = tk.Label(listing_container,text=f"{current_trial}:{counter}")

            print('all is death plague and rot')

            image_container = tk.Frame(container_container, height = int(entry_height * 4/5),name='image_container')

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
    
    root.after(500, lambda: update_image_display_entries(root,display_width,entry_height,dictionary, variable,display_height))