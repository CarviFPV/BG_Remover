from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
import io
from typing import List
import zipfile
import os

app = FastAPI(title="Background Remover API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3005",      # Docker frontend
        "http://localhost:3000",      # Local dev frontend
        "http://localhost:5173",      # Vite dev server
        "http://frontend:80",         # Docker internal network
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Background Remover API",
        "version": "1.0.0",
        "endpoints": {
            "/remove-background": "POST - Remove background from a single image",
            "/remove-background-batch": "POST - Remove background from multiple images"
        }
    }


@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    """
    Remove background from a single PNG image
    """
    # Validate file type
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(
            status_code=400,
            detail="Only PNG, JPG, and JPEG files are supported"
        )
    
    try:
        # Read the uploaded file
        contents = await file.read()
        input_image = Image.open(io.BytesIO(contents))
        
        # Remove background
        output_image = remove(input_image)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        # Get original filename without extension
        original_name = os.path.splitext(file.filename)[0]
        
        return StreamingResponse(
            img_byte_arr,
            media_type="image/png",
            headers={
                "Content-Disposition": f"attachment; filename={original_name}_no_bg.png"
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


@app.post("/remove-background-batch")
async def remove_background_batch(files: List[UploadFile] = File(...)):
    """
    Remove background from multiple images and return as a ZIP file
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    # Validate all files
    for file in files:
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise HTTPException(
                status_code=400,
                detail=f"File {file.filename} is not a supported image format"
            )
    
    try:
        # Create a ZIP file in memory
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file in files:
                # Read and process each image
                contents = await file.read()
                input_image = Image.open(io.BytesIO(contents))
                
                # Remove background
                output_image = remove(input_image)
                
                # Convert to bytes
                img_byte_arr = io.BytesIO()
                output_image.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)
                
                # Get original filename without extension
                original_name = os.path.splitext(file.filename)[0]
                
                # Add to ZIP
                zip_file.writestr(
                    f"{original_name}_no_bg.png",
                    img_byte_arr.getvalue()
                )
        
        zip_buffer.seek(0)
        
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={
                "Content-Disposition": "attachment; filename=processed_images.zip"
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing images: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint for Docker"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
