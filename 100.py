import tkinter as tk

root =  tk.Tk()
tk.Label(root,text = "I love Python！").pack()
var = tk.StringVar(value = "Hi,what's up")
text_input = tk.Entry(root,textvariable = var)
text_input.pack()

def print_content():
	text_output['text'] = var.get()
	var.set('')

tk.Button(root,text = 'print',command = print_content).pack()
root.bind('<Return>',lambda event:print_content())

text_output = tk.Message(root,text = '')
text_output.pack()
root.mainloop()