import './Statements.css';
import { useRef } from 'react';         
import axios from "axios";
import Button from '@mui/material/Button';
import DescriptionIcon from '@mui/icons-material/Description';
import { useState } from 'react';
import { usePromiseTracker } from "react-promise-tracker";
import { trackPromise } from 'react-promise-tracker';
import { TailSpin } from "react-loader-spinner";
import TextField from '@mui/material/TextField';

// this is Q AND A
function Analyze() {
    const hiddenFileInput = useRef(null);
    const [fileContent, setFileContent] = useState('');
    const [statement, setStatement] = useState('');

    const [newQList, setnewQList] = useState([]);
    const [newQ, setNewQ] = useState('');
    const handleClick = event => {
        hiddenFileInput.current.click();
    };


    const LoadingIndicator = props => {
        const { promiseInProgress } = usePromiseTracker();
        return (
            promiseInProgress && 
            <div>
                <TailSpin color="green" radius={"2px"}/>
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
    const checkEnter = (e) =>{
        if(e.key === 'Enter'){
            setnewQList(newQList => [...newQList, newQ]);
            setNewQ("");
            // alert(newQ);
        }
    }
    const handleText = (e) =>{
        setNewQ(e.target.value);
    }

    function sendData(text) {
        trackPromise(
        axios({
            method: "POST",
            url: "/QandA",
            data: {
                questions: newQList,
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
                    padding: "10px 12px",
                    fontSize: "16px",
                    width: "20%",
                    position: "absolute",
                    left: "40%",
                    top: "20%"
                }}
                    variant="contained" onClick={handleClick}><DescriptionIcon fontSize='large'></DescriptionIcon> Upload A Statement For Q and A</Button>
            
            <TextField style={{
                backgroundColor: "#21b6ae",
                fontSize: "16px",
                width: "20%",
                position: "absolute",
                left: "40%",
                top: "32%",
                color:"white"
            }} label="Additional Questions" value = {newQ} variant="filled" focused onChange={(e) => handleText(e)} onKeyDown={checkEnter} />
            
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

export default Analyze;
