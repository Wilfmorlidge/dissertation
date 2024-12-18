import os
import tkinter as tk
from PIL import Image, ImageTk

def update_image_display_entries(root,display_width,entry_height,dictionary, variable, display_height):
    while not dictionary.empty():
        current_trial = dictionary.get()
        file_count = 0
        for entry in os.listdir( f"./results/trial_{current_trial}/pertubed"):
            # Check if the entry is a file
            if os.path.isfile(os.path.join(f"./results/trial_{current_trial}/pertubed", entry)):
                file_count += 1

        for counter in range(0,file_count):
            container_container = tk.Frame(root)


            listing_container = tk.Frame(container_container, height = int(entry_height * 1/5))
            listing = tk.Label(listing_container,text=f"{current_trial}:{counter}")

            image_container = tk.Frame(container_container, height = int(entry_height * 4/5))

            unpertubed_image = Image.open( f"./results/trial_{current_trial}/unpertubed/image_{counter}.png")
            unpertubed_image = unpertubed_image.resize((int(display_width/3),int(entry_height * 4/5)))
            unpertubed_image = ImageTk.PhotoImage(unpertubed_image)
            unpertubed_label = tk.Label(image_container,image = unpertubed_image)
            unpertubed_label.image = unpertubed_image

            pertubation_image = Image.open( f"./results/trial_{current_trial}/pertubation/image_{counter}.png")
            pertubation_image = pertubation_image.resize((int(display_width/3),int(entry_height * 4/5)))
            pertubation_image = ImageTk.PhotoImage(pertubation_image)
            pertubation_label = tk.Label(image_container,image = pertubation_image)
            pertubation_label.image = pertubation_image

            pertubed_image = Image.open( f"./results/trial_{current_trial}/pertubed/image_{counter}.png")
            pertubed_image = pertubed_image.resize((int(display_width/3),int(entry_height * 4/5)))
            pertubed_image = ImageTk.PhotoImage(pertubed_image)
            pertubed_label = tk.Label(image_container,image = pertubed_image)
            pertubed_label.image = pertubed_image

            listing.pack(side='left')
            listing_container.pack(side='top',fill='x', expand=(True))
           
            unpertubed_label.pack(side = 'left')
            pertubation_label.pack(side = 'left')
            pertubed_label.pack(side = 'left')
            image_container.pack(side = 'top',fill='x', expand=(True))

            container_container.pack(side='top',fill='x', expand=(True))

        total_height = 0
        extension_frame = None
        for widget in root.winfo_children():
            if widget.winfo_name() == 'exception_frame':
                extension_frame = widget
            else:
                total_height += widget.winfo_height()
            widget.update_idletasks()  # Ensure the widget's geometry is updated
        if extension_frame != None:
            extension_frame.pack_forget()  # Remove the widget from its current packing
            extension_frame.pack(side='bottom', fill='x',pady=(0,(max((display_height-total_height),0))))  # Re-pack it at the bottom
    
    root.after(500, lambda: update_image_display_entries(root,display_width,entry_height,dictionary, variable,display_height))
1