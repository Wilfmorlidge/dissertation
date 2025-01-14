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
                instances_of_sub_widgets = (0,0)
                for widget1 in widget.winfo_children():
                    if isinstance(widget1, tk.Label):
                        instances_of_sub_widgets[0] += 1
                        for counter in range (0,(len(expected_button_titles)-1)):
                            if expected_button_titles[counter] == widget1.cget("text"):
                                del expected_button_titles[counter]
                    if isinstance(widget1, tk.Text):
                        instances_of_sub_widgets[1] += 1
                if instances_of_sub_widgets != (1,1):
                    fail_flag = 1

        self.assertEqual(expected_button_titles,[])
        self.assertEqual(fail_flag, 0)

                        

   # def test_clicking_a_button_changes_the_value_of_variable(self):
    #    root = tk.Tk()
     #   container = tk.Frame(root)
      #  display_width = 200
       # entry_height = 100
        #dictionary = {'fake_data_1':1}
        #variable = [None]
        #display_height = 500
        #single_input_scroll_list_entries(container,display_width,entry_height,dictionary, variable,display_height)

       # container.pack(side='top',pady=(10,0))

        #root.update_idletasks()
        #root.update()

      #  for widget in container.winfo_children():
       #     if ((isinstance(widget, tk.Button)) and (widget.cget("text")=='fake_data_1')):
        #        widget.invoke()

#        root.update_idletasks()
 #       root.update()

  #      self.assertEqual(variable,['fake_data_1',1])

   # def test_clicking_two_buttons_in_succession_leaves_the_value_of_variable_with_the_second_button(self):
    #    root = tk.Tk()
     #   container = tk.Frame(root)
      #  display_width = 200
       # entry_height = 100
       # dictionary = {'fake_data_1':1,'fake_data_2': 2}
       # variable = [None]
      #  display_height = 500
      #  single_input_scroll_list_entries(container,display_width,entry_height,dictionary, variable,display_height)

#        container.pack(side='top',pady=(10,0))

 #       root.update_idletasks()
  #      root.update()


   #     for widget in container.winfo_children():
    #        if ((isinstance(widget, tk.Button)) and (widget.cget("text")=='fake_data_1')):
     #           widget.invoke()

      #  root.update_idletasks()
       # root.update()

        #for widget in container.winfo_children():
         #   if ((isinstance(widget, tk.Button)) and (widget.cget("text")=='fake_data_2')):
          #      widget.invoke()

       # root.update_idletasks()
       # root.update()


        #self.assertEqual(variable,['fake_data_2',2])

    #def test_clicking_the_same_button_twice_resets_the_value_of_variable(self):
     #   root = tk.Tk()
      #  container = tk.Frame(root)
       # display_width = 200
       # entry_height = 100
       # dictionary = {'fake_data_1':1}
       # variable = [None]
       # display_height = 500
       # single_input_scroll_list_entries(container,display_width,entry_height,dictionary, variable,display_height)

        #container.pack(side='top',pady=(10,0))

       # root.update_idletasks()
       # root.update()


       # for widget in container.winfo_children():
       #     if ((isinstance(widget, tk.Button)) and (widget.cget("text")=='fake_data_1')):
       #         widget.invoke()
#
 #       root.update_idletasks()
  #      root.update()

        
   #     self.assertEqual(variable,['fake_data_1',1])

    #    for widget in container.winfo_children():
     #       if ((isinstance(widget, tk.Button)) and (widget.cget("text")=='fake_data_1')):
      #          widget.invoke()

       # root.update_idletasks()
        #root.update()


        #self.assertEqual(variable,[None])





        


if __name__ == '__main__':
    unittest.main()