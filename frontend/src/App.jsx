import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = '/api';

function App() {
  const [files, setFiles] = useState([]);
  const [processing, setProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState('');

  const handleFileChange = (event) => {
    const selectedFiles = Array.from(event.target.files);
    const imageFiles = selectedFiles.filter(file => 
      file.type === 'image/png' || file.type === 'image/jpeg' || file.type === 'image/jpg'
    );
    
    if (imageFiles.length !== selectedFiles.length) {
      setMessage('Only PNG and JPEG images are supported. Some files were filtered out.');
    }
    
    setFiles(imageFiles);
    setMessage(`${imageFiles.length} file(s) selected`);
  };

  const handleSingleUpload = async () => {
    if (files.length === 0) {
      setMessage('Please select at least one image');
      return;
    }

    setProcessing(true);
    setProgress(0);
    setMessage('Processing...');

    try {
      const file = files[0];
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(`${API_URL}/remove-background`, formData, {
        responseType: 'blob',
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setProgress(percentCompleted);
        }
      });

      // Download the processed image
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${file.name.split('.')[0]}_no_bg.png`);
      document.body.appendChild(link);
      link.click();
      link.remove();

      setMessage('✅ Background removed successfully!');
      setProgress(100);
    } catch (error) {
      setMessage(`❌ Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setProcessing(false);
    }
  };

  const handleBatchUpload = async () => {
    if (files.length === 0) {
      setMessage('Please select at least one image');
      return;
    }

    setProcessing(true);
    setProgress(0);
    setMessage(`Processing ${files.length} image(s)...`);

    try {
      const formData = new FormData();
      files.forEach(file => {
        formData.append('files', file);
      });

      const response = await axios.post(`${API_URL}/remove-background-batch`, formData, {
        responseType: 'blob',
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setProgress(percentCompleted);
        }
      });

      // Download the ZIP file
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'processed_images.zip');
      document.body.appendChild(link);
      link.click();
      link.remove();

      setMessage(`✅ Successfully processed ${files.length} image(s)!`);
      setProgress(100);
    } catch (error) {
      setMessage(`❌ Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setProcessing(false);
    }
  };

  const clearFiles = () => {
    setFiles([]);
    setMessage('');
    setProgress(0);
  };

  return (
    <div className="App">
      <div className="container">
        <h1>🎨 Background Remover</h1>
        <p className="subtitle">Remove backgrounds from your images using AI</p>

        <div className="upload-section">
          <label htmlFor="file-upload" className="file-label">
            <input
              id="file-upload"
              type="file"
              accept="image/png,image/jpeg,image/jpg"
              multiple
              onChange={handleFileChange}
              disabled={processing}
            />
            <span className="button-text">
              📁 Choose Images
            </span>
          </label>

          {files.length > 0 && (
            <div className="file-list">
              <h3>Selected Files ({files.length}):</h3>
              <ul>
                {files.map((file, index) => (
                  <li key={index}>
                    {file.name} ({(file.size / 1024).toFixed(2)} KB)
                  </li>
                ))}
              </ul>
              <button onClick={clearFiles} className="clear-button" disabled={processing}>
                Clear
              </button>
            </div>
          )}
        </div>

        {files.length > 0 && (
          <div className="action-buttons">
            {files.length === 1 ? (
              <button 
                onClick={handleSingleUpload} 
                disabled={processing}
                className="process-button"
              >
                {processing ? '⏳ Processing...' : '✨ Remove Background'}
              </button>
            ) : (
              <button 
                onClick={handleBatchUpload} 
                disabled={processing}
                className="process-button"
              >
                {processing ? '⏳ Processing...' : `✨ Process ${files.length} Images`}
              </button>
            )}
          </div>
        )}

        {processing && (
          <div className="progress-section">
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <p className="progress-text">{progress}%</p>
          </div>
        )}

        {message && (
          <div className={`message ${message.includes('❌') ? 'error' : 'success'}`}>
            {message}
          </div>
        )}

        <div className="info-section">
          <h3>ℹ️ How to Use</h3>
          <ol>
            <li>Click "Choose Images" to select one or more PNG/JPEG images</li>
            <li>Click "Remove Background" to process your images</li>
            <li>Single image: Downloads directly as PNG</li>
            <li>Multiple images: Downloads as a ZIP file</li>
          </ol>
        </div>
      </div>
    </div>
  );
}

export default App;
