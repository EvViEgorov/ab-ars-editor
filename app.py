from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from source.process import parse_sig_file

root = Tk()
root.title("AB-ARS Editor")

for c in range(3): root.columnconfigure(index=c, weight=1)
for r in range(3): root.rowconfigure(index=r, weight=1)

label = Label(text="FILEPATH: ")
label.grid(column=0, columnspan=3, row=0)

text_editor = Text()
text_editor.grid(column=0, columnspan=3, row=1)

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
    if filepath != "":
        text = text_editor.get("1.0", END)
        with open(filepath, "w", encoding="UTF-8") as file:
            file.write(text)

def parse_json():
    if filepath != "":
        with open(filepath, "r", encoding="UTF-8") as file:
            text = file.read()
            parsed_text = ''.join(parse_sig_file(text, text_only=True))
        text_editor.delete("1.0", END)
        text_editor.insert("1.0", parsed_text)


open_btn = ttk.Button(text="Open File", command=open_file)
open_btn.grid(column=0, row=2)

save_btn = ttk.Button(text="Save File", command=save_file)
save_btn.grid(column=1, row=2)

parse_btn = ttk.Button(text="Parse JSON", command=parse_json)
parse_btn.grid(column=2, row=2)

root.mainloop()