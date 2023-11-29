import * as React from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Analyze from "./Analyze"
import Statements from "./Statements"
import DynamicQA from "./DynamicQA"
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import HomeIcon from '@mui/icons-material/Home';
import GrainIcon from '@mui/icons-material/Grain';
import DescriptionIcon from '@mui/icons-material/Description';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import Home from "./Home"

export default function MyToolBar() {
    const navigate = useNavigate();

    const navigateToAnalyze = () => {
        navigate('./Analyze');
    };

    const navigateToClusters = () => {
        navigate('./DynamicQA');
    };
    const navigateToStatements = () => {
        navigate('./Statements');
    };

    const navigateHome = () => {
        navigate('./Home');
    };

    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static">
                <Toolbar>
                    <Button color="inherit" onClick={navigateHome}><HomeIcon></HomeIcon>Home</Button>
                    <Button color="inherit" onClick={navigateToAnalyze}><UploadFileIcon></UploadFileIcon>Upload Statement</Button>
                    <Button color="inherit" onClick={navigateToClusters}><GrainIcon></GrainIcon>Dynamic Q and A</Button>
                    <Button color="inherit" onClick={navigateToStatements}><DescriptionIcon></DescriptionIcon>Case Files</Button>
                </Toolbar>
            </AppBar>
            <Routes>
                <Route path="/Analyze" element={<Analyze />} />
                <Route path="/DynamicQA" element={<DynamicQA />} />
                <Route path="/Statements" element={<Statements />} />
                <Route path="/Home" element={<Home />} />
            </Routes>
        </Box>

    );
}

