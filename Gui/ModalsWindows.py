import tkinter as tk
from tkinter import ttk


class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        width, height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry('%dx%d+300+150' % (width * 0.2, height * 0.1))


class ConfigWindow(Window):
    def __init__(self, parent, getter, setter, update):
        super().__init__(parent)
        self.title('Parser configuration')
        self.update_configuration = setter
        self.get_configuration = getter

        self.__menu_pattern = tk.StringVar(self, value=self.get_configuration("menu_pattern"))
        self.__menu_start_page = tk.StringVar(self, value=self.get_configuration("menu_page"))
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)

        # Regular expression
        ttk.Label(self, text='Menu Parser:').grid(row=0, column=0, padx=5, pady=5)

        self.menu_regex_entry = ttk.Entry(self, width=50, )
        self.menu_regex_entry.config(validate='focusout', textvariable=self.__menu_pattern)
        self.menu_regex_entry.grid(row=0, column=1, columnspan=2, padx=5)

        # Token ??

        # Menu page start
        ttk.Label(self, text='Menu start page:').grid(row=1, column=0, padx=5, pady=5)
        # TODO add validation
        self.menu_start_entry = ttk.Entry(self, width=50)
        self.menu_start_entry.config(validate='focusout', textvariable=self.__menu_start_page)
        self.menu_start_entry.grid(row=1, column=1, columnspan=2, padx=5)

        #self.label_error = ttk.Label(self, foreground='red')
        #self.label_error.grid(row=1, column=1, sticky=tk.W, padx=5)

        # Save changes
        self.save_button = ttk.Button(self, text='Save', command=self.on_update)
        self.save_button.grid(row=6, column=4, padx=5)

    def on_update(self):
        self.update_configuration("menu_pattern", self.__menu_pattern.get(), False)
        self.update_configuration("menu_page", int(self.__menu_start_page.get()))

        self.destroy()
