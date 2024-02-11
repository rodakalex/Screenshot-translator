import asyncio
import tkinter as tk
import config
from make_screen import take_screenshot, get_formatter_text
import pyrogram

app = pyrogram.Client(config.name, config.api_id, config.api_hash)


async def get_last_message(text):
    try:
        async with app:
            await app.send_message(chat_id='YTranslateBot', text=text)
            await asyncio.sleep(1)
            async for message in app.get_chat_history(chat_id='YTranslateBot', limit=1, offset_id=-1):
                global mMessage_text
                mMessage_text = message.text
                print(message.text)
    except Exception as e:
        print(e)


def from_screen():
    take_screenshot()
    text = get_formatter_text()
    text_entry.delete("1.0", tk.END)
    text_entry.insert(tk.END, text)
    app.run(get_last_message(text))
    translation_label.config(text=mMessage_text)
    # app.stop()


def translate_text():
    text = text_entry.get("1.0", tk.END)
    app.run(get_last_message(text))
    translation_label.config(text=mMessage_text)
    # app.stop()


def select_all(event):
    event.widget.tag_add("sel", "1.0", "end")


def copy_text():
    text = text_entry.get("1.0", tk.END)
    window.clipboard_clear()
    window.clipboard_append(text)


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
    translate_button = tk.Button(window, text="Перевести", command=translate_text)
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
