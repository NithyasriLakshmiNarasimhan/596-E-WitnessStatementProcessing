// import React, { useState } from 'react';
import './App.css'
import Box from '@mui/material/Box';

function FileContentDisplay({ content }) {
    return (
        
        <Box>
        {content ? (
                <pre>{content}</pre>
            ) : (
                <p></p>
            )}
        </Box>
    );
}

export default FileContentDisplay;