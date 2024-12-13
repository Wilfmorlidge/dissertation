import tkinter as tk

def output_page(root,output_queue):
    def check_queue(root, output_queue):
        while not output_queue.empty():
            result = output_queue.get()
            print('this is the queue as received in the main thread' + str(result))
            label = tk.Label(root,text=str(result))
            label.pack(side = 'top',fill='y', expand=(True))
        root.after(500, lambda: check_queue(root,output_queue))
    

    for widget in root.winfo_children():
        widget.destroy()

    root.after(100,lambda: check_queue(root,output_queue))