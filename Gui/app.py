"""Module providing a functionality of converting pdf to text."""

from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from Gui.ModalsWindows import ConfigWindow
from Gui.internalize import General
from Gui.Buffer import Buffer
from Gui import midas
from functools import partial


class MainWindow:
    Lk = "ru"

    def __init__(self):
        self.analyzer = midas.PDFP()
        self.__buffer = Buffer(self.analyzer.table_of_content)
        self.__chapter_selected = {}

        # Создаем основное окно
        root = Tk()
        root.title(General.title[self.Lk])
        root.overrideredirect(False)
        root.resizable(True, True)

        # Устанавливаем размер окна
        width, height = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry('%dx%d+200+100' % (width * 0.7, height * 0.6))

        # Создаем рамку для размещения элементов
        frame = ttk.Frame(root, borderwidth=0, relief="sunken")
        frame.pack(fill=BOTH, expand=True, padx=5, pady=5)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        # Zone of text
        text_frame = LabelFrame(frame, text=General.text_zone[self.Lk])
        text_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.__w_text_frame = text_frame

        text_widget = Text(text_frame, bg="black", fg="white", borderwidth=0, relief="sunken")
        text_widget.pack(fill=BOTH, expand=True)
        text_widget.bind('<KeyRelease>', self.__text_updated)
        self.__text_widget = text_widget

        # Button of editing text
        btn_frame = ttk.Frame(text_frame)
        btn_frame.pack()
        self.undo_btn = ttk.Button(btn_frame, text="U", width=1)
        self.undo_btn.pack(side=LEFT)
        self.cfg_btn = ttk.Button(btn_frame, text="Cfg", width=1, command=)
        self.cfg_btn.pack(side=LEFT)

        # Zone context
        lf = ttk.LabelFrame(frame, text="Context")
        lf.grid(row=0, column=1, sticky="nsew", ipadx=5, ipady=5)
        self.w_label_frame = lf

        # Кнопка для обработки данных
        self.process_button = ttk.Button(
            frame, text=General.source[self.Lk], command=self.open_file_dialog)
        self.process_button.grid(row=2, column=1, sticky="e")

        # Кнопка для закрытия окна
        # close_button = ttk.Button(
        #    root, text="Х", command=self.close_window, width=1)
        # close_button.place(relx=1.0, rely=0, anchor="ne")


        # Перемещение окна с помощью мыши
        root.bind("<ButtonPress-1>", self.on_press)
        #root.bind("<B1-Motion>", self.on_drag)

        self.root = root

    def run(self):
        self.__text_widget.insert(END, General.text_preview[self.Lk])
        self.__text_widget.configure(state="disabled")
        # Запускаем главный цикл обработки событий
        self.root.mainloop()

    # EVENT HANDLERS
    def on_drag(self, event):
        self.root.geometry(
            f"+{event.x_root - offset_x}+{event.y_root - offset_y}")

    def on_press(self, event):
        global offset_x, offset_y
        offset_x = event.x_root - self.root.winfo_x()
        offset_y = event.y_root - self.root.winfo_y()

    # BL
    def process_data(self):
        """
        process selected chapters and save them at file
        """
        # TODO file name should be configurable
        with open("./result.txt", "w") as f:
            print("Selected items:", self.__chapter_selected)
            for item in self.__chapter_selected.keys():
                if self.__chapter_selected[item].get():
                    f.write(self.__buffer.get(item))


    def close_window(self):
        self.root.destroy()

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(title="Select a File",
                                               filetypes=[("PDF files", "*.pdf"), ("Text files", "*.txt"),
                                                          ("All files", "*.*")])
        if file_path:
            # selected_file_label.config(text=f"Selected File: {file_path}")
            self.process_button["text"] = General.process[self.Lk]
            self.process_button["command"] = self.process_data
            self.process_file(file_path)

    def process_file(self, file_path):
        self.analyzer.set_source(file_path)
        self.analyzer.run()
        self.display_context_menu()

    def display_context_menu(self):
        if not self.analyzer.isError():  # should be replaced to exception
            row = 0
            for item, name, page in self.analyzer.get_context():
                link1 = Label(self.w_label_frame, text=item + ' ' + name, cursor="hand2")
                value = IntVar()
                self.__chapter_selected[item] = value
                enabled_checkbutton = ttk.Checkbutton(self.w_label_frame,
                                                      variable=value,
                                                      command=partial(self.__add_to_list, item))
                enabled_checkbutton.grid(row=row, column=0, padx=5)
                link1.grid(row=row, column=1)
                row += 1
                link1.bind("<Button-1>", func=partial(self.display_chapter_text, item))
                self.__buffer.update(self.analyzer.get_chapter(item), item)

    def __add_to_list(self, chapter: str, **kwargs):
        print(self.__chapter_selected[chapter].get())

    def display_chapter_text(self, chapter, event):
        if self.__text_widget["state"] == "disabled":
            self.__text_widget.config(state=NORMAL)
        self.__buffer.chapter_focus = chapter
        text = self.__buffer.get(chapter)
        self.__text_widget.replace("1.0", END, text)

    def __text_updated(self, *args, **kwargs):
        if self.__buffer.chapter_focus == "":
            return None
        text = self.__text_widget.get("1.0", END)
        self.__buffer.update(text=text)
