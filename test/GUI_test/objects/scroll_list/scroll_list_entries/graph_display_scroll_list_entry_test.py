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
            file.write('\n' + str({'accuracy': 0.6, 'mean_pertubation': 42, 'GMQ': 3, 'Sharpe_ratio':1.4}))
            file.write('\n' + str({'accuracy': 0.4, 'mean_pertubation': 38, 'GMQ': 12, 'Sharpe_ratio':1.8}))

        dictionary.put(0)

        graph_display_scroll_list_entries(container,display_width,entry_height, dictionary, variable, display_height)

        container.pack(side='top',pady=(10,0))

        time.sleep(5)

        root.update_idletasks()
        root.update()

        returned_arrays = []


        for widget in container.winfo_children():
            if isinstance(widget, tk.Frame):
                for widget1 in widget.winfo_children():
                    if isinstance(widget1, tk.Label):
                        returned_arrays.append(widget1.metadata['y_data'])

        if os.path.exists('./results'):
            shutil.rmtree('./results')

        root.destroy()

        npt.assert_array_equal(returned_arrays,[[0.,0.6,0.4],[0,42,38],[0,3,12],[0.,1.4,1.8]])


    def test_graphs_are_updated_correctly(self):
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
            file.write('\n' + str({'accuracy': 0.6, 'mean_pertubation': 42, 'GMQ': 3, 'Sharpe_ratio':1.4}))
            file.write('\n' + str({'accuracy': 0.4, 'mean_pertubation': 38, 'GMQ': 12, 'Sharpe_ratio':1.8}))

        dictionary.put(0)

        graph_display_scroll_list_entries(container,display_width,entry_height, dictionary, variable, display_height)

        container.pack(side='top',pady=(10,0))

        time.sleep(2)

        root.update_idletasks()
        root.update()

        returned_arrays = []


        for widget in container.winfo_children():
            if isinstance(widget, tk.Frame):
                for widget1 in widget.winfo_children():
                    if isinstance(widget1, tk.Label):
                        returned_arrays.append(widget1.metadata['y_data'])


        npt.assert_array_equal(returned_arrays,[[0.,0.6,0.4],[0,42,38],[0,3,12],[0.,1.4,1.8]])

        with open(f'./results/cumulative_metrics.txt', "a") as file:
            file.write('\n' + str({'accuracy': 0.2, 'mean_pertubation': 73, 'GMQ': 9, 'Sharpe_ratio':1.33333}))

        dictionary.put(1)

        time.sleep(2)

        root.update_idletasks()
        root.update()

        returned_arrays = []

        time.sleep(2)


        for widget in container.winfo_children():
            if isinstance(widget, tk.Frame):
                for widget1 in widget.winfo_children():
                    if isinstance(widget1, tk.Label):
                        returned_arrays.append(widget1.metadata['y_data'])

        if os.path.exists('./results'):
            shutil.rmtree('./results')

        root.destroy()

        npt.assert_array_equal(returned_arrays,[[0.,0.6,0.4,0.2],[0,42,38,73],[0,3,12,9],[0.,1.4,1.8,1.33333]])





        
                
                        

def suite():
    suite = unittest.TestSuite()
    suite.addTest(graph_display_scroll_list_entry_test('test_graphs_are_created_on_initial_step'))
    suite.addTest(graph_display_scroll_list_entry_test('test_graphs_are_updated_correctly'))
    return suite










        


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())