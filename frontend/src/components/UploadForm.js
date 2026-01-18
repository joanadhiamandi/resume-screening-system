import React, { useState } from 'react';
import axios from 'axios';
import './UploadForm.css';

function UploadForm({ onResultReceived }) {
  const [files, setFiles] = useState([]);
  const [jobDescription, setJobDescription] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const droppedFiles = Array.from(e.dataTransfer.files);
    const pdfFiles = droppedFiles.filter(file => file.type === 'application/pdf');
    
    if (pdfFiles.length + files.length > 10) {
      setError('Maximum 10 files allowed');
      return;
    }
    
    setFiles(prevFiles => [...prevFiles, ...pdfFiles].slice(0, 10));
    setError('');
  };

  const handleFileInput = (e) => {
    const selectedFiles = Array.from(e.target.files);
    const pdfFiles = selectedFiles.filter(file => file.type === 'application/pdf');
    
    if (pdfFiles.length + files.length > 10) {
      setError('Maximum 10 files allowed');
      return;
    }
    
    setFiles(prevFiles => [...prevFiles, ...pdfFiles].slice(0, 10));
    setError('');
  };

  const removeFile = (index) => {
    setFiles(prevFiles => prevFiles.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (files.length === 0) {
      setError('Please upload at least one resume');
      return;
    }
    
    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const formData = new FormData();
      
      // Add all files with the same field name 'files'
      files.forEach(file => {
        formData.append('files', file);
      });
      
      formData.append('job_description', jobDescription);

      const response = await axios.post(
        'http://127.0.0.1:8000/api/v1/screening/upload',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      console.log('Response:', response.data);
      onResultReceived(response.data);
      
      // Clear form
      setFiles([]);
      setJobDescription('');
      
    } catch (err) {
      console.error('Error:', err);
      setError(err.response?.data?.detail || 'Error uploading resumes');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-form-container">
      <h2>📄 Upload Resumes for Screening</h2>
      
      <form onSubmit={handleSubmit}>
        <div
          className={`dropzone ${dragActive ? 'active' : ''} ${files.length > 0 ? 'has-files' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => document.getElementById('fileInput').click()}
        >
          <input
            id="fileInput"
            type="file"
            multiple
            accept=".pdf"
            onChange={handleFileInput}
            style={{ display: 'none' }}
          />
          
          {files.length === 0 ? (
            <div className="dropzone-text">
              <p>📎 Drag & drop PDF resumes here</p>
              <small>or click to select (max 10 files)</small>
            </div>
          ) : (
            <div className="files-list">
              <p className="files-count">✅ {files.length} file(s) selected</p>
              {files.map((file, index) => (
                <div key={index} className="file-item">
                  <span className="file-name">📄 {file.name}</span>
                  <button
                    type="button"
                    className="remove-btn"
                    onClick={(e) => {
                      e.stopPropagation();
                      removeFile(index);
                    }}
                  >
                    ❌
                  </button>
                </div>
              ))}
              <small className="add-more">Click to add more files (max 10)</small>
            </div>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="jobDescription">Job Description:</label>
          <textarea
            id="jobDescription"
            className="job-description-input"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Enter the job description here..."
            rows="8"
            required
          />
        </div>

        {error && <div className="error-message">⚠️ {error}</div>}

        <button
          type="submit"
          className="submit-button"
          disabled={loading || files.length === 0}
        >
          {loading ? '🔄 Processing...' : `🚀 Screen ${files.length} Resume${files.length !== 1 ? 's' : ''}`}
        </button>
      </form>
    </div>
  );
}

export default UploadForm;
