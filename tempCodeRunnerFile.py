def download_image(self):
    #     if self.image_path.lower().endswith(".pdf"):
    #         file_path = filedialog.asksaveasfilename(
    #             defaultextension=".pdf",
    #             filetypes=[("PDF File", "*.pdf")],
    #             title="Save Compressed PDF"
    #         )
    #         if file_path:
    #             shutil.copyfile(self.pdf_output_path, file_path)
    #             messagebox.showinfo("Success", f"PDF saved to:\n{file_path}")
    #         else:
    #             messagebox.showwarning("No File", "Save location not selected.")
    #         return

    #     if self.compressed_image:
    #         file_path = filedialog.asksaveasfilename(
    #             defaultextension=".jpg",
    #             filetypes=[("JPEG Image", "*.jpg"), ("PNG Image", "*.png")],
    #             title="Save Compressed Image"
    #         )
    #         if file_path:
    #             self.compressed_image.save(file_path)
    #             messagebox.showinfo("Success", f"Image saved to:\n{file_path}")
    #     else:
    #         messagebox.showwarning("No Image", "No compressed image to download.")