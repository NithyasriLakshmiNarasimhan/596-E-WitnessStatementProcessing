import './Statements.css';
import { usePromiseTracker } from "react-promise-tracker";
import { TailSpin } from "react-loader-spinner";
// import CaseList from './CaseList'
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import FolderIcon from '@mui/icons-material/Folder';
import DriveFolderUploadIcon from '@mui/icons-material/DriveFolderUpload';
import { useState, useEffect } from 'react';
import axios from "axios";

import { trackPromise } from 'react-promise-tracker';

function Statements() {
    const [fileContent, setFileContent] = useState('');
    const [fileNames, setFileNames] = useState([]);
    const [currPath, setCurrPath] = useState([]);

    const LoadingIndicator = props => {
        const { promiseInProgress } = usePromiseTracker();
        return (
            promiseInProgress &&
            <div>
                <TailSpin color="green" radius={"2px"} />
            </div >
        );
    }
    useEffect(() => {
        trackPromise(
            axios({
                method: "POST",
                url: "/getFiles",
                data: { fileNum: "File 1" }
            })
                .then((response) => {
                    const res = response.data
                    // alert(res);
                    setFileNames(res);
                }).catch((error) => {
                    if (error.response) {
                        console.log(error.response)
                        console.log(error.response.status)
                        console.log(error.response.headers)
                    }
                }));
    }, []);
    const moveUp = (event) => {
        if (currPath.length === 0) {
            return;
        }
        let filePath = "";
        let newPath = [...currPath];
        newPath.pop()
        newPath.forEach((e) => filePath += (e + "/"));
        setCurrPath(newPath)
        trackPromise(
            axios({
                method: "POST",
                url: "/getFileContent",
                data: { fileNum: filePath }
            })
                .then((response) => {
                    const res = response.data
                    // alert(res);
                    setFileNames(res[0])
                }).catch((error) => {
                    if (error.response) {
                        console.log(error.response)
                        console.log(error.response.status)
                        console.log(error.response.headers)
                    }
                }));
    }
    const handleListItemClick = (event, index) => {
        // hideList();
        let filePath = "";
        currPath.forEach((e) => filePath += (e + "/"));
        filePath += index;
        let newPath = [...currPath];
        setCurrPath(newPath)
        trackPromise(
            axios({
                method: "POST",
                url: "/getFileContent",
                data: { fileNum: filePath }
            })
                .then((response) => {
                    const res = response.data
                    // alert(res);
                    if(res[1] !== ""){
                    setFileContent(res[1]);}
                    if (res[0].length !== 0) {
                        setFileNames(res[0])
                        newPath.push(index)
                    }
                }).catch((error) => {
                    if (error.response) {
                        console.log(error.response)
                        console.log(error.response.status)
                        console.log(error.response.headers)
                    }
                }));
    };

    return (
        <header className="App-header">
            <Box id='fileList' sx={{ width: '20%', bgcolor: 'primary.list' }} style={{ position: 'absolute', top: '10%' }}>
                <List component="nav" aria-label="main mailbox folders">
                    <ListItemButton
                        onClick={(event) => moveUp(event)}
                    >
                        <ListItemIcon>
                            <DriveFolderUploadIcon style={{ fill: "white" }} />
                        </ListItemIcon>
                        {/* <ListItemText primary={currPath[currPath.length-1]+":"} /> */}
                    </ListItemButton>
                    {fileNames.map(e => {
                        return (
                            <ListItemButton
                                onClick={(event) => handleListItemClick(event, e)}
                            >
                                <ListItemIcon>
                                    <FolderIcon style={{ fill: "white" }} />
                                </ListItemIcon>
                                <ListItemText primary={e} />
                            </ListItemButton>);
                    })}
                </List>
            </Box>

            <p>
                <div style={{ position: 'relative', left: '20%', right: '10%', width: '70%', top: '-200px' }}>
                    {fileContent}
                </div>
            </p>
            <div className='center'>
                <LoadingIndicator />
            </div>
        </header>
    );
}
export default Statements;

