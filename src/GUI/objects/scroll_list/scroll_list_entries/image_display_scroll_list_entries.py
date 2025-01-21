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


    print(root.winfo_children())
    for widget in root.winfo_children():
        canvas_width = variable.winfo_width() 
        canvas_height = variable.winfo_height() 
        x_scroll = variable.canvasx(0) 
        y_scroll = variable.canvasy(0) # Calculate the visible region 
        visible_region = (x_scroll, y_scroll, x_scroll + canvas_width, y_scroll + canvas_height)


        x = widget.winfo_x() 
        y = widget.winfo_y() 
        width = widget.winfo_width()
        height = widget.winfo_height()
        widget_bbox = (x, y, x + width, y + height)

        print(widget_bbox)
        print(visible_region)

        #    widget_height = widget.winfo_height() + widget.pack_info().get('pady', 0)
        #    if (widget_bbox[2] > canvas_bbox[0] and widget_bbox[0] < canvas_bbox[2] and widget_bbox[3] > canvas_bbox[1] and widget_bbox[1] < canvas_bbox[3]):
        #        root.pack_configure(pady = root.pack_info().get('pady', 0) - widget_height)
        #        try:
        #            widget.pack(side='top',expand=True,fill='x',pady=(0,30),padx=(22.5,22.5))
        #        except:
        #            nothing = None
        #    else:
        #        root.pack_configure(pady = root.pack_info().get('pady', 0) + widget_height)
        #        try:
        #            widget.pack_forget()
        #        except:
        #            nothing = None

        
    root.after(500, lambda: update_image_display_entries(root,display_width,entry_height,dictionary, variable,display_height))