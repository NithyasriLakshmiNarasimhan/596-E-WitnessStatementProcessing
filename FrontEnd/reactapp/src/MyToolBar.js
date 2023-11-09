import * as React from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Analyze from "./Analyze"
import Statements from "./Statements"
import Clusters from "./Clusters"
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import HomeIcon from '@mui/icons-material/Home';
import SearchIcon from '@mui/icons-material/Search';
import GrainIcon from '@mui/icons-material/Grain';
import DescriptionIcon from '@mui/icons-material/Description';
import Home from "./Home"

export default function MyToolBar() {
    const navigate = useNavigate();

    const navigateToAnalyze = () => {
        navigate('./Analyze');
    };

    const navigateToClusters = () => {
        navigate('./Clusters');
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
                    <Button color="inherit" onClick={navigateToAnalyze}><SearchIcon></SearchIcon>Q and A</Button>
                    <Button color="inherit" onClick={navigateToClusters}><GrainIcon></GrainIcon>Clusters</Button>
                    <Button color="inherit" onClick={navigateToStatements}><DescriptionIcon></DescriptionIcon>N E R</Button>
                </Toolbar>
            </AppBar>
            <Routes>
                <Route path="/Analyze" element={<Analyze />} />
                <Route path="/Clusters" element={<Clusters />} />
                <Route path="/Statements" element={<Statements />} />
                <Route path="/Home" element={<Home />} />
            </Routes>
        </Box>

    );
}

