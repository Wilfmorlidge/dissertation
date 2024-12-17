import os
import tkinter as tk
from PIL import Image, ImageTk

def update_image_display_entries(root,display_width,entry_height,dictionary, variable, display_height):
    print('------------------------------------------------your god will judge you harshly-----------------------')
    print('------------------------------------------------------------------------------------------------------')
    while not dictionary.empty():
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++your existence is an exercise in futility+++++++++++++')
        result = dictionary.get()
        file_count = 0
        for entry in os.listdir( f"./images/trial_{result['trial_number']}/pertubed"):
            # Check if the entry is a file
            if os.path.isfile(os.path.join(f"./images/trial_{result['trial_number']}/pertubed", entry)):
                file_count += 1

        total_height = 0
        extension_frame = None
        for widget in root.winfo_children():
            print('why in the fuck')
            if widget.winfo_name() == 'exception_frame':
                print('bruh')
                extension_frame = widget
            else:
                total_height += widget.winfo_height()
            widget.update_idletasks()  # Ensure the widget's geometry is updated
            print('this is the current weight' + str(total_height))
            if extension_frame != None:
                extension_frame.pack_forget()  # Remove the widget from its current packing
                extension_frame.pack(side='bottom', fill='x',pady=(0,(max((display_height-total_height),0))))  # Re-pack it at the bottom


        for counter in range(0,file_count):
            image_container = tk.Frame(root)
            unpertubed_image = Image.open( f"./images/trial_{result['trial_number']}/unpertubed/image_{counter}.png")
            unpertubed_image = unpertubed_image.resize((int(display_width/3),entry_height))
            unpertubed_image = ImageTk.PhotoImage(unpertubed_image)
            unpertubed_label = tk.Label(image_container,image = unpertubed_image)
            unpertubed_label.image = unpertubed_image

            pertubation_image = Image.open( f"./images/trial_{result['trial_number']}/pertubation/image_{counter}.png")
            pertubation_image = pertubation_image.resize((int(display_width/3),entry_height))
            pertubation_image = ImageTk.PhotoImage(pertubation_image)
            pertubation_label = tk.Label(image_container,image = pertubation_image)
            pertubation_label.image = pertubation_image

            pertubed_image = Image.open( f"./images/trial_{result['trial_number']}/pertubed/image_{counter}.png")
            pertubed_image = pertubed_image.resize((int(display_width/3),entry_height))
            pertubed_image = ImageTk.PhotoImage(pertubed_image)
            pertubed_label = tk.Label(image_container,image = pertubed_image)
            pertubed_label.image = pertubed_image

            unpertubed_label.pack(side = 'left')
            pertubation_label.pack(side = 'left')
            pertubed_label.pack(side = 'left')
            image_container.pack(side = 'top',fill='x', expand=(True))
    
    root.after(500, lambda: update_image_display_entries(root,display_width,entry_height,dictionary, variable,display_height))
1