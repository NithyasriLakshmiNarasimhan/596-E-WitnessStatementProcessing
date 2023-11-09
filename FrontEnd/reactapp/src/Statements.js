import './Statements.css';
import { useRef } from 'react';
import axios from "axios";
import Button from '@mui/material/Button';
import DescriptionIcon from '@mui/icons-material/Description';
import { useState } from 'react';
import { usePromiseTracker } from "react-promise-tracker";
import { trackPromise } from 'react-promise-tracker';
import { TailSpin } from "react-loader-spinner";

// this is N E R 
function Statements() {
    const hiddenFileInput = useRef(null);
    const [fileContent, setFileContent] = useState('');
    const [statement, setStatement] = useState('');

    const handleClick = event => {
        hiddenFileInput.current.click();
    };


    const LoadingIndicator = props => {
        const { promiseInProgress } = usePromiseTracker();
        return (
            promiseInProgress &&
            <div>
                <TailSpin color="green" radius={"2px"} />
            </div >
        );
    }

    const showFile = async (e) => {
        e.preventDefault()
        const reader = new FileReader()
        reader.onload = async (e) => {
            const text = (e.target.result)
            console.log(text);
            // alert(text);
            sendData(text)
        };
        reader.readAsText(e.target.files[0]);
    }

    function sendData(text) {
        trackPromise(
            axios({
                method: "POST",
                url: "/NER",
                data: {
                    statement: text
                }
            })
                .then((response) => {
                    const res = response.data
                    // alert(res);
                    setFileContent(res);
                    setStatement(text);
                    // setProfileData(({
                    //     profile_name: res.name,
                    //     about_me: res.about
                    // }))
                }).catch((error) => {
                    if (error.response) {
                        console.log(error.response)
                        console.log(error.response.status)
                        console.log(error.response.headers)
                    }
                }));
    }

    return (
        <div className="Analyze">
            <Button style={{
                borderRadius: 35,
                backgroundColor: "#21b6ae",
                padding: "6px 12px",
                fontSize: "16px",
                width: "20%",
                position: "absolute",
                left: "40%",
                top: "20%"

            }}
                variant="contained" onClick={handleClick}><DescriptionIcon fontSize='large'></DescriptionIcon> Upload A Statement For NER</Button>
            <header className="App-header">
                <div className='center'>
                    <LoadingIndicator />
                </div>
                <p>{fileContent}
                <br></br><br></br>Your Witness Statement:<br></br><br></br>
                    {statement}</p>
                <input
                    type="file"
                    onChange={(e) => showFile(e)}
                    ref={hiddenFileInput}
                    style={{ display: 'none' }}
                />
            </header>
        </div>
    );
}

export default Statements;












// import './App.css'
// import * as React from 'react';
// import { useState } from 'react';
// import ListItem from '@mui/material/ListItem';
// import ListItemButton from '@mui/material/ListItemButton';
// import ListItemText from '@mui/material/ListItemText';
// import { FixedSizeList } from 'react-window';
// import FileContentDisplay from './FileContentDisplay';
// import DescriptionIcon from '@mui/icons-material/Description';
// import statement1 from './witnessstatements/statement1.txt'
// const texts = require.context('./witnessstatements', true);
// const textsList = texts.keys().map(text => texts(text));

// function Statements() {
//     const [fileContent, setFileContent] = useState('');


//     function renderRow(props) {
//         const { index, style } = props;
//         return (
//             <ListItem style={style} key={index} component="div" disablePadding>
//                 <ListItemButton onClick={() => showStatement(index)}>
//                     <DescriptionIcon></DescriptionIcon>
//                     <ListItemText primary={` Statement ${index + 1}`} />
//                 </ListItemButton>
//             </ListItem>
//         );
//     }

//     function showStatement(index) {
//         // alert(textsList[0]);
//         fetch(statement1)
//             .then(r => r.text())
//             .then(text => {
//                 setFileContent(text);
//             });
//     }

//     const nums = 10;
//     return (
//         <div className="background">
//         <div className="Statements">
//                 <div className= "foreground">
//                 <FixedSizeList
//                     height={300}
//                     width={200}
//                     itemSize={46}
//                     itemCount={nums}
//                     overscanCount={5}
//                 >
//                     {renderRow}
//                 </FixedSizeList>
//                 </div>
//                 <div className='background'>
//                     <div className='statement'>
//                 <FileContentDisplay content={fileContent} />
//                     </div>
//                 </div>
//             </div>
//             </div>
//     );
// }

// export default Statements;
