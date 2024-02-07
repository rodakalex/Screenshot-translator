import tkinter as tk
from translate import Translator

from make_screen import take_screenshot, get_formatter_text


def translate_text(text, target_language='ru'):
    translator = Translator(to_lang=target_language)
    return translator.translate(text)


def _translate():
    translation_label.config(text=translate_text(text_entry.get("1.0", "end-1c")))


def select_all(event):
    event.widget.tag_add("sel", "1.0", "end")


def copy_text():
    text = text_entry.get("1.0", tk.END)
    window.clipboard_clear()
    window.clipboard_append(text)


def from_screen():
    take_screenshot()
    text = get_formatter_text()
    text_entry.delete("1.0", tk.END)
    text_entry.insert(tk.END, text)
    ru_text = translate_text(text)
    translation_label.config(text=translate_text(ru_text))


if __name__ == '__main__':
    window = tk.Tk()
    window.title("Qua")
    window.geometry("400x200")

    text_entry = tk.Text(window, height=5, width=45)
    text_entry.pack(pady=10)
    text_entry.bind("<Control-a>", select_all)

    translation_label = tk.Label(window, text="", wraplength=350)
    translation_label.pack()

    # Создание и размещение кнопки "Перевести"
    translate_button = tk.Button(window, text="Перевести", command=_translate)
    translate_button.pack(side="left", padx=10, pady=10)

    # Создание и размещение кнопки "Скриншот"
    screenshot_button = tk.Button(window, text="Скриншот", command=from_screen)
    screenshot_button.pack(side="left", padx=10, pady=10)

    # Создание и размещение кнопки "Копировать"
    copy_button = tk.Button(window, text="Копировать", command=copy_text)
    copy_button.pack(side="left", padx=10, pady=10)

    status_label = tk.Label(window, text="")
    status_label.pack()

    window.mainloop()
