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
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sys.path.insert(0, './src')

from GUI.objects.scroll_list.scroll_list_entries.graph_display_scroll_list_entries import graph_display_scroll_list_entries


class graph_display_scroll_list_entry_test(unittest.TestCase):


    def test_graphs_are_created_on_initial_step(self):
        root = tk.Tk()
        container = tk.Frame(root)
        display_width = 200
        entry_height = 100
        dictionary = queue.Queue()
        variable = 5
        display_height = 500

        if os.path.exists('./results'):
            shutil.rmtree('./results')
        os.makedirs('./results', exist_ok=True)
        with open(f'./results/cumulative_metrics.txt', "w") as file:
            file.write(str({'accuracy': 0, 'mean_pertubation': 0, 'GMQ': 0, 'Sharpe_ratio':0}))


        fig = plt.figure()
        dpi = fig.get_dpi()
        fig, ax = plt.subplots(figsize=((display_width/dpi), (entry_height/dpi)))
        ax.plot(0,1,2)
        ax.set_xlim(0, variable)  # Set x-axis limits
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig)
        canvas.draw()
        buf = canvas.buffer_rgba()
        np_array = np.asarray(buf)
        plt.imshow(np_array)
        plt.show()
        print(np_array)


        dictionary.put(0)

        graph_display_scroll_list_entries(root,display_width,entry_height, dictionary, variable, display_height)

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

        time.sleep(5)

        if os.path.exists('./results'):
            shutil.rmtree('./results')

        root.destroy()




        
                
                        

def suite():
    suite = unittest.TestSuite()
    suite.addTest(graph_display_scroll_list_entry_test('test_graphs_are_created_on_initial_step'))
    return suite










        


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())