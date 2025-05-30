import { Link } from 'react-router-dom';
import { useAppContext } from '../../contexts/AppContext';
import './Navigation.css'; // Create this CSS file

function Navigation() {
  const context = useAppContext();
  function clearConversation() {
    context.setConversation([]);
  }

  return (
    <div>      
      <nav className="sidebar">
        <ul className="nav-list">
          <li className="nav-item">
            <Link to="/" className="nav-link">דבר עם המורה</Link>
          </li>
          <li className="nav-item">
            <Link to="/memory" className="nav-link">זיכרון</Link>
          </li>
        </ul>
      </nav>
      <button onClick={clearConversation} className='clear-button nav-link'>מחק</button>
    </div>
  );
}

export default Navigation;