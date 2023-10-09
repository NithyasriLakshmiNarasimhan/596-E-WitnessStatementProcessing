import { Routes, Route, useNavigate } from 'react-router-dom';
import Analyze from "./Analyze"
import Statements from "./Statements"
import Clusters from "./Clusters"
export default function App() {
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
    navigate('/');
  };

  return (
    <div>
      <div>
        <button onClick={navigateHome}>Home</button>
        <button onClick={navigateToAnalyze}>Analyze</button>
        <button onClick={navigateToClusters}>Clusters</button>
        <button onClick={navigateToStatements}>Statements</button>

        <Routes>
          <Route path="/Analyze" element={<Analyze />} />
          <Route path="/Clusters" element={<Clusters />} />
          <Route path="/Statements" element={<Statements />} />

          <Route path="/" element={<Home />} />
        </Routes>
      </div>
    </div>
  );
}

function Home() {
  return (
    <div className="Home">
      <header className="App-header">
        <div style={{
          backgroundColor: 'green'
        }}>
          <p>
            This is the the home page. We will add stuff later.
          </p>
        </div>
      </header>
    </div>
  ); }

