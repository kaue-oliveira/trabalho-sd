import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import PublicHome from './pages/PublicHome';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<PublicHome />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;