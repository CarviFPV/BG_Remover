import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
from pathlib import Path
import threading
from rembg import remove
from PIL import Image


class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Background Remover")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Variables
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.processing = False
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="Background Remover", 
            font=("Arial", 18, "bold"),
            pady=20
        )
        title_label.pack()
        
        # Input folder section
        input_frame = tk.Frame(self.root, padx=20, pady=10)
        input_frame.pack(fill="x")
        
        input_label = tk.Label(input_frame, text="Input Folder:", font=("Arial", 10))
        input_label.pack(anchor="w")
        
        input_path_frame = tk.Frame(input_frame)
        input_path_frame.pack(fill="x", pady=5)
        
        self.input_entry = tk.Entry(
            input_path_frame, 
            textvariable=self.input_folder,
            font=("Arial", 9),
            state="readonly"
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        input_button = tk.Button(
            input_path_frame, 
            text="Browse", 
            command=self.browse_input_folder,
            width=10
        )
        input_button.pack(side="right")
        
        # Output folder section
        output_frame = tk.Frame(self.root, padx=20, pady=10)
        output_frame.pack(fill="x")
        
        output_label = tk.Label(output_frame, text="Output Folder:", font=("Arial", 10))
        output_label.pack(anchor="w")
        
        output_path_frame = tk.Frame(output_frame)
        output_path_frame.pack(fill="x", pady=5)
        
        self.output_entry = tk.Entry(
            output_path_frame, 
            textvariable=self.output_folder,
            font=("Arial", 9),
            state="readonly"
        )
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        output_button = tk.Button(
            output_path_frame, 
            text="Browse", 
            command=self.browse_output_folder,
            width=10
        )
        output_button.pack(side="right")
        
        # Progress section
        progress_frame = tk.Frame(self.root, padx=20, pady=20)
        progress_frame.pack(fill="x")
        
        self.progress_label = tk.Label(
            progress_frame, 
            text="Ready to process images", 
            font=("Arial", 9)
        )
        self.progress_label.pack(anchor="w", pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            mode="determinate",
            length=560
        )
        self.progress_bar.pack(fill="x")
        
        # Process button
        self.process_button = tk.Button(
            self.root, 
            text="Remove Background", 
            command=self.start_processing,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            pady=10,
            width=20,
            cursor="hand2"
        )
        self.process_button.pack(pady=20)
    
    def browse_input_folder(self):
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_folder.set(folder)
    
    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder.set(folder)
    
    def start_processing(self):
        if not self.input_folder.get():
            messagebox.showerror("Error", "Please select an input folder")
            return
        
        if not self.output_folder.get():
            messagebox.showerror("Error", "Please select an output folder")
            return
        
        if self.processing:
            messagebox.showwarning("Warning", "Processing already in progress")
            return
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self.process_images)
        thread.daemon = True
        thread.start()
    
    def process_images(self):
        self.processing = True
        self.process_button.config(state="disabled", bg="#cccccc")
        
        input_path = Path(self.input_folder.get())
        output_path = Path(self.output_folder.get())
        
        # Create output folder if it doesn't exist
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Get all PNG files
        png_files = list(input_path.glob("*.png"))
        total_files = len(png_files)
        
        if total_files == 0:
            self.root.after(0, lambda: messagebox.showinfo(
                "Info", 
                "No PNG files found in the input folder"
            ))
            self.processing = False
            self.process_button.config(state="normal", bg="#4CAF50")
            return
        
        # Process each file
        for idx, png_file in enumerate(png_files, 1):
            try:
                # Update progress
                progress_text = f"Processing {idx}/{total_files}: {png_file.name}"
                self.root.after(0, lambda text=progress_text: self.progress_label.config(text=text))
                
                progress_value = (idx / total_files) * 100
                self.root.after(0, lambda value=progress_value: self.progress_bar.config(value=value))
                
                # Read input image
                with Image.open(png_file) as input_image:
                    # Remove background
                    output_image = remove(input_image)
                    
                    # Save output image
                    output_file = output_path / png_file.name
                    output_image.save(output_file)
                
            except Exception as e:
                error_msg = f"Error processing {png_file.name}: {str(e)}"
                self.root.after(0, lambda msg=error_msg: messagebox.showerror("Error", msg))
        
        # Completed
        self.root.after(0, lambda: self.progress_label.config(
            text=f"Completed! Processed {total_files} images"
        ))
        self.root.after(0, lambda: messagebox.showinfo(
            "Success", 
            f"Successfully processed {total_files} images!"
        ))
        
        self.processing = False
        self.process_button.config(state="normal", bg="#4CAF50")


def main():
    root = tk.Tk()
    app = BackgroundRemoverApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
