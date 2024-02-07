import tkinter as tk
from PIL import ImageGrab
import pytesseract
from PIL import Image


def get_text_from_screen() -> str:
    image = Image.open('./screenshot.png')
    return pytesseract.image_to_string(image, lang='eng')


def get_formatter_text():
    return get_text_from_screen().lower().replace("\n", " ")


class ScreenshotApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.text = None
        self.y = None
        self.x = None
        self.begin_x = None
        self.begin_y = None
        self.end_x = None
        self.end_y = None
        self.canvas = tk.Canvas(self, cursor="cross")
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.rect = None
        self.overrideredirect(True)
        self.wait_visibility(self)
        self.wm_attributes("-alpha", 0.01)
        #self.geometry(f"1024x768+0+0")

        # Полный экран
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

    def on_button_press(self, event):
        self.begin_x = self.canvas.canvasx(event.x)
        self.begin_y = self.canvas.canvasy(event.y)

    def on_button_release(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)

        self.take_screenshot()
        self.quit()

    def take_screenshot(self):
        x1 = min(self.begin_x, self.end_x)
        y1 = min(self.begin_y, self.end_y)
        x2 = max(self.begin_x, self.end_x)
        y2 = max(self.begin_y, self.end_y)

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save('./screenshot.png')


def take_screenshot():
    app = ScreenshotApplication()
    app.mainloop()
    app.destroy()


if __name__ == '__main__':
    take_screenshot()
