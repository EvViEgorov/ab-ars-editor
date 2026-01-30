from tkinter import *
from tkinter import ttk
from tkinter import filedialog
 
root = Tk()
root.title("AB-ARS Editor")

for c in range(2): root.columnconfigure(index=c, weight=1)
for r in range(3): root.rowconfigure(index=r, weight=1)

label = Label(text="FILEPATH: ")
label.grid(column=0, columnspan=2, row=0)

text_editor = Text()
text_editor.grid(column=0, columnspan=2, row=1)

filepath = ""

def open_file():
    global filepath
    filepath = filedialog.askopenfilename()
    if filepath != "":
        label.config(text=f'FILEPATH: {filepath}')
        with open(filepath, "r", encoding="UTF-8") as file:
            text = file.read()
            text_editor.delete("1.0", END)
            text_editor.insert("1.0", text)

def save_file():
    if filepath != "FILEPATH: ":
        text = text_editor.get("1.0", END)
        with open(filepath, "w", encoding="UTF-8") as file:
            file.write(text)

btn = ttk.Button(text="Open File", command=open_file)
btn.grid(column=0, row=2)

btn = ttk.Button(text="Save File", command=save_file)
btn.grid(column=1, row=2)

root.mainloop()