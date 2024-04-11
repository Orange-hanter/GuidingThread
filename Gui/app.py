"""Module providing a functionality of converting pdf to text."""


import tkinter as tk
from internalize import General


class MainWindow:

    Lk = "ru"

    def on_drag(self, event):
        self.root.geometry(
            f"+{event.x_root - offset_x}+{event.y_root - offset_y}")

    def on_press(self, event):
        global offset_x, offset_y
        offset_x = event.x_root - self.root.winfo_x()
        offset_y = event.y_root - self.root.winfo_y()

    def process_data(self):
        # Здесь вы можете добавить логику обработки данных из списка
        selected_items = [item for item, var in zip(
            items, checkboxes) if var.get()]
        print("Selected items:", selected_items)

    def close_window(self):
        self.root.destroy()

    def __init__(self):
        # Создаем основное окно
        self.root = tk.Tk()
        self.root.title(General.title[self.Lk])

        # Устанавливаем размер окна
        self.root.geometry("1920x1080")

        # Убираем рамку окна
        self.root.overrideredirect(True)

        # Создаем рамку для размещения элементов
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        # Зона с текстом
        text_frame = tk.LabelFrame(frame, text=General.text_zone[self.Lk])
        text_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Зона с контекстом
        list_label = tk.Label(
            frame, text=General.context[self.Lk], relief="solid")
        list_label.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Создаем текстовое поле и добавляем скроллбар
        text_widget = tk.Text(text_frame, wrap="word")
        text_widget.pack(expand=True, fill="both")
        self.text_widget = text_widget

        # Кнопка для обработки данных
        process_button = tk.Button(
            frame, text="Обработать", command=self.process_data)
        process_button.grid(row=2, column=1, sticky="e")

        # Кнопка для закрытия окна
        close_button = tk.Button(
            self.root, text="Х", command=self.close_window)
        close_button.place(relx=1.0, rely=0, anchor="ne")

        # Перемещение окна с помощью мыши
        offset_x = 0
        offset_y = 0
        self.root.bind("<ButtonPress-1>", self.on_press)
        self.root.bind("<B1-Motion>", self.on_drag)

    def run(self):
        # Пример текста для отображения
        example_text = "Пример текста для отображения в текстовой зоне. " * 10
        self.text_widget.insert(tk.END, example_text)
        # Запускаем главный цикл обработки событий
        self.root.mainloop()
