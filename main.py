import tkinter as tk
import os

root = tk.Tk()

# os.system("") executes any command written inside the quotation marks (on linux atleast will try on windows later)
def neko():
	if os.name == 'posix':
		os.system("python3 hello.pyw")
	elif os.name == 'nt':
		os.system("game.pyw")

frame = tk.LabelFrame(root, text="Welcome to the Game, press the PLAY Button to play!", padx=20, pady=20)
frame.pack(padx = 10, pady = 10)

b_play = tk.Button(frame, text="PLAY", command=neko).pack()
b_exit = tk.Button(frame, text="EXIT", command=root.quit).pack()

l = tk.Label(frame, text="ENJOY THE GAME").pack()

root.mainloop()
