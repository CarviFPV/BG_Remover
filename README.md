# BG_Remover

A Python GUI application that removes backgrounds from PNG images in batch using the `rembg` library.

## Features

- 🖼️ Batch process multiple PNG images at once
- 📁 Easy folder selection for input and output
- 🎨 Simple and intuitive GUI built with tkinter
- 📊 Real-time progress tracking
- ⚡ Fast background removal using AI

## Requirements

- Python 3.7 or higher
- Windows, macOS, or Linux

## Installation

1. Clone this repository:
```bash
git clone https://github.com/CarviFPV/BG_Remover.git
cd BG_Remover
```

2. Create a virtual environment (recommended):
```bash
python -m venv .venv
```

3. Activate the virtual environment:
   - On Windows:
   ```bash
   .venv\Scripts\activate
   ```
   - On macOS/Linux:
   ```bash
   source .venv/bin/activate
   ```

4. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python app.py
```

2. In the GUI:
   - Click **Browse** next to "Input Folder" and select the folder containing your PNG images
   - Click **Browse** next to "Output Folder" and select where you want to save the processed images
   - Click **Remove Background** to start processing

3. Wait for the process to complete. The progress bar will show the current status.

4. Find your processed images (with transparent backgrounds) in the output folder!

## How it Works

The application uses the `rembg` library, which employs a U2-Net neural network model to automatically detect and remove backgrounds from images. The GUI is built with Python's tkinter library for a native desktop experience.

## Dependencies

- **rembg**: AI-powered background removal
- **Pillow (PIL)**: Image processing
- **tkinter**: GUI (included with Python)

## Notes

- The first run may take longer as rembg downloads the AI model
- Only PNG files are processed (case-insensitive)
- Output images are saved with the same filename as the input
- If an output file already exists, it will be overwritten

## License

See the LICENSE file for details.
