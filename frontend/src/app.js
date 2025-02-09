import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import axios from "axios";

const Home = ({ userData, financialData }) => {
  return (
    <div>
      <h1>Welcome, {userData.username}!</h1>
      <p>Level: {userData.level} | Challenges Completed: {userData.challenges_completed}</p>
      <h2>Financial Data</h2>
      <p>BTC Price: {financialData.btc_price} USD</p>
      <p>Stock Price (AAPL): {financialData.stock_price} USD</p>
    </div>
  );
};

const BalanceSheetChallenge = () => (
  <div>
    <h2>Balance Sheet Challenge</h2>
    <p>This is the Balance Sheet Challenge page.</p>
  </div>
);

const EbitdaSpeedRun = () => (
  <div>
    <h2>EBITDA Speed Run</h2>
    <p>This is the EBITDA Speed Run page.</p>
  </div>
);

const HorizontalAnalysis = () => (
  <div>
    <h2>Horizontal Analysis Battle</h2>
    <p>This is the Horizontal Analysis Battle page.</p>
  </div>
);

const CompanyFaceOff = () => (
  <div>
    <h2>Company Face-Off</h2>
    <p>This is the Company Face-Off page.</p>
  </div>
);

const App = () => {
  const [userData, setUserData] = useState(null);
  const [financialData, setFinancialData] = useState(null);

  useEffect(() => {
    // Fetch user data
    axios.get("/api/user")
      .then((response) => {
        setUserData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching user data:", error);
      });

    // Fetch financial data
    axios.get("/api/financial-data?symbol=AAPL")
      .then((response) => {
        setFinancialData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching financial data:", error);
      });
  }, []);

  return (
    <Router>
      <nav>
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/balance-sheet">Balance Sheet Challenge</Link></li>
          <li><Link to="/ebitda-speed-run">EBITDA Speed Run</Link></li>
          <li><Link to="/horizontal-analysis">Horizontal Analysis Battle</Link></li>
          <li><Link to="/company-face-off">Company Face-Off</Link></li>
        </ul>
      </nav>

      <Routes>
        <Route
          path="/"
          element={userData && financialData ? <Home userData={userData} financialData={financialData} /> : <p>Loading...</p>}
        />
        <Route path="/balance-sheet" element={<BalanceSheetChallenge />} />
        <Route path="/ebitda-speed-run" element={<EbitdaSpeedRun />} />
        <Route path="/horizontal-analysis" element={<HorizontalAnalysis />} />
        <Route path="/company-face-off" element={<CompanyFaceOff />} />
      </Routes>
    </Router>
  );
};

export default App;
