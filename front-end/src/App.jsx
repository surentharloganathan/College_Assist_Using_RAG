
import { useState } from "react";
import Sidebar from "./components/side_bar.jsx";
import AboutProject from "./pages/about_project.jsx";
import HowItWorks from "./pages/how_it_works.jsx";
import ChatWindow  from "./components/chat_window.jsx";

import "./App.css";

function App() {
  const [activePage, setActivePage] = useState("chat");
  const [chatResetKey, setChatResetKey] = useState(0);
  


  function handleNewChat() {
  setActivePage("chat");
  setChatResetKey((previousKey) => previousKey + 1);
}


  function handleNavigate(page) {
    setActivePage(page);
  }

  function renderPage() {
    switch (activePage) {
      case "about-project":
        return <AboutProject />;

      case "how-it-works":
        return <HowItWorks />;

      case "contact":
        return <div>Contact information will be added here.</div>;

        default:
          return <ChatWindow  resetKey = {chatResetKey}/>;
    }
  }

  return (
    <div className="app">
      <Sidebar
        onNewChat={handleNewChat}
        activePage={activePage}
        onNavigate={handleNavigate}
      />

      <main className="page-content">
        {renderPage()}
      </main>
    </div>
  );
}

export default App;
