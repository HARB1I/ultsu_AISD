import tkinter as tk
from tkinter import messagebox
import csv


class Diamond:
    def __init__(self, canvas, center_x, center_y, width, height, color="black"):
        self.canvas = canvas
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.color = color
        self.id = self.draw()

    def draw(self):
        x0 = self.center_x
        y0 = self.center_y
        points = [
            x0,
            y0 - self.height / 2,  # верхняя точка
            x0 + self.width / 2,
            y0,  # правая точка
            x0,
            y0 + self.height / 2,  # нижняя точка
            x0 - self.width / 2,
            y0,  # левая точка
        ]
        return self.canvas.create_polygon(points, fill=self.color, outline="black")

    def move(self, dx, dy):
        self.center_x += dx
        self.center_y += dy
        self.canvas.move(self.id, dx, dy)

    def change_color(self, new_color):
        self.color = new_color
        self.canvas.itemconfig(self.id, fill=new_color)

    def intersects(self, other):
        return not (
            self.center_x + self.width / 2 < other.center_x - other.width / 2
            or self.center_x - self.width / 2 > other.center_x + other.width / 2
            or self.center_y + self.height / 2 < other.center_y - other.height / 2
            or self.center_y - self.height / 2 > other.center_y + other.height / 2
        )


class DiamondApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Программа для работы с ромбами")

        self.center_window(800, 850)

        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()

        self.add_canvas_grid()

        self.diamonds = []

        self.control_frame = tk.Frame(root)
        self.control_frame.pack()

        tk.Label(self.control_frame, text="Центр ромба по X:").grid(row=0, column=0)
        self.center_x_entry = tk.Entry(self.control_frame)
        self.center_x_entry.grid(row=0, column=1)

        tk.Label(self.control_frame, text="Центр ромба по Y:").grid(row=1, column=0)
        self.center_y_entry = tk.Entry(self.control_frame)
        self.center_y_entry.grid(row=1, column=1)

        tk.Label(self.control_frame, text="Ширина ромба:").grid(row=2, column=0)
        self.width_entry = tk.Entry(self.control_frame)
        self.width_entry.grid(row=2, column=1)

        tk.Label(self.control_frame, text="Высота ромба:").grid(row=3, column=0)
        self.height_entry = tk.Entry(self.control_frame)
        self.height_entry.grid(row=3, column=1)

        tk.Label(self.control_frame, text="Цвет:").grid(row=4, column=0)

        self.color_map = {
            "Чёрный": "black",
            "Красный": "red",
            "Синий": "blue",
            "Зелёный": "green",
            "Жёлтый": "yellow",
            "Фиолетовый": "purple",
            "Оранжевый": "orange",
        }

        self.color_var = tk.StringVar(value="Чёрный")
        self.color_menu = tk.OptionMenu(
            self.control_frame, self.color_var, *self.color_map.keys()
        )
        self.color_menu.grid(row=4, column=1)

        tk.Button(
            self.control_frame, text="Добавить ромб", command=self.add_diamond
        ).grid(row=5, column=0, columnspan=2)
        tk.Button(
            self.control_frame,
            text="Проверить пересечения",
            command=self.check_intersections,
        ).grid(row=6, column=0, columnspan=2)
        tk.Button(
            self.control_frame, text="Загрузить ромбы", command=self.load_diamonds
        ).grid(row=7, column=0, columnspan=2)
        tk.Button(
            self.control_frame, text="Очистить холст", command=self.clear_canvas
        ).grid(row=8, column=0, columnspan=2)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def add_canvas_grid(self):
        width = 800
        height = 600
        for i in range(0, width, 50):
            self.canvas.create_line(i, 0, i, height, fill="lightgray")
            if i > 0:
                self.canvas.create_text(
                    i, 10, text=str(i), fill="gray", font=("Arial", 8)
                )

        for j in range(0, height, 50):
            self.canvas.create_line(0, j, width, j, fill="lightgray")
            if j > 0:
                self.canvas.create_text(
                    10, j, text=str(j), fill="gray", font=("Arial", 8)
                )

        # Добавляем оси X и Y
        self.canvas.create_line(
            0, height // 2, width, height // 2, fill="black", width=2, arrow=tk.LAST
        )  # ось X
        self.canvas.create_line(
            width // 2, 0, width // 2, height, fill="black", width=2, arrow=tk.LAST
        )  # ось Y

        self.canvas.create_text(
            width // 2 + 20,
            height - 10,
            text="Y",
            fill="black",
            font=("Arial", 10, "bold"),
        )
        self.canvas.create_text(
            width - 10,
            height // 2 - 20,
            text="X",
            fill="black",
            font=("Arial", 10, "bold"),
        )

    def add_diamond(self):
        try:
            center_x = int(self.center_x_entry.get())
            center_y = int(self.center_y_entry.get())
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            color = self.color_map[self.color_var.get()]

            diamond = Diamond(self.canvas, center_x, center_y, width, height, color)
            self.diamonds.append(diamond)
        except ValueError:
            messagebox.showerror(
                "Ошибка", "Некорректный ввод! Пожалуйста, введите правильные числа."
            )

    def check_intersections(self):
        for i, d1 in enumerate(self.diamonds):
            for j, d2 in enumerate(self.diamonds):
                if i != j and d1.intersects(d2):
                    messagebox.showinfo(
                        "Пересечение", f"Ромб {i + 1} пересекается с ромбом {j + 1}."
                    )
                    return
        messagebox.showinfo("Пересечение", "Пересечений не найдено.")

    def load_diamonds(self):
        file_path = "diamonds.txt"
        try:
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) != 5:
                        continue
                    center_x, center_y, width, height, color = row
                    diamond = Diamond(
                        self.canvas,
                        int(center_x),
                        int(center_y),
                        int(width),
                        int(height),
                        color,
                    )
                    self.diamonds.append(diamond)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", f"Файл '{file_path}' не найден.")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат данных в файле.")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.add_canvas_grid()
        self.diamonds.clear()


if __name__ == "__main__":
    root = tk.Tk()
    app = DiamondApp(root)
    root.mainloop()
