import { useState } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    const text = message.trim();

    if (!text || loading) return;

    // Add user's message
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: text,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
         method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: text,
        }),
      });

      if (!response.ok) {
        throw new Error("Backend request failed");
      }

      const data = await response.json();

      // Add LARVI's response
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.response,
          category: data.category || "GENERAL",
        },
      ]);
    } catch (error) {
      console.error("Chat error:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Sorry, I couldn't connect to LARVI right now.",
          category: "ERROR",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const useSuggestion = (text) => {
    setMessage(text);
  };

  const startNewChat = () => {
    setMessages([]);
    setMessage("");
  };

  return (
    <div className="larvi-app">

      {/* ================= SIDEBAR ================= */}

      <aside className="sidebar">

        <div className="brand">
          <div className="brand-icon">L</div>
          <span>LARVI</span>
        </div>

        <button
          className="new-chat-btn"
          onClick={startNewChat}
        >
          <span>+</span>
          New Chat
        </button>

        <div className="sidebar-section">

          <p className="section-title">
            RECENT
          </p>

          <button
            className="conversation"
            onClick={startNewChat}
          >
            <span>💬</span>
            Getting started
          </button>

          <button
            className="conversation"
            onClick={startNewChat}
          >
            <span>💬</span>
            My conversations
          </button>

        </div>

        <div className="sidebar-bottom">

          <button className="sidebar-option">
            ⚙️ Settings
          </button>

          <button className="sidebar-option">
            ❓ Help
          </button>

        </div>

      </aside>


      {/* ================= MAIN ================= */}

      <main className="main-content">


        {/* ================= TOPBAR ================= */}

        <header className="topbar">

          <div>
            <span className="status-dot"></span>

            <span className="online-text">
              LARVI is online
            </span>
          </div>

          <button className="profile-btn">

            <div className="profile-avatar">
              Y
            </div>

            <span>
              Profile
            </span>

          </button>

        </header>


        {/* ================= CHAT AREA ================= */}

        <section className="chat-area">

          {/* ================= WELCOME ================= */}

          {messages.length === 0 ? (

            <div className="welcome">

              <div className="welcome-orb">
                <span>L</span>
              </div>

              <h1>
                Hello! I'm <span>LARVI</span>.
              </h1>

              <p>
                Your intelligent AI agent. Ask me anything,
                give me a task, or tell me what you need help with.
              </p>


              {/* Suggestions */}

              <div className="suggestions">

                <button
                  onClick={() =>
                    useSuggestion(
                      "What can you help me with?"
                    )
                  }
                >

                  <strong>
                    💡 What can you do?
                  </strong>

                  <span>
                    Learn about LARVI's capabilities
                  </span>

                </button>


                <button
                  onClick={() =>
                    useSuggestion(
                      "Help me organize my day"
                    )
                  }
                >

                  <strong>
                    📅 Organize my day
                  </strong>

                  <span>
                    Plan tasks and manage your time
                  </span>

                </button>


                <button
                  onClick={() =>
                    useSuggestion(
                      "Help me write something"
                    )
                  }
                >

                  <strong>
                    ✍️ Help me write
                  </strong>

                  <span>
                    Create, edit, or improve content
                  </span>

                </button>

              </div>

            </div>

          ) : (

            /* ================= MESSAGES ================= */

            <div className="messages">

              {messages.map((msg, index) => (

                <div
                  key={index}
                  className={`message ${
                    msg.role === "user"
                      ? "user-message"
                      : "assistant-message"
                  }`}
                >

                  {/* Avatar */}

                  <div className="message-avatar">

                    {msg.role === "user"
                      ? "Y"
                      : "L"}

                  </div>


                  {/* Message */}

                  <div className="message-wrapper">

                    {/* Agent category */}

                    {msg.role === "assistant" &&
                      msg.category &&
                      msg.category !== "ERROR" && (

                        <div className="agent-category">
                          {msg.category}
                        </div>

                    )}


                    <div className="message-content">
                      {msg.content}
                    </div>

                  </div>

                </div>

              ))}


              {/* Loading */}

              {loading && (

                <div className="message assistant-message">

                  <div className="message-avatar">
                    L
                  </div>

                  <div className="message-wrapper">

                    <div className="agent-category">
                      LARVI
                    </div>

                    <div className="message-content typing">
                      LARVI is thinking...
                    </div>

                  </div>

                </div>

              )}

            </div>

          )}

        </section>


        {/* ================= INPUT ================= */}

        <div className="input-container">

          <div className="input-box">

            <button className="attach-btn">
              +
            </button>


            <input
              type="text"
              placeholder="Ask LARVI anything..."
              value={message}
              onChange={(e) =>
                setMessage(e.target.value)
              }
              onKeyDown={(e) => {

                if (e.key === "Enter") {
                  sendMessage();
                }

              }}
              disabled={loading}
            />


            <button
              className="send-btn"
              onClick={sendMessage}
              disabled={loading || !message.trim()}
            >
              ➤
            </button>

          </div>


          <p className="input-note">
            LARVI can make mistakes. Check important information.
          </p>

        </div>

      </main>

    </div>
  );
}

export default App;