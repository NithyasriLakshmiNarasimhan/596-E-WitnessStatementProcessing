// import React, { useState } from 'react';
import './App.css'

function FileContentDisplay({ content }) {
    return (
        
        <div>
            {content ? (
                <pre>{content}</pre>
            ) : (
                <p></p>
            )}
        </div>
    );
}

export default FileContentDisplay;