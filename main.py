from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vandens ženklas")
        self.root.geometry("600x600")
        self.root.minsize(600, 600)

        self.image_path = None
        self.watermark_text = tk.StringVar()
        self.font_size = tk.StringVar(value="30")
        self.font_name = tk.StringVar(value="Arial")
        self.position = tk.StringVar(value="Viršuje kairėje")
        self.repeat = tk.BooleanVar(value=False)
        self.font_color = tk.StringVar(value="White")

        self.fonts = {
            "Arial": "arial.ttf",
            "Calibri": "calibri.ttf",
            "Times New Roman": "times.ttf",
            "Verdana": "verdana.ttf",
            "Comic Sans MS": "comic.ttf"
        }

        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(main_frame, text="Pasirinkite nuotrauką:").grid(row=0, column=0, sticky="w")
        tk.Button(main_frame, text="Įkelti nuotrauką", command=self.load_image).grid(row=0, column=1, sticky="w")

        tk.Label(main_frame, text="Vandens ženklo tekstas:").grid(row=1, column=0, sticky="w")
        tk.Entry(main_frame, textvariable=self.watermark_text).grid(row=1, column=1, sticky="ew")

        tk.Label(main_frame, text="Teksto dydis:").grid(row=2, column=0, sticky="w")
        self.font_size_entry = tk.Entry(main_frame, textvariable=self.font_size)
        self.font_size_entry.grid(row=2, column=1, sticky="ew")
        validate_cmd = (self.root.register(self.validate_font_size), "%P")
        self.font_size_entry.config(validate="key", validatecommand=validate_cmd)

        tk.Label(main_frame, text="Šriftas:").grid(row=3, column=0, sticky="w")
        font_combobox = ttk.Combobox(main_frame, textvariable=self.font_name, values=list(self.fonts.keys()), state="readonly")
        font_combobox.grid(row=3, column=1, sticky="ew")
        font_combobox.current(0)

        tk.Label(main_frame, text="Padėtis:").grid(row=4, column=0, sticky="w")
        positions = ["Viršuje kairėje", "Viršuje centre", "Viršuje dešinėje", "Centre", "Apačioje kairėje", "Apačioje centre", "Apačioje dešinėje"]
        tk.OptionMenu(main_frame, self.position, *positions).grid(row=4, column=1, sticky="ew")

        tk.Label(main_frame, text="Teksto spalva:").grid(row=5, column=0, sticky="w")
        font_colors = ["White", "Black", "Red", "Green", "Blue"]
        tk.OptionMenu(main_frame, self.font_color, *font_colors).grid(row=5, column=1, sticky="ew")

        tk.Checkbutton(main_frame, text="Pasikartojantis vandens ženklas", variable=self.repeat).grid(row=6, column=0, columnspan=2, sticky="w")

        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(button_frame, text="Peržiūrėti vandens ženklą", command=self.preview_watermark).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Išsaugoti nuotrauką", command=self.save_image).pack(side=tk.LEFT, padx=5)

        self.image_label = tk.Label(main_frame)
        self.image_label.grid(row=7, column=0, columnspan=2, pady=10)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(7, weight=1)

    def validate_font_size(self, new_value):
        if new_value == "":
            return True
        try:
            value = int(new_value)
            if value >= 1:
                return True
            else:
                return False
        except ValueError:
            return False

    def is_font_size_valid(self):
        font_size = self.font_size.get()
        if font_size == "":
            return False
        try:
            value = int(font_size)
            if value < 1:
                return False
            return True
        except ValueError:
            messagebox.showerror("Klaida", "Teksto dydis turi būti sveikasis skaičius.")
            return False

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if self.image_path:
            self.show_image()

    def show_image(self):
        image = Image.open(self.image_path)
        self.display_image(image)

    def display_image(self, image):
        max_width = 500
        max_height = 400
        width, height = image.size
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def add_watermark(self):
        if not self.image_path:
            messagebox.showerror("Klaida", "Prašome įkelti nuotrauką!")
            return None
        if not self.is_font_size_valid():
            return None
        image = Image.open(self.image_path).convert("RGBA")
        width, height = image.size

        match self.font_color.get():
            case "White":
                txt = Image.new('RGBA', image.size, (255, 255, 255, 0))
                red = 255
                green = 255
                blue = 255
            case "Black":
                txt = Image.new('RGBA', image.size, (0, 0, 0, 0))
                red = 0
                green = 0
                blue = 0
            case "Red":
                txt = Image.new('RGBA', image.size, (255, 0, 0, 0))
                red = 255
                green = 0
                blue = 0
            case "Green":
                txt = Image.new('RGBA', image.size, (0, 255, 0, 0))
                red = 0
                green = 255
                blue = 0
            case "Blue":
                txt = Image.new('RGBA', image.size, (0, 0, 255, 0))
                red = 0
                green = 0
                blue = 255
            case _:
                txt = Image.new('RGBA', image.size, (255, 255, 255, 0))
                red = 255
                green = 255
                blue = 255

        draw = ImageDraw.Draw(txt)
        font_file = self.fonts.get(self.font_name.get(), "arial.ttf")
        try:
            font = ImageFont.truetype(font_file, int(self.font_size.get()))
        except IOError:
            messagebox.showerror("Klaida", "Nepavyko rasti šrifto. Naudojamas numatytasis šriftas.")
            font = ImageFont.load_default()

        text = self.watermark_text.get()
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        match self.position.get():
            case "Viršuje kairėje":
                x, y = 10, 10
            case "Viršuje centre":
                x, y = (width - text_width) // 2, 10
            case "Viršuje dešinėje":
                x, y = width - text_width - 10, 10
            case "Centre":
                x, y = (width - text_width) // 2, (height - text_height) // 2
            case "Apačioje kairėje":
                x, y = 10, height - text_height - 16
            case "Apačioje centre":
                x, y = (width - text_width) // 2, height - text_height - 16
            case "Apačioje dešinėje":
                x, y = width - text_width - 10, height - text_height - 16
            case _:
                x, y = 10, 10

        # Uždeda vandens ženkla
        if self.repeat.get():
            for i in range(0, width, text_width + 50):
                for j in range(0, height, text_height + 50):
                    draw.text((i, j), text, font=font, fill=(red, green, blue, 255))
        else:
            draw.text((x, y), text, font=font, fill=(red, green, blue, 255))
        watermarked_image = Image.alpha_composite(image, txt)
        return watermarked_image

    def preview_watermark(self):
        if not self.is_font_size_valid():
            return
        watermarked_image = self.add_watermark()
        if watermarked_image:
            self.display_image(watermarked_image)

    def save_image(self):
        if not self.is_font_size_valid():
            return
        watermarked_image = self.add_watermark()
        if watermarked_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                watermarked_image.save(save_path)
                messagebox.showinfo("Pasisekė", "Nuotrauka sėkmingai išsaugota!")

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()