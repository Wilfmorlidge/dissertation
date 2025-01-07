import unittest
import tkinter as tk
import sys
import time 
import queue
sys.path.insert(0, './src')

from GUI.objects.scroll_list.scroll_list import scroll_list
from GUI.objects.window.window import window
from GUI.pages.landing_page import landing_page

class scroll_list_tests(unittest.TestCase):
    # test that passing a different model name to the function causes the corresponding model to be returned
    def test_scrolling_an_empty_list(self):

        def entry_function(list_frame,display_width,entry_height, dictionary, variable,display_height):
            return True

        root = tk.Tk()
        container = tk.Frame(root)
        dcitionary = {}
        variable = []
        entry_function = entry_function
        test_widget = scroll_list(container,display_width=200,display_height=400,entry_height=2, dictionary = dcitionary, variable = variable, entry_function = entry_function)
        container.pack(side='top',pady=(10,0))

        root.update_idletasks()
        root.update()

        current_scroll_region_corner= (0,0)
        for widget in test_widget.winfo_children():
            if isinstance(widget, tk.Canvas):
                current_scroll_region_corner=(widget.canvasx(0),widget.canvasy(0))
        
        for widget in test_widget.winfo_children():
            if isinstance(widget, tk.Scrollbar):
                    # Simulate clicking on the scrollbar
                    widget.event_generate("<ButtonPress-1>", x=10, y=10)
    
                    # Simulate dragging the scrollbar down
                    for _ in range(10):
                        widget.event_generate("<B1-Motion>", x=10, y=20)
                        widget.update_idletasks()
    
                    # Simulate releasing the scrollbar
                    widget.event_generate("<ButtonRelease-1>", x=10, y=20)

                    root.update_idletasks()
                    root.update()

        new_scroll_region_corner = (0,0)
        for widget in test_widget.winfo_children():
            if isinstance(widget, tk.Canvas):
                new_scroll_region_corner=(widget.canvasx(0),widget.canvasy(0))

        root.update_idletasks()
        root.update()

        self.assertEqual(current_scroll_region_corner,new_scroll_region_corner)

    def test_exception_frame_adds_correct_padding(self):
        def entry_function(list_frame,display_width,entry_height, dictionary, variable,display_height):
            for counter in range (0,10):
                Button = tk.Button(list_frame,text=f'fake_data_{counter}')
                Button.pack(side = 'top',fill='x', expand=(True),pady=(0,5))

        root = tk.Tk()
        container = tk.Frame(root)
        dcitionary = {}
        variable = []
        entry_function = entry_function
        test_widget = scroll_list(container,display_width=200,display_height=400,entry_height=2, dictionary = dcitionary, variable = variable, entry_function = entry_function)
        container.pack(side='top',pady=(10,0))


        root.update_idletasks()
        root.update()

        time.sleep(2)

        root.update_idletasks()
        root.update()

        pady = 0
        for widget1 in test_widget.winfo_children():
            if isinstance(widget1, tk.Canvas):
                for widget2 in widget1.winfo_children():
                    if isinstance(widget2,tk.Frame):
                        for widget3 in widget2.winfo_children():
                            if widget3.winfo_name() == 'exception_frame':
                                pady = widget3.pack_info().get('pady', 0)
        self.assertEqual(pady,(0,94))


    def test_exception_frame_updates_correctly(self):
        def entry_function(list_frame,display_width,entry_height, dictionary, variable,display_height):

            flag = 0
            while not dictionary.empty():
                dictionary.get()
                Button = tk.Button(list_frame,text=f'fake_data')
                Button.pack(side = 'top',fill='x', expand=(True),pady=(0,5))
            list_frame.after(100,lambda: entry_function(list_frame,display_width,entry_height, dictionary, variable,display_height))

        root = tk.Tk()
        container = tk.Frame(root)
        dcitionary = queue.Queue()
        for i in range(10):
            dcitionary.put(i)
        variable = [0,10]
        entry_function = entry_function
        test_widget = scroll_list(container,display_width=200,display_height=400,entry_height=2, dictionary = dcitionary, variable = variable, entry_function = entry_function)
        container.pack(side='top',pady=(10,0))


        root.update_idletasks()
        root.update()

        time.sleep(2)

        root.update_idletasks()
        root.update()

        pady = 0
        exception_frame = None
        for widget1 in test_widget.winfo_children():
            if isinstance(widget1, tk.Canvas):
                for widget2 in widget1.winfo_children():
                    if isinstance(widget2,tk.Frame):
                        for widget3 in widget2.winfo_children():
                            if widget3.winfo_name() == 'exception_frame':
                                pady = widget3.pack_info().get('pady', 0)
                                exception_frame = widget3
        self.assertEqual(pady,(0,94))

        dcitionary.put(11)
        dcitionary.put(12)


        root.update_idletasks()
        root.update()

        time.sleep(2)

        root.update_idletasks()
        root.update()

        pady = exception_frame.pack_info().get('pady', 0)
        self.assertEqual(pady,(0,82))


    def test_scrolling_a_more_than_full_list(self):
            # test that passing a different model name to the function causes the corresponding model to be returned
        def entry_function(list_frame,display_width,entry_height, dictionary, variable,display_height):
            for counter in range (0,50):
                Button = tk.Button(list_frame,text=f'fake_data_{counter}')
                Button.pack(side = 'top',fill='x', expand=(True),pady=(0,5))

        root = tk.Tk()
        container = tk.Frame(root)
        dcitionary = {}
        variable = []
        entry_function = entry_function
        test_widget = scroll_list(container,display_width=200,display_height=400,entry_height=2, dictionary = dcitionary, variable = variable, entry_function = entry_function)
        container.pack(side='top',pady=(10,0))

        root.update_idletasks()
        root.update()

        current_scroll_region_corner= (0,0)
        for widget in test_widget.winfo_children():
            if isinstance(widget, tk.Canvas):
                current_scroll_region_corner=(widget.canvasx(0),widget.canvasy(0))
        
        for widget in test_widget.winfo_children():
            if isinstance(widget, tk.Scrollbar):
                    # Simulate clicking on the scrollbar
                    widget.event_generate("<ButtonPress-1>", x=10, y=10)
    
                    # Simulate dragging the scrollbar down
                    for _ in range(10):
                        widget.event_generate("<B1-Motion>", x=10, y=20)
                        widget.update_idletasks()
    
                    # Simulate releasing the scrollbar
                    widget.event_generate("<ButtonRelease-1>", x=10, y=20)

                    root.update_idletasks()
                    root.update()

        new_scroll_region_corner = (0,0)
        for widget in test_widget.winfo_children():
            if isinstance(widget, tk.Canvas):
                new_scroll_region_corner=(widget.canvasx(0),widget.canvasy(0))

        root.update_idletasks()
        root.update()

        self.assertNotEqual(current_scroll_region_corner,new_scroll_region_corner)







        


if __name__ == '__main__':
    unittest.main()