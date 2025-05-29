import { Link } from 'react-router-dom';
import './Navigation.css'; // Create this CSS file

function Navigation() {
  return (
    <nav className="sidebar">
      <ul className="nav-list">
        <li className="nav-item">
          <Link to="/" className="nav-link">Talk to the Teacher</Link>
        </li>
        <li className="nav-item">
          <Link to="/memory" className="nav-link">Memory</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navigation;