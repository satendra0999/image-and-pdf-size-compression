import time
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pikepdf

# Set appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("400x300")
        self.title("Loading...")
        self.overrideredirect(True)
        self.configure(fg_color="lightblue")

        self.frames = []
        self.load_gif("loading.gif")

        self.image_label = ctk.CTkLabel(self, text="")
        self.image_label.pack(expand=True)

        ctk.CTkLabel(self, text="🚀 Launching Image Compressor...", font=ctk.CTkFont(size=14), text_color="white").pack(pady=10)

        self.frame_index = 0
        self.animate()

    def load_gif(self, gif_name):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            gif_path = os.path.join(script_dir, gif_name)
            gif = Image.open(gif_path)
            for frame in range(0, gif.n_frames):
                gif.seek(frame)
                frame_image = ImageTk.PhotoImage(gif.copy().resize((200, 200)))
                self.frames.append(frame_image)
        except Exception as e:
            print("GIF load error:", e)

    def animate(self):
        if self.frames:
            self.image_label.configure(image=self.frames[self.frame_index])
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.after(100, self.animate)

class ImageCompressorApp(ctk.CTk):
    def change_theme(self, mode):
        ctk.set_appearance_mode(mode.lower())

    def __init__(self):
        super().__init__()
        self.title("🔥 Modern Image Compressor")
        self.geometry("600x600")
        self.resizable(False, False)
        self.compressed_image = None

        self.image_path = ""
        self.original_preview = None
        self.compressed_preview = None

        self.create_widgets()

    def create_widgets(self):
        theme_frame = ctk.CTkFrame(self, fg_color="transparent")
        theme_frame.pack(pady=5)

        ctk.CTkLabel(theme_frame, text="Theme:").pack(side="left", padx=5)

        self.theme_option = ctk.CTkOptionMenu(
            theme_frame,
            values=["Light", "Dark"],
            command=self.change_theme
        )
        self.theme_option.set("LIGHT")
        self.theme_option.pack(side="bottom")

        ctk.CTkLabel(self, text="📷 Image Compressor", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=15)

        self.file_label = ctk.CTkLabel(self, text="No file selected", wraplength=400)
        self.file_label.pack(pady=5)

        ctk.CTkButton(self, text="Browse", command=self.browse_file).pack(pady=5)

        ctk.CTkLabel(self, text="Compression Quality").pack(pady=10)
        self.quality_slider = ctk.CTkSlider(self, from_=1, to=100, number_of_steps=99)
        self.quality_slider.set(100)
        self.quality_slider.pack(pady=5)

        ctk.CTkButton(self, text="Compress", command=self.compress_image, fg_color="green").pack(pady=15)

        ctk.CTkButton(self, text="Convert to PDF", command=self.convert_image_to_pdf, fg_color="blue").pack(pady=5)

        previews_frame = ctk.CTkFrame(self)
        previews_frame.pack(pady=10)

        self.original_preview_label = ctk.CTkLabel(previews_frame, text="Original")
        self.original_preview_label.grid(row=0, column=0, padx=10)

        self.compressed_preview_label = ctk.CTkLabel(previews_frame, text="Compressed")
        self.compressed_preview_label.grid(row=0, column=1, padx=10)

        self.result_text = ctk.CTkLabel(self, text="", wraplength=500, font=ctk.CTkFont(size=12))
        self.result_text.pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("All Supported Files", "*.jpg *.jpeg *.png *.bmp *.pdf"),
                ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
                ("PDF Files", "*.pdf")
            ]
        )
        if file_path:
            self.image_path = file_path
            self.file_label.configure(text=os.path.basename(self.image_path))
            self.result_text.configure(text="")

            if self.image_path.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
                self.show_preview(self.image_path, self.original_preview_label)
            else:
                self.original_preview_label.configure(text="📄 PDF selected", image="")

    def compress_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select a file first.")
            return

        if self.image_path.lower().endswith(".pdf"):
            self.compress_pdf()
            return

        quality = int(self.quality_slider.get())
        output_path = os.path.join(os.path.dirname(self.image_path), "compressed_" + os.path.basename(self.image_path))

        try:
            with Image.open(self.image_path) as img:
                img.convert("RGB").save(output_path, "JPEG", optimize=True, quality=quality)

            original_size = os.path.getsize(self.image_path) / 1024
            compressed_size = os.path.getsize(output_path) / 1024
            saved_percent = (1 - compressed_size / original_size) * 100

            self.result_text.configure(
                text=f"✅ IMAGE Compression Done!\nOriginal: {original_size:.2f} KB\nCompressed: {compressed_size:.2f} KB\nSaved: {saved_percent:.2f}%"
            )
            self.show_preview(output_path, self.compressed_preview_label)
            self.compressed_image = Image.open(output_path)

        except Exception as e:
            messagebox.showerror("Compression Failed", str(e))

    def compress_pdf(self):
        input_path = self.image_path
        output_path = os.path.join(os.path.dirname(input_path), "compressed_" + os.path.basename(input_path))

        try:
            with pikepdf.open(input_path) as pdf:
                pdf.remove_unreferenced_resources()
                pdf.save(output_path)

            original_size = os.path.getsize(input_path) / 1024
            compressed_size = os.path.getsize(output_path) / 2048
            saved_percent = (1 - compressed_size / original_size) * 100

            self.result_text.configure(
                text=f"✅ PDF Compression Done!\nOriginal: {original_size:.2f} KB\nCompressed: {compressed_size:.2f} KB\nSaved: {saved_percent:.2f}%"
            )
            self.pdf_output_path = output_path

        except Exception as e:
            messagebox.showerror("PDF Compression Failed", str(e))

    def convert_image_to_pdf(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image file first.")
            return

        if not self.image_path.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
            messagebox.showerror("Invalid File", "Only image files can be converted to PDF.")
            return

        try:
            image = Image.open(self.image_path).convert("RGB")
            output_path = os.path.join(
                os.path.dirname(self.image_path),
                os.path.splitext(os.path.basename(self.image_path))[0] + "_converted.pdf"
            )
            image.save(output_path, "PDF", resolution=100.0)

            self.result_text.configure(text=f"✅ Image converted to PDF!\nSaved as: {os.path.basename(output_path)}")
            self.compressed_preview_label.configure(text="📄 PDF created", image="")

        except Exception as e:
            messagebox.showerror("Conversion Failed", str(e))

    def show_preview(self, path, label_widget):
        try:
            img = Image.open(path)
            img.thumbnail((140, 140))
            tk_img = ctk.CTkImage(light_image=img, size=(140, 140))
            label_widget.configure(image=tk_img, text="")
            label_widget.image = tk_img
        except Exception as e:
            label_widget.configure(text="⚠️ Preview failed")

# Run the app
if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()

    splash = SplashScreen(root)
    root.after(2000, splash.destroy)

    def launch_main():
        app = ImageCompressorApp()
        app.mainloop()

    root.after(2000, launch_main)
    root.mainloop()
