import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>

    <div className='header'>
      <p className='headeritems'>Home</p>
      <p className='headeritems'>about</p>
      <p className='headeritems'>Music genre ?</p>
      <p style={{width : "1000px"}}> </p>
      <p className='headeritems-left'>Music Genre classifier</p>
      

            
    </div>

    <div className='firstdiv'>
       <p className='music-genre-text'>MUSIC GENRE CLASSIFIER
       <p className='music-button' href='#find'>Find Your Music Genre !</p>

       </p>
    </div>

    <div className='seconddiv'>
         <div className='aboutheader'>
          <p className='abouttext'>About this website!</p>
          <p className='aboutdef'> A music genre classifier is a type of machine learning model that can automatically analyze 
            and categorize music into different genres based on various features such as audio spectrograms, tempo, 
            rhythm, and instrumentation. These classifiers are trained using labeled music data, where each piece of
             music is associated with a specific genre. Once trained, the classifier can predict the genre of new, 
             unseen music based on its features.</p>
         </div>
    </div>


    <App />

    <div className='copyright'>
      <p className='text'>
        Music Genre classifier
        <br></br>
        randomwalk.AI.copyright@2024
        </p>
      
    </div>

  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
