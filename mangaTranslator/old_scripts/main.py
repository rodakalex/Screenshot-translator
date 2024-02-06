import tkinter as tk
from translate import Translator

from mangaTranslator.old_scripts.get_screen import make_screen


def translate_text(text, target_language='ru'):
    translator = Translator(to_lang=target_language)
    return translator.translate(text)


def _translate():
    translation_label.config(text=translate_text(text_entry.get("1.0", "end-1c")))


def select_all(event):
    event.widget.tag_add("sel", "1.0", "end")


def from_screen():
    text = make_screen()
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

    translation_label = tk.Label(window, text="")
    translation_label.pack()

    translate_button = tk.Button(window, text="Перевести", command=_translate)
    translate_button.pack(pady=10)

    screenshot_button = tk.Button(window, text="Скриншот", command=from_screen)
    screenshot_button.pack()

    status_label = tk.Label(window, text="")
    status_label.pack()

    window.mainloop()
