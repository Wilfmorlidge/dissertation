import unittest
import tkinter as tk
import sys



sys.path.insert(0, './src')

from GUI.objects.scroll_list.scroll_list_entries.multi_input_scroll_list_entries import multi_input_scroll_list_entries


class multi_input_scroll_list_entries_test(unittest.TestCase):

    def test_buttons_are_created_for_all_entries_in_the_dictionary(self):
        root = tk.Tk()
        container = tk.Frame(root)
        display_width = 200
        entry_height = 100
        dictionary = {'fake_data_1':1,'fake_data_2':2,'fake_data_3':3,'fake_data_4':4}
        variable = [None]
        display_height = 500
        multi_input_scroll_list_entries(container,display_width,entry_height,dictionary, variable,display_height)

        container.pack(side='top',pady=(10,0))

        root.update_idletasks()
        root.update()

        expected_button_titles =['fake_data_1','fake_data_2','fake_data_3','fake_data_4']

        fail_flag = 0

        for widget in container.winfo_children():
            if isinstance(widget, tk.Frame):
                matching_title = -1
                instances_of_sub_widgets = [0,0]
                for widget1 in widget.winfo_children():
                    if isinstance(widget1, tk.Label):
                        instances_of_sub_widgets[0] = instances_of_sub_widgets[0] + 1
                        remove = False
                        for entry in expected_button_titles:
                            if entry == widget1.cget("text"):
                                remove = True
                        if remove == True:
                            expected_button_titles.remove(widget1.cget("text"))
                    if isinstance(widget1, tk.Text):
                        instances_of_sub_widgets[1] = instances_of_sub_widgets[1] + 1
                if instances_of_sub_widgets != [1,1]:
                    fail_flag = 1

        self.assertEqual(expected_button_titles,[])
        self.assertEqual(fail_flag, 0)

                        
    def test_typeing_in_a_field_updates_its_value(self):
        root = tk.Tk()
        container = tk.Frame(root)
        display_width = 200
        entry_height = 100
        dictionary = {'fake_data_1':1}
        variable = []
        display_height = 500
        multi_input_scroll_list_entries(container,display_width,entry_height,dictionary, variable,display_height)

        container.pack(side='top',pady=(10,0))

        root.update_idletasks()
        root.update()

        for widget in container.winfo_children():
            if (isinstance(widget, tk.Frame)):
                for widget1 in widget.winfo_children():
                    if (isinstance(widget1,tk.Text)):
                        for char in "0.11,8.999,8.81,9.99,1.19,7.25,3":
                            widget1.insert(tk.END, char)
                            widget1.event_generate("<<TextModified>>", when="tail")

        root.update_idletasks()
        root.update()

        value = variable[0].get(0.0,'end')

        self.assertEqual(value,"0.11,8.999,8.81,9.99,1.19,7.25,3\n")











        


if __name__ == '__main__':
    unittest.main()