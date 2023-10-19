import './App.css';
import { useRef } from 'react';         

import Button from '@mui/material/Button';
import DescriptionIcon from '@mui/icons-material/Description';


function Analyze() {
    const hiddenFileInput = useRef(null);

    const handleClick = event => {
        hiddenFileInput.current.click();
    };

    const handleChange = event => {
        const fileUploaded = event.target.files[0];
        handleFile(fileUploaded);                   // ADDED
    };
    const handleFile = file =>{
        fetch(file)
            .then(r => r.text())
            .then(text => {
            });
            alert("File uploaded");
        }    
     
    return (
        <div className="Analyze">
            <header className="App-header">
                
                    <p>
                        This is the page to analyze new statements.
                    </p>
                <Button onClick={handleClick}><DescriptionIcon fontSize='large'></DescriptionIcon> Add New Statement</Button>

                <input
                    type="file"
                    onChange={handleChange}
                    ref={hiddenFileInput}
                    style={{ display: 'none' }}
                />
            </header>
        </div>
    );
}

export default Analyze;
