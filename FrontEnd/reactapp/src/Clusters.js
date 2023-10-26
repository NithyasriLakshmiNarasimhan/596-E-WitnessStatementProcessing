import './App.css';

function Clusters() {
    return (
        <div className="Clusters">
            <header className="App-header">
                
                    <p>
                        This is the page to view clusters. We will add stuff later.
                    </p>
             
            </header>
        </div>
    );
}

export default Clusters;




// import { useState } from 'react'
// import axios from "axios";
// import logo from './logo.svg';
// import './App.css';

// function Clusters() {

//     // new line start
//     const [profileData, setProfileData] = useState(null)

//     function getData() {
//         axios({
//             method: "GET",
//             url: "/QandA",
//         })
//             .then((response) => {
//                 const res = response.data
//                 alert(res);
//                 // setProfileData(({
//                 //     profile_name: res.name,
//                 //     about_me: res.about
//                 // }))
//             }).catch((error) => {
//                 if (error.response) {
//                     console.log(error.response)
//                     console.log(error.response.status)
//                     console.log(error.response.headers)
//                 }
//             })
//     }

//     function sendData(){
//         axios({
//             method: "POST",
//             url: "/QandA",
//             data: {
//                 statement: "Statement 1: My name is Amanda Wells.On Tuesday afternoon around 3: 30pm, I was walking my dog in the park when I heard a child scream.I looked over and saw a man grabbing a young boy who looked about 10 years old.The boy was yelling Help, help! but the man put his hand over the boy's mouth and dragged him towards a white van. He forced the boy into the side door of the van and then got into the driver's seat and quickly drove off.I immediately called 911 to report what I saw.I really hope they find that poor boy."}
            
//             })
//             .then((response) => {
//                 const res = response.data
//                 alert(res.statement);
//                 // setProfileData(({
//                 //     profile_name: res.name,
//                 //     about_me: res.about
//                 // }))
//             }).catch((error) => {
//                 if (error.response) {
//                     console.log(error.response)
//                     console.log(error.response.status)
//                     console.log(error.response.headers)
//                 }
//             })
//     }
    
//     //end of new line 

//     return (
//         <div className="App">
//             <header className="App-header">
//                 <img src={logo} className="App-logo" alt="logo" />
//                 <p>
//                     Edit <code>src/App.js</code> and save to reload.
//                 </p>
//                 <a
//                     className="App-link"
//                     href="https://reactjs.org"
//                     target="_blank"
//                     rel="noopener noreferrer"
//                 >
//                     Learn React
//                 </a>

//                 {/* new line start*/}
//                 <p>To get your profile details: </p><button onClick={sendData}>Click me</button>
//                 {profileData && <div>
//                     <p>Profile name: {profileData.profile_name}</p>
//                     <p>About me: {profileData.about_me}</p>
//                 </div>
//                 }
//                 {/* end of new line */}
//             </header>
//         </div>
//     );
// }

// export default Clusters;
