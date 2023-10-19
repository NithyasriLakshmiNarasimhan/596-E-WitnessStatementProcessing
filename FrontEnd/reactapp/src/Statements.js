import './App.css'
import * as React from 'react';
import { useState } from 'react';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import { FixedSizeList } from 'react-window';
import FileContentDisplay from './FileContentDisplay';
import DescriptionIcon from '@mui/icons-material/Description';
import statement1 from './witnessstatements/statement1.txt'


function Statements() {
    const [fileContent, setFileContent] = useState('');


    function renderRow(props) {
        const { index, style } = props;
        return (
            <ListItem style={style} key={index} component="div" disablePadding>
                <ListItemButton onClick={() => showStatement(index)}>
                    <DescriptionIcon></DescriptionIcon>
                    <ListItemText primary={` Statement ${index + 1}`} />
                </ListItemButton>
            </ListItem>
        );
    }

    function showStatement(index) {
        fetch(statement1)
            .then(r => r.text())
            .then(text => {
                setFileContent(text);
            });
    }

    const nums = 10;
    return (
        <div className="background">
        <div className="Statements">
                <div className= "foreground">
                <FixedSizeList
                    height={300}
                    width={200}
                    itemSize={46}
                    itemCount={nums}
                    overscanCount={5}
                >
                    {renderRow}
                </FixedSizeList>
                </div>
                <div className='background'>
                <FileContentDisplay content={fileContent} />
                </div>
            </div>
            </div>
    );
}

export default Statements;
