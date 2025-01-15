import unittest
import tkinter as tk
import sys
import queue
import time
import os
import shutil
from PIL import Image, ImageTk
import numpy as np
import numpy.testing as npt

sys.path.insert(0, './src')

from GUI.objects.scroll_list.scroll_list_entries.image_display_scroll_list_entries import update_image_display_entries


class multi_input_scroll_list_entries_test(unittest.TestCase):


    def test_images_are_appended_on_initial_step(self):
        root = tk.Tk()
        container = tk.Frame(root)
        display_width = 200
        entry_height = 100
        dictionary = queue.Queue()
        variable = [None]
        display_height = 500

        if os.path.exists('./results'):
            shutil.rmtree('./results')
        os.makedirs(f'./results/trial_0/unpertubed', exist_ok=True)
        os.makedirs(f'./results/trial_0/pertubation', exist_ok=True)
        os.makedirs(f'./results/trial_0/pertubed', exist_ok=True)

        image = np.random.uniform(-50,50,(224,224,3))


        image = Image.fromarray(((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8))
        image.save(f'./results/trial_0/unpertubed/image_0.png')
        image.save(f'./results/trial_0/pertubation/image_0.png')
        image.save(f'./results/trial_0/pertubed/image_0.png')

        image = Image.open( f"./results/trial_0/unpertubed/image_0.png")
        image = image.resize((int(display_width/3) -30,int(entry_height * 4/5)-30))
        image = ImageTk.PhotoImage(image)
        label = tk.Label(root,image = image)
        label.image = image
        image = np.array((ImageTk.getimage(label.image)).getdata())

        dictionary.put(0)

        update_image_display_entries(container,display_width,entry_height,dictionary, variable,display_height)

        container.pack(side='top',pady=(10,0))

        time.sleep(2)

        root.update_idletasks()
        root.update()

        returned_images = []


        for widget in container.winfo_children():
            if isinstance(widget, tk.Frame):
                for widget1 in widget.winfo_children():
                    if isinstance(widget, tk.Frame):
                        for widget2 in widget1.winfo_children():
                            if isinstance(widget2,tk.Label):
                                try:
                                    returned_images.append(np.array((ImageTk.getimage(widget2.image)).getdata()))

                                except:
                                    Nothing = None


        if os.path.exists('./results'):
            shutil.rmtree('./results')

        root.destroy()

        npt.assert_array_equal(returned_images,[image,image,image])

    
    def test_images_are_appended_after_changes(self):
        root = tk.Tk()
        container = tk.Frame(root)
        display_width = 200
        entry_height = 100
        dictionary = queue.Queue()
        variable = [None]
        display_height = 500

        if os.path.exists('./results'):
            shutil.rmtree('./results')
        os.makedirs(f'./results/trial_0', exist_ok=True)
        os.makedirs(f'./results/trial_0/unpertubed', exist_ok=True)
        os.makedirs(f'./results/trial_0/pertubation', exist_ok=True)
        os.makedirs(f'./results/trial_0/pertubed', exist_ok=True)

        image = np.random.uniform(-50,50,(224,224,3))

        image = Image.fromarray(((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8))
        image.save(f'./results/trial_0/unpertubed/image_0.png')
        image.save(f'./results/trial_0/pertubation/image_0.png')
        image.save(f'./results/trial_0/pertubed/image_0.png')


        dictionary.put(0)

        update_image_display_entries(container,display_width,entry_height,dictionary, variable,display_height)

        container.pack(side='top',pady=(10,0))

        time.sleep(2)

        root.update_idletasks()
        root.update()

        os.makedirs(f'./results/trial_1', exist_ok=True)
        os.makedirs(f'./results/trial_1/unpertubed', exist_ok=True)
        os.makedirs(f'./results/trial_1/pertubation', exist_ok=True)
        os.makedirs(f'./results/trial_1/pertubed', exist_ok=True)

        image.save(f'./results/trial_1/unpertubed/image_0.png')
        image.save(f'./results/trial_1/pertubation/image_0.png')
        image.save(f'./results/trial_1/pertubed/image_0.png')

        dictionary.put(1)

        root.update_idletasks()
        root.update()

        time.sleep(2)

        root.update_idletasks()
        root.update()


        image = Image.open( f"./results/trial_1/unpertubed/image_0.png")
        image = image.resize((int(display_width/3) -30,int(entry_height * 4/5)-30))
        image = ImageTk.PhotoImage(image)
        label = tk.Label(root,image = image)
        label.image = image
        image = np.array((ImageTk.getimage(label.image)).getdata())

        fail_flag = False

        returned_images = []

        for widget in container.winfo_children():
            if isinstance(widget, tk.Frame):
                for widget1 in widget.winfo_children():
                    if isinstance(widget, tk.Frame):
                        for widget2 in widget1.winfo_children():
                            if isinstance(widget2,tk.Label):
                                try:
                                    returned_images.append(np.array((ImageTk.getimage(widget2.image)).getdata()))

                                except:
                                    nothing = None

        if os.path.exists('./results'):
            shutil.rmtree('./results')

        root.destroy()

        npt.assert_array_equal(returned_images,[image,image,image,image,image,image])

        
                
                        

def suite():
    suite = unittest.TestSuite()
    suite.addTest(multi_input_scroll_list_entries_test('test_images_are_appended_on_initial_step'))
    suite.addTest(multi_input_scroll_list_entries_test('test_images_are_appended_after_changes'))
    return suite










        


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())