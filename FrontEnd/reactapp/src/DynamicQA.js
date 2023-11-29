// // import React, { useState } from 'react';
// // import './Statements.css';
// // import { usePromiseTracker } from "react-promise-tracker";
// // import { TailSpin } from "react-loader-spinner";
// // // import CaseList from './CaseList'
// // import Box from '@mui/material/Box';
// // import List from '@mui/material/List';
// // import ListItemButton from '@mui/material/ListItemButton';
// // import ListItemIcon from '@mui/material/ListItemIcon';
// // import ListItemText from '@mui/material/ListItemText';
// // import FolderIcon from '@mui/icons-material/Folder';
// // import DriveFolderUploadIcon from '@mui/icons-material/DriveFolderUpload';
// // import axios from "axios";

// // import { trackPromise } from 'react-promise-tracker';

// // const LoadingIndicator = props => {
        
// //     const { promiseInProgress } = usePromiseTracker();
// //     return (
// //         promiseInProgress &&
// //         <div>
// //             <TailSpin color="green" radius={"2px"} />
// //         </div >
// //     );
// // }



// // function DynamicQA() {
// //     const [text, setText] = useState('');
// //     const [question, setQuestion] = useState('');
// //     const [response, setResponse] = useState('');

// //     const handleSubmit = () => {
// //         trackPromise(
// //             axios({
// //                 method: "POST",
// //                 url: "/process_text",
// //                 data: {
// //                     text: text,
// //                     question: question
// //                 }
// //             })
// //             .then((response) => {
// //                 const res = response.data
// //                 setResponse("response:\n" + res);
// //             }).catch((error) => {
// //                 if (error.response) {
// //                     console.log(error.response)
// //                     console.log(error.response.status)
// //                     console.log(error.response.headers)
// //                 }
// //             })
// //         );
// //     };

// //     return (
// //         <div className="DynamicQA">
// //             <header className="App-header">
// //                 <div>
// //                 <label htmlFor="userTextInput">Enter Case Number    </label>
// //                     <input 
// //                         type="text" 
// //                         value={text} 
// //                         onChange={(e) => setText(e.target.value)} 
// //                     />
// //                     <br />
// //                 <label htmlFor="userTextInput">Enter your Question    </label>
// //                     <input 
// //                         type="question" 
// //                         value={question} 
// //                         onChange={(e) => setQuestion(e.target.value)} 
// //                     />

// // <br />
// //                     <button onClick={handleSubmit}>Submit</button>
// //                     <p>{response}</p>
// //                 </div>
// //             </header>
// //         </div>
// //     );
// // }

// // export default DynamicQA;




// import React, { useState } from 'react';
// import axios from "axios";
// import { trackPromise } from 'react-promise-tracker';
// import { usePromiseTracker } from "react-promise-tracker";
// import { TailSpin } from "react-loader-spinner";
// import './Statements.css';
// import Box from '@mui/material/Box';
// import List from '@mui/material/List';
// import ListItemButton from '@mui/material/ListItemButton';
// import ListItemIcon from '@mui/material/ListItemIcon';
// import ListItemText from '@mui/material/ListItemText';
// import FolderIcon from '@mui/icons-material/Folder';
// import DriveFolderUploadIcon from '@mui/icons-material/DriveFolderUpload';

// const LoadingIndicator = () => {
//     const { promiseInProgress } = usePromiseTracker();
//     return promiseInProgress && (
//         <div className="loader">
//             <TailSpin color="green" radius={"2px"} />
//         </div>
//     );
// };

// const DynamicQA = () => {
//     const [text, setText] = useState('');
//     const [question, setQuestion] = useState('');
//     const [response, setResponse] = useState('');

//     const handleSubmit = async () => {
//         try {
//             const response = await trackPromise(axios.post("/process_text", { text, question }));
//             setResponse(`response:\n${response.data}`);
//         } catch (error) {
//             // Handle errors here
//             console.error('An error occurred:', error);
//         }
//     };

//     return (
//         <div className="DynamicQA">
//             <header className="App-header">
//                 <div>
//                     <label htmlFor="userTextInput">Enter Case Number</label>
//                     <input 
//                         type="text" 
//                         value={text} 
//                         onChange={(e) => setText(e.target.value)}
//                     />
//                     <br />
//                     <label htmlFor="userQuestionInput">Enter your Question</label>
//                     <input 
//                         type="text" 
//                         value={question} 
//                         onChange={(e) => setQuestion(e.target.value)}
//                     />
//                     <br />
//                     <button onClick={handleSubmit}>Submit</button>
//                     <p>{response}</p>
//                 </div>
//             </header>
//         </div>
//     );
// };

// export default DynamicQA;



import React, { useState } from 'react';
import './Statements.css';
import { usePromiseTracker } from "react-promise-tracker";
import { TailSpin } from "react-loader-spinner";
import { Box, TextField, Button, Typography, CircularProgress } from '@mui/material';

import axios from "axios";
import { trackPromise } from 'react-promise-tracker';

const LoadingIndicator = () => {    
    const { promiseInProgress } = usePromiseTracker();
    return (
        promiseInProgress && <CircularProgress color="primary" />
    );
}

function DynamicQA() {
    const [text, setText] = useState('');
    const [question, setQuestion] = useState('');
    const [response, setResponse] = useState('');

    const handleSubmit = () => {
        trackPromise(
            axios.post("/process_text", { text, question })
                .then((response) => setResponse("response:\n" + response.data))
                .catch((error) => console.error('Error:', error))
        );
    };

    return (
        <Box className="DynamicQA" sx={{ padding: 3 }}>
            <Typography variant="h4" gutterBottom>
                Dynamic Q&A
            </Typography>
            <TextField 
                label="Enter Case Number" 
                variant="outlined" 
                value={text} 
                onChange={(e) => setText(e.target.value)} 
                fullWidth 
                margin="normal"
            />
            <TextField 
                label="Enter your Question" 
                variant="outlined" 
                value={question} 
                onChange={(e) => setQuestion(e.target.value)} 
                fullWidth 
                margin="normal"
            />
            <Button variant="contained" color="primary" onClick={handleSubmit}>
                Submit
            </Button>
            <Typography variant="body1" sx={{ marginTop: 2 }}>
                {response}
            </Typography>
            <LoadingIndicator />
        </Box>
    );
}

export default DynamicQA;

