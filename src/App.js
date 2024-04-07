import React, { useState } from 'react';
import axios from 'axios';

import './App.css';

const App = () => {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (file) {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await axios.post('http://localhost:8000/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        setUploadStatus(`Music Genre of your file : ${response.data["Music Genre"]}`);

      } catch (error) {
        console.error('Error uploading file:', error);
        setUploadStatus('Error uploading file');
      }
    } else {
      console.error('Please select a file.');
      setUploadStatus('Please select a file');
    }
  };

  return (
    <div className='uploaddiv'>
      <div className='uploadmain'> 
        
        <h1 className='uploadtext'>Upload .wav File</h1>
        <br></br>
        <br></br>
        <form onSubmit={handleSubmit} className='form'>
           <div className="custom-file-input">
             <input className="choosebtn" type="file" accept=".wav" onChange={handleFileChange} />
           </div>
          
           <button className = 'uploadbtn' type="submit">Upload</button>
        </form>
        {uploadStatus && <p style={{fontWeight : "bold"}}>{uploadStatus}</p>}
      </div>
    </div>
  );
};

export default App;