import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Monitoring from './pages/Monitoring';
import ModelStats from './pages/ModelStats';
import DataLineage from './pages/DataLineage';
import Alerts from './pages/Alerts';

const App: React.FC = () => {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Monitoring />} />
          <Route path="/stats" element={<ModelStats />} />
          <Route path="/data" element={<DataLineage />} />
          <Route path="/alerts" element={<Alerts />} />
        </Routes>
      </Layout>
    </Router>
  );
};

export default App;
