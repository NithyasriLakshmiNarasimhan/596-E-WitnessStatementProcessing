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
import SearchIcon from '@mui/icons-material/Search';

function Analyze() {
    const hiddenFileInput = useRef(null);
    const [QandAResponse, setQandAResponse] = useState('');
    const [NERResponse, setNERResponse] = useState('');
    const [statement, setStatement] = useState('');
    const [newQs, setNewQs] = useState('');
    const [newQList, setnewQList] = useState([]);
    const [newQ, setNewQ] = useState('');
    const [currStatement, setCurrStatement] = useState('');
    const [fileName, setFileName] = useState('');
    const [currCaseName, setCurrCaseName] = useState('');
    const [savedMessage, setSavedMessage] = useState('');
    const [showCaseName, setShowCaseName] = useState('');
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
            setCurrStatement(text);
        };
        reader.readAsText(e.target.files[0]);
        setFileName(e.target.files[0].name)
    }
    const checkEnter = (e) => {
        if (e.key === 'Enter') {
            setShowCaseName("Case Name: " + currCaseName)
        }
    }
    const handleText = (e) => { 
        setCurrCaseName(e.target.value);
    }
    function sendData() {
        // sendQandA();
        sendNER();
    }
    function sendNER() {
        trackPromise(
            axios({
                method: "POST",
                url: "/NER",
                data: {
                    statement: currStatement,
                    caseName: currCaseName,
                    fileName: fileName
                }
            })
                .then((response) => {
                    const res = response.data
                    setNERResponse(res);
                    setSavedMessage("Saved Analysis to: "+currCaseName);
                }).catch((error) => {
                    if (error.response) {
                        console.log(error.response)
                        console.log(error.response.status)
                        console.log(error.response.headers)
                    }
                }));
    }


    function sendQandA() {
        trackPromise(
            axios({
                method: "POST",
                url: "/QandA",
                data: {
                    questions: newQList,
                    statement: currStatement
                }
            })
                .then((response) => {
                    const res = response.data
                    setQandAResponse("Questions and answers:\n" + res);
                    setStatement("Witness Statement:\n" + currStatement);

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
                variant="contained" onClick={handleClick}><DescriptionIcon fontSize='large'></DescriptionIcon> Upload New Statement</Button>

            <TextField style={{
                backgroundColor: "#21b6ae",
                fontSize: "16px",
                width: "20%",
                position: "absolute",
                left: "40%",
                top: "32%",
                color: "white"
            }} label="Case Name:" value={currCaseName} variant="filled" focused onChange={(e) => handleText(e)} onKeyDown={checkEnter} />
            <Button style={{
                borderRadius: 35,
                backgroundColor: "#21b6ae",
                padding: "10px 12px",
                fontSize: "16px",
                width: "20%",
                position: "absolute",
                left: "40%",
                top: "45%"
            }}
                variant="contained" onClick={sendData}><SearchIcon fontSize='large'></SearchIcon> Analyze Statement</Button>
            <header className="App-header">
                <div className='center'>
                    <LoadingIndicator />
                </div>
                <p>
                    {fileName}<br></br>
                    {showCaseName}<br></br>
                    {savedMessage}
                    <br></br>
                    <br></br>
                    {NERResponse}
                    <br></br>
                    <br></br>
                    {statement}
                    </p>

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
