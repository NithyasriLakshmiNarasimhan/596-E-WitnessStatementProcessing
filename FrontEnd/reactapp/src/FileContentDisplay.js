// import React, { useState } from 'react';
import './App.css'

function FileContentDisplay({ content }) {
    return (
        
        <div className='background'>     
           <div className='statement'>
            {content ? (
                <pre>{content}</pre>
            ) : (
                <p></p>
            )}
        </div>
        </div>

    );
}

export default FileContentDisplay;