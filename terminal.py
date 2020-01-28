import tkinter as tk

root = tk.Tk()

def update_btn_text():

    if str(btn_text.get()) == "Connect":

        btn_text.set("Disconnect")

    elif  str(btn_text.get()) == "Disconnect":

        btn_text.set("Connect")


btn_text = tk.StringVar()
btn = tk.Button(root, textvariable=btn_text, command=update_btn_text)
btn_text.set("Connect")

btn.pack()

root.mainloop()