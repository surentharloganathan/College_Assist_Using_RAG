
function Sidebar({onNewChat,activePage, onNavigate}){
      const navigationItems = [
    { id: "about-project", label: "About Project", icon: "📘" },
    { id: "how-it-works", label: "How It Works", icon: "⚙️" },
    
   
  ];
    return (
     <div>   
    <aside className="sidebar">
      <button className="new-chat-btn" onClick={onNewChat}>
        <span>＋</span>
        New Chat
      </button>

      <div className="sidebar-group">
        <p className="sidebar-heading">WORKSPACE</p>

        <button
          className={`sidebar-item ${
            activePage === "chat" ? "active" : ""
          }`}
          onClick={() => onNavigate("chat")}
        >
          <span className="sidebar-icon">💬</span>
          Chat
        </button>
      </div>

      <div className="sidebar-group">
        <p className="sidebar-heading">INFORMATION</p>

        {navigationItems.map((item) => (
          <button
            key={item.id}
            className={`sidebar-item ${
              activePage === item.id ? "active" : ""
            }`}
            onClick={() => onNavigate(item.id)}
          >
            <span className="sidebar-icon">{item.icon}</span>
            {item.label}
          </button>
        ))}
      </div>


<div className="sidebar-bottom">
  <div className="profile-avatar">S</div>

  <div className="profile-details">
    <strong style={{ color: "white" }}>Developed By</strong>
    <span>Surenthar</span>

    <div className="sidebar-social-links">
      <a
        href="https://www.linkedin.com/in/surenthar-l-367b51323/"
        target="_blank"
        rel="noopener noreferrer"
      >
        LinkedIn
      </a>

      <a
        href="https://github.com/surentharloganathan"
        target="_blank"
        rel="noopener noreferrer"
      >
        GitHub
      </a>
    </div>
  </div>
</div>
</aside>


  </div>      
 ); 

}

export default Sidebar;
