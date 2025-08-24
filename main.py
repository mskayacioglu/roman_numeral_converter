# main.py
import tkinter as tk
from gui import RomanConverterApp, center_window

def main():
    root = tk.Tk()
    root.title("Roman Numeral Converter")
    center_window(root, 600, 400)

    root.geometry("400x300")
    root.minsize(400, 300)

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    app = RomanConverterApp(root)
    app.grid(row=0, column=0, sticky="nsew")

    root.mainloop()

if __name__ == "__main__":
    main()

# TODO
# Report