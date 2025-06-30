import { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../auth/AuthContext';

export const NavBar = () => {
  const { login } = useContext(AuthContext);
  return (
    <nav style={{ padding: '1rem', background: '#eee' }}>
      <Link to="/">Home</Link> | <Link to="/trainer">Trainer</Link> |{' '}
      <Link to="/admin">Admin</Link>
      <span style={{ marginLeft: '1rem' }}>
        <button onClick={() => login('Trainer')}>Trainer</button>
        <button onClick={() => login('Admin')}>Admin</button>
        <button onClick={() => login('Public')}>Logout</button>
      </span>
    </nav>
  );
};
