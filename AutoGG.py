import tkinter
from tkinter import *

from threading import Thread
from PIL import Image, ImageTk
from kb import keyboard_check, read_keys

# Основа
root = Tk()

# Название
root.title("AutoGG")

# Размер, запрет расширения
root.geometry("225x280")
root.resizable(height=False, width=False)

# Иконка
root.iconphoto(True, PhotoImage(file='img/icon.png'))

# Фон
background_image = ImageTk.PhotoImage(Image.open("img/background.png"))

background_lable = Label(root, image=background_image)
background_lable.place(relheight=1, relwidth=1)

is_running = False

def create_keys():
    saved_values = []
    for lbl, entry in key_time_pairs:
        key_or_time = entry.get() if hasattr(entry, "get") else ""
        # key_or_time = entry.get()
        if lbl.cget("text") == "key":
            saved_values.append("key: " + key_or_time)
        elif lbl.cget("text") == "time":
            saved_values.append("time: " + key_or_time)
        elif lbl.cget("text") == "Активация:":
            saved_values.append("activate: " + key_or_time)
        elif lbl.cget("text") == "Ctrl" and len(key_or_time) == 1:
            saved_values.append("ctrl: " + key_or_time)
        elif lbl.cget("text") == "Shift" and len(key_or_time) == 1:
            saved_values.append("shift: " + key_or_time)
        elif lbl.cget("text") == "Enter":
            saved_values.append("enter")
        elif lbl.cget("text") == "Alt+" and len(key_or_time) == 1:
            saved_values.append("alt: " + key_or_time)

        print("lbl", lbl.cget("text"))

    with open("keylist.txt", "w", encoding='utf-8') as file:
        for i in saved_values:
            file.write(str(i + "\n"))

    global current_row

    settings_window.destroy()
    current_row = 1
    print(f'Сохраненные значения: {saved_values}')

def setting_destroy():
    global current_row
    settings_window.destroy()
    current_row = 1

def settings():
    global settings_window, place, key_time_pairs, current_row

    key_time_pairs = []
    current_row = 1

    # Window settings
    settings_window = tkinter.Toplevel(root)
    settings_window.title("Настройки")
    settings_window.iconphoto(False, PhotoImage(file='img/settings.png'))
    settings_window.geometry('180x300')
    settings_window.resizable(height=False, width=False)

    # Buttons

    button_add = Button(settings_window, text="Хоткей", font=("Comic Sans MS", 8), command=add_input)
    button_add.place(relx=0.16, rely=0.08, anchor="center")

    button_time = Button(settings_window, text="Пауза", font=("Comic Sans MS", 8), command=add_time)
    button_time.place(relx=0.15, rely=0.19, anchor="center")

    button_enter = Button(settings_window, text="Enter", font=("Comic Sans MS", 8), command=add_enter)
    button_enter.place(relx=0.14, rely=0.30, anchor="center")

    button_shift = Button(settings_window, text="Shift+", font=("Comic Sans MS", 8), command=add_shift)
    button_shift.place(relx=0.15, rely=0.41, anchor="center")

    button_ctrl = Button(settings_window, text="Ctrl+", font=("Comic Sans MS", 8), command=add_ctrl)
    button_ctrl.place(relx=0.14, rely=0.52, anchor="center")

    button_alt = Button(settings_window, text="Alt+", font=("Comic Sans MS", 8), command=add_alt)
    button_alt.place(relx=0.14, rely=0.63, anchor="center")

    button_time = Button(settings_window, text="Убрать", font=("Comic Sans MS", 8), command=remove_last_key)
    button_time.place(relx=0.16, rely=0.74, anchor="center")

    button_apply = Button(settings_window, text="Применить", font=("Comic Sans MS", 9), command=create_keys)
    button_apply.place(relx=0.7, rely=0.88, anchor="center")

    button_reset = Button(settings_window, text="Отмена", font=("Comic Sans MS", 9), command=setting_destroy)
    button_reset.place(relx=0.25, rely=0.88, anchor="center")

    # Блок активации
    label_description = Label(
        settings_window,
        text="(по умолчанию '-')",
        font=("Comic Sans MS", 7),
        fg="black",
    )
    label_description.place(relx=0.84, rely=0.15, anchor="se")

    label_activate = Label(
        settings_window,
        text="Активация:",
        font=("Comic Sans MS", 10),
        fg="black",
    )
    label_activate.place(relx=0.78, rely=0.1, anchor="se")

    entry_activation = Entry(settings_window, width=2, justify="center")
    entry_activation.place(relx=0.85, rely=0.055, anchor="center")

    key_time_pairs.append((label_activate, entry_activation))  # Сохраняем сами виджеты



def add_input():
    # Input
    global current_row, settings_window, place, entry_one

    if current_row > 12:
        return

    # Определение мест
    current_place = place[str(current_row)]

    # Кнопка
    input_one = Label(settings_window, text="key", font=("Comic Sans MS", 8))
    input_one.place(relx=current_place[0], rely=current_place[2], anchor="center")

    # Поле ввода
    entry_one = Entry(settings_window, width=2, justify="center")
    entry_one.place(relx=current_place[1], rely=current_place[2], anchor="center")

    key_time_pairs.append((input_one, entry_one))  # Сохраняем сами виджеты

    current_row += 1


    # print(current_place[0],current_place[1],current_place[2], f"Current row {current_row}")
    print(key_time_pairs)

