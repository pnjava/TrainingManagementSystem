import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './auth/AuthContext';
import { NavBar } from './components/NavBar';
import PublicHome from './pages/PublicHome';
import { TrainerHome } from './pages/TrainerHome';
import { AdminHome } from './pages/AdminHome';

const App = () => (
  <AuthProvider>
    <BrowserRouter>
      <NavBar />
      <Routes>
        <Route path="/" element={<PublicHome />} />
        <Route path="/trainer" element={<TrainerHome />} />
        <Route path="/admin" element={<AdminHome />} />
      </Routes>
    </BrowserRouter>
  </AuthProvider>
);

export default App;
