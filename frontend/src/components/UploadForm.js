import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import './UploadForm.css';

function UploadForm({ onResultReceived }) {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      setError('');
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    maxFiles: 1
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please upload a PDF resume');
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
      formData.append('file', file);
      formData.append('job_description', jobDescription);

      const response = await axios.post(
        'http://127.0.0.1:8000/api/v1/screening/upload',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );

      onResultReceived(response.data);
      
      setFile(null);
      setJobDescription('');
      
    } catch (err) {
      setError(err.response?.data?.detail || 'Error uploading resume');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-form-container">
      <h2>📄 Upload Resume for Screening</h2>
      
      <form onSubmit={handleSubmit}>
        <div
          {...getRootProps()}
          className={`dropzone ${isDragActive ? 'active' : ''} ${file ? 'has-file' : ''}`}
        >
          <input {...getInputProps()} />
          {file ? (
            <div className="file-info">
              <p>✅ {file.name}</p>
              <small>{(file.size / 1024).toFixed(2)} KB</small>
            </div>
          ) : isDragActive ? (
            <p>📎 Drop the PDF here...</p>
          ) : (
            <div className="dropzone-text">
              <p>📎 Drag & drop a PDF resume here</p>
              <small>or click to select</small>
            </div>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="jobDescription">Job Description:</label>
          <textarea
            id="jobDescription"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Enter the job description here..."
            rows="8"
            className="job-description-input"
          />
        </div>

        {error && <div className="error-message">⚠️ {error}</div>}

        <button type="submit" className="submit-button" disabled={loading}>
          {loading ? '🔄 Screening Resume...' : '🚀 Screen Resume'}
        </button>
      </form>
    </div>
  );
}

export default UploadForm;