# place = [0.5, 0.6, 0.2] - place[0] - x для первой, place[1] 0 х для второй, place[2] - y для обоих

def add_time():
    # Time
    global current_row, settings_window, place

    if current_row > 12:
        return

    current_place = place[str(current_row)]

    input_one = Label(settings_window, text="time", font=("Comic Sans MS", 8))
    input_one.place(relx=current_place[0], rely=current_place[2], anchor="center")
    entry_one = Entry(settings_window, width=2, justify="center")
    entry_one.place(relx=current_place[1], rely=current_place[2], anchor="center")

    vcmd = settings_window.register(validate_input)

    key_time_pairs.append((input_one, entry_one))

    current_row += 1

def add_ctrl():
    # Ctrl
    global current_row, settings_window, place

    if current_row > 12:
        return

    current_place = place[str(current_row)]

    input_one = Label(settings_window, text="Ctrl", font=("Comic Sans MS", 8))
    input_one.place(relx=current_place[0] - 0.01, rely=current_place[2], anchor="center")
    entry_one = Entry(settings_window, width=2, justify="center")
    entry_one.place(relx=current_place[1], rely=current_place[2], anchor="center")

    vcmd = settings_window.register(validate_input)

    key_time_pairs.append((input_one, entry_one))

    current_row += 1

def add_shift():
    # Shift
    global current_row, settings_window, place

    if current_row > 12:
        return

    current_place = place[str(current_row)]

    input_one = Label(settings_window, text="Shift", font=("Comic Sans MS", 7))
    input_one.place(relx=current_place[0] - 0.01, rely=current_place[2], anchor="center")
    entry_one = Entry(settings_window, width=2, justify="center")
    entry_one.place(relx=current_place[1], rely=current_place[2], anchor="center")

    vcmd = settings_window.register(validate_input)

    key_time_pairs.append((input_one, entry_one))

    current_row += 1

def add_alt():
    # Alt
    global current_row, settings_window, place

    if current_row > 12:
        return

    current_place = place[str(current_row)]

    input_one = Label(settings_window, text="Alt+", font=("Comic Sans MS", 8))
    input_one.place(relx=current_place[0], rely=current_place[2], anchor="center")
    entry_one = Entry(settings_window, width=2, justify="center")
    entry_one.place(relx=current_place[1], rely=current_place[2], anchor="center")

    vcmd = settings_window.register(validate_input)

    key_time_pairs.append((input_one, entry_one))

    current_row += 1


def add_enter():
    global current_row, settings_window, place

    if current_row > 12:
        return

    current_place = place[str(current_row)]

    input_one = Label(settings_window, text="Enter", font=("Comic Sans MS", 8))
    input_one.place(relx=current_place[0] + 0.05, rely=current_place[2], anchor="center")


    vcmd = settings_window.register(validate_input)

    key_time_pairs.append((input_one, ''))

    current_row += 1


def validate_input(new_value):
    return len(new_value) <= 1

def remove_last_key():
    global key_time_pairs, current_row
    if key_time_pairs:  # Проверяем, есть ли элементы для удаления
        if current_row >= 2:
            lbl, entry = key_time_pairs.pop()  # Удаляем последнюю пару
            lbl.destroy()  # Убираем с экрана Label
            current_row -= 1  # Уменьшаем счётчик
            if hasattr(entry, 'destroy'):
                entry.destroy() # Убираем с экрана Entry


def start():
    global is_running, button_start

    # Проверка на нажати кнопки запуска
    if not is_running:
        is_running = True

        # Смена кнопки
        button_start.config(text="Остановить", font=("Comic Sans MS", 10))
        # Запуск в отдельном потоке, daemon автоматически завершаются, когда основной поток программы заканчивает своё выполнение.
        Thread(target=keyboard_check, args=(lambda: is_running,), daemon=True).start()
    else:
        button_start.config(text="Запуск", font=("Comic Sans MS", 10), command=start)
        is_running = False

        print(f"Остановлено")

# Места размещения полей ввода
place = {
    "1": [0.385, 0.5, 0.2],
    "2": [0.385, 0.5, 0.3],
    "3": [0.385, 0.5, 0.4],
    "4": [0.385, 0.5, 0.5],
    "5": [0.385, 0.5, 0.6],
    "6": [0.385, 0.5, 0.7],
    "7": [0.735, 0.85, 0.2],
    "8": [0.735, 0.85, 0.3],
    "9": [0.735, 0.85, 0.4],
    "10": [0.735, 0.85, 0.5],
    "11": [0.735, 0.85, 0.6],
    "12": [0.735, 0.85, 0.7]
}
current_row = 1

# Список для хранения сохраненных значений
key_time_pairs = []

# Хранение значений
saved_data = []

# Кнопки
button_start = Button(root, text="Запуск", font=("Comic Sans MS", 10), command=start)
button_start.place(relx=0.5, rely=0.45, anchor="center")

button_settings = Button(root, text="Настройки", command=settings)
button_settings.place(relx=0.5, rely=0.82, anchor="center")

# Авторство
label_author = Label(
    root,
    text="By PowerOfLuck",
    font=("Comic Sans MS", 10),
    fg="green",
    bg="black"
)
label_author.place(relx=1.0, rely=1.0, anchor="se")



root.mainloop()