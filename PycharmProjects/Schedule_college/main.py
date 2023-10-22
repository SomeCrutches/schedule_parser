import tkinter as tk
from parse_html import Parser
from parse_xl import ScheduleParser
import time


class RoundedButton(tk.Canvas):
    def __init__(self, master, width, height, color, text, command=None):
        super().__init__(master, width=width, height=height, highlightthickness=0)
        self.rounded_rect = self.create_rounded_rect(0, 0, width, height, color)
        self.text = self.create_text(width // 2, height // 2, text=text, fill="white", font=("Arial", 12, "bold"))
        self.bind("<Button-1>", lambda _: command())

    def create_rounded_rect(self, x1, y1, x2, y2, color, radius=25):
        self.create_arc(x1, y1, x1 + 2 * radius, y1 + 2 * radius, start=90, extent=90, outline=color, fill=color)
        self.create_arc(x2 - 2 * radius, y1, x2, y1 + 2 * radius, start=0, extent=90, outline=color, fill=color)
        self.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, outline=color, fill=color)
        self.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, outline=color, fill=color)
        self.create_rectangle(x1 + radius, y1, x2 - radius, y2, outline=color, fill=color)
        self.create_rectangle(x1, y1 + radius, x2, y2 - radius, outline=color, fill=color)
        return self.find_all()


class CustomApp:
    def __init__(self, master):
        self.master = master
        master.title("Custom App")
        master.attributes('-fullscreen', True)
        master.bind("<F11>", self.toggle_fullscreen)
        master.bind("<Escape>", self.quit_fullscreen)

        # Код для текстового поля
        self.text_area = tk.Text(master, width=40, height=10, font=("Times New Roman", 12))
        self.text_area.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

        # Код для маленького текстового поля
        self.entry_label = tk.Label(master, text="Имя преподавателя:", font=("Times New Roman", 12))
        self.entry_label.grid(row=1, column=0, padx=5, pady=5)

        self.default_text = "Дедюхина А"

        self.entry = tk.Entry(master, font=("Times New Roman", 12))
        self.entry.insert(0, self.default_text)
        self.entry.bind("<FocusIn>", self.on_entry_click)
        self.entry.bind("<FocusOut>", self.on_focusout)
        self.entry.grid(row=1, column=1, padx=5, pady=5)

        # Код для кнопок
        self.button1 = RoundedButton(master, 250, 40, "green", "Скачать таблицы", self.download_tables)
        self.button1.grid(row=1, column=2, padx=5, pady=5)

        self.button2 = RoundedButton(master, 250, 40, "green", "Раскрыть таблицы", self.open_tables)
        self.button2.grid(row=1, column=3, padx=5, pady=5)

        self.quit_button = RoundedButton(master, 120, 40, "red", "Quit", master.quit)
        self.quit_button.grid(row=1, column=4, padx=5, pady=5)

        # Настройка заполнения строк и столбцов
        for i in range(2):
            master.grid_columnconfigure(i, weight=1)
        master.grid_rowconfigure(0, weight=1)

    def download_tables(self):
        self.text_area.insert(tk.END, "Скачивание началось(до минуты занимает).\n")
        first_links = Parser()

        start_time = time.time()
        first_links.parse_html()
        end_time = time.time()
        execution_time = round(end_time - start_time, 2)
        self.text_area.insert(tk.END, f"Парсинг страницы занял {execution_time} сек.\n")

        start_time = time.time()
        table = first_links.get_table()
        end_time = time.time()
        execution_time = round(end_time - start_time, 2)
        self.text_area.insert(tk.END, f"Парсинг таблицы занял {execution_time} сек.\n")

        start_time = time.time()
        links = first_links.parse_table(table)
        end_time = time.time()
        execution_time = round(end_time - start_time, 2)
        self.text_area.insert(tk.END, f"Парсинг таблицы занял {execution_time} сек.\n")

        start_time = time.time()
        first_links.download_tables(links)
        end_time = time.time()
        execution_time = round(end_time - start_time, 2)
        self.text_area.insert(tk.END, f"Скачивание таблиц заняло {execution_time} сек.\n")

        self.text_area.insert(tk.END, "Скачивание завершено.\n")

    def on_entry_click(self, event):
        if self.entry.get() == self.default_text:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, '')

    def on_focusout(self, event):
        if self.entry.get() == '':
            self.entry.insert(0, self.default_text)

    def open_tables(self):
        self.text_area.delete(1.0, tk.END)
        teacher_name = self.entry.get()
        if teacher_name == self.default_text:
            teacher_name = 'Дедюхина А'
        folder_path = 'Tables'
        parser = ScheduleParser(folder_path)
        parser.parse_schedule()
        teacher_pairs = parser.get_schedule()

        for teacher, pairs in teacher_pairs.items():
            if teacher_name in teacher:
                for pair in pairs:
                    self.text_area.insert(tk.END, f"День недели: {pair[0]}, Номер пары: {pair[1]}, Аудитория: {pair[2]}, Предмет: {pair[3]}, Группа: {pair[4]}\n")




    def toggle_fullscreen(self, event=None):
        self.master.attributes('-fullscreen', not self.master.attributes('-fullscreen'))

    def quit_fullscreen(self, event=None):
        self.master.attributes('-fullscreen', False)


root = tk.Tk()
app = CustomApp(root)
root.mainloop()
