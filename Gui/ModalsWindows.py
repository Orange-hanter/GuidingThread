import tkinter as tk


class ConfigWindow:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(None)

        label = tk.Label(self.window, text='This is a top level window.')
        label.pack()

        btn = tk.Button(self.window, text='Close Me', command=self.close)
        btn.pack()

        self.window.protocol('WM_DELETE_WINDOW', self.close)

    def close(self):
        self.window.destroy()
        self.root.deiconify()
