import tkinter as tk
from PIL import Image
import numpy as np

def denormalize_and_save_image(image,ident,type):
    display_2 = Image.fromarray(((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8))
    display_2.save(f'./images/{type}/image_{ident}.png')

from tkinter import ttk
def front_end_main():
    root = tk.Tk()

    tk.Label(root, text='Classic Label').pack()
    ttk.Label(root, text='Themed Label').pack()
    root.mainloop()
