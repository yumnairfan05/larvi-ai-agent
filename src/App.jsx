import { useEffect, useRef, useState } from "react";
import "./App.css";

const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const STORAGE_KEY = "larvi_conversations";

function App() {
  const [message, setMessage] = useState("");
  const [conversations, setConversations] = useState([]);
  const [activeChatId, setActiveChatId] = useState(null);
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // =========================================================
  // LOAD SAVED CONVERSATIONS
  // =========================================================

  useEffect(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);

      if (saved) {
        const parsed = JSON.parse(saved);

        if (Array.isArray(parsed)) {
          setConversations(parsed);

          if (parsed.length > 0) {
            setActiveChatId(parsed[0].id);
          }
        }
      }
    } catch (error) {
      console.error("Could not load conversations:", error);
    }

    inputRef.current?.focus();
  }, []);

  // =========================================================
  // SAVE CONVERSATIONS
  // =========================================================

  useEffect(() => {
    try {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify(conversations)
      );
    } catch (error) {
      console.error("Could not save conversations:", error);
    }
  }, [conversations]);

  // =========================================================
  // AUTO SCROLL
  // =========================================================

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [conversations, activeChatId, loading]);

  // =========================================================
  // CURRENT CHAT
  // =========================================================

  const activeConversation = conversations.find(
    (conversation) => conversation.id === activeChatId
  );

  const messages = activeConversation?.messages || [];

  // =========================================================
  // CREATE NEW CHAT
  // =========================================================

  const startNewChat = () => {
    setActiveChatId(null);
    setMessage("");

    setTimeout(() => {
      inputRef.current?.focus();
    }, 100);
  };

  // =========================================================
  // CREATE CONVERSATION
  // =========================================================

  const createConversation = (firstMessage) => {
    const newConversation = {
      id: Date.now().toString(),

      title:
        firstMessage.length > 32
          ? firstMessage.substring(0, 32) + "..."
          : firstMessage,

      messages: [],

      createdAt: new Date().toISOString(),

      updatedAt: new Date().toISOString(),
    };

    setConversations((prev) => [
      newConversation,
      ...prev,
    ]);

    setActiveChatId(newConversation.id);

    return newConversation.id;
  };

  // =========================================================
  // ADD MESSAGE TO CONVERSATION
  // =========================================================

  const addMessageToConversation = (
    chatId,
    newMessage
  ) => {
    setConversations((prev) =>
      prev.map((conversation) => {
        if (conversation.id !== chatId) {
          return conversation;
        }

        return {
          ...conversation,

          messages: [
            ...conversation.messages,
            newMessage,
          ],

          updatedAt: new Date().toISOString(),
        };
      })
    );
  };

  // =========================================================
  // SEND MESSAGE
  // =========================================================

  const sendMessage = async () => {
    const text = message.trim();

    if (!text || loading) return;

    let chatId = activeChatId;

    // Create chat if this is the first message
    if (!chatId) {
      chatId = createConversation(text);
    }

    // Add user message
    addMessageToConversation(chatId, {
      role: "user",
      content: text,
    });

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
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

      addMessageToConversation(chatId, {
        role: "assistant",

        content:
          data.response ||
          "I received your request, but no response was returned.",

        category:
          data.category || "GENERAL",
      });
    } catch (error) {
      console.error("Chat error:", error);

      addMessageToConversation(chatId, {
        role: "assistant",

        content:
          "Sorry, I couldn't connect to LARVI right now. Please make sure the LARVI backend is running.",

        category: "ERROR",
      });
    } finally {
      setLoading(false);

      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
    }
  };

  // =========================================================
  // SELECT CHAT
  // =========================================================

  const selectConversation = (id) => {
    if (loading) return;

    setActiveChatId(id);
    setMessage("");

    setTimeout(() => {
      inputRef.current?.focus();
    }, 100);
  };

  // =========================================================
  // DELETE CHAT
  // =========================================================

  const deleteConversation = (id, e) => {
    e.stopPropagation();

    if (loading) return;

    setConversations((prev) =>
      prev.filter(
        (conversation) =>
          conversation.id !== id
      )
    );

    if (activeChatId === id) {
      const remaining = conversations.filter(
        (conversation) =>
          conversation.id !== id
      );

      if (remaining.length > 0) {
        setActiveChatId(remaining[0].id);
      } else {
        setActiveChatId(null);
      }
    }
  };

  // =========================================================
  // SUGGESTION
  // =========================================================

  const useSuggestion = (text) => {
    setMessage(text);

    setTimeout(() => {
      inputRef.current?.focus();
    }, 50);
  };

  // =========================================================
  // KEYBOARD
  // =========================================================

  const handleKeyDown = (e) => {
    if (
      e.key === "Enter" &&
      !e.shiftKey
    ) {
      e.preventDefault();

      sendMessage();
    }
  };

  // =========================================================
  // FORMAT CHAT DATE
  // =========================================================

  const formatDate = (dateString) => {
    const date = new Date(dateString);

    const now = new Date();

    const isToday =
      date.toDateString() ===
      now.toDateString();

    if (isToday) {
      return date.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });
    }

    return date.toLocaleDateString([], {
      month: "short",
      day: "numeric",
    });
  };

  // =========================================================
  // RENDER
  // =========================================================

  return (
    <div className="larvi-app">

      {/* ================================================= */}
      {/* SIDEBAR */}
      {/* ================================================= */}

      <aside className="sidebar">

        {/* BRAND */}

        <div className="brand">

          <div className="brand-icon">
            L
          </div>

          <span>
            LARVI
          </span>

        </div>


        {/* NEW CHAT */}

        <button
          className="new-chat-btn"
          onClick={startNewChat}
        >
          <span>＋</span>

          New Chat
        </button>


        {/* CONVERSATIONS */}

        <div className="sidebar-section">

          <p className="section-title">
            CONVERSATIONS
          </p>


          {conversations.length === 0 ? (

            <div className="empty-history">
              Your conversations
              will appear here.
            </div>

          ) : (

            <div className="conversation-list">

              {conversations.map(
                (conversation) => (

                  <button
                    key={conversation.id}
                    className={`conversation ${
                      activeChatId ===
                      conversation.id
                        ? "active-conversation"
                        : ""
                    }`}
                    onClick={() =>
                      selectConversation(
                        conversation.id
                      )
                    }
                  >

                    <span className="conversation-icon">
                      💬
                    </span>


                    <span className="conversation-info">

                      <span className="conversation-title">
                        {conversation.title}
                      </span>

                      <span className="conversation-date">
                        {formatDate(
                          conversation.updatedAt
                        )}
                      </span>

                    </span>


                    <span
                      className="delete-chat"
                      onClick={(e) =>
                        deleteConversation(
                          conversation.id,
                          e
                        )
                      }
                      title="Delete conversation"
                    >
                      ×
                    </span>

                  </button>

                )
              )}

            </div>

          )}

        </div>


        {/* SIDEBAR BOTTOM */}

        <div className="sidebar-bottom">

          <button className="sidebar-option">
            <span>⚙️</span>
            Settings
          </button>

          <button className="sidebar-option">
            <span>❓</span>
            Help
          </button>

        </div>

      </aside>


      {/* ================================================= */}
      {/* MAIN */}
      {/* ================================================= */}

      <main className="main-content">

        {/* TOPBAR */}

        <header className="topbar">

          <div className="connection-status">

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


        {/* ================================================= */}
        {/* CHAT */}
        {/* ================================================= */}

        <section className="chat-area">

          {messages.length === 0 ? (

            <div className="welcome">

              <div className="welcome-orb">
                <span>L</span>
              </div>


              <p className="welcome-label">
                YOUR AI ASSISTANT
              </p>


              <h1>
                Hello! I'm{" "}
                <span>LARVI</span>.
              </h1>


              <p className="welcome-description">
                Your intelligent AI agent for
                managing emails, calendars,
                tasks, and everyday work.
              </p>


              {/* SUGGESTIONS */}

              <div className="suggestions">

                <button
                  onClick={() =>
                    useSuggestion(
                      "What can you help me with?"
                    )
                  }
                >

                  <div className="suggestion-icon">
                    💡
                  </div>

                  <div>

                    <strong>
                      What can you do?
                    </strong>

                    <span>
                      Explore LARVI's capabilities
                    </span>

                  </div>

                </button>


                <button
                  onClick={() =>
                    useSuggestion(
                      "Show my unread emails"
                    )
                  }
                >

                  <div className="suggestion-icon">
                    📧
                  </div>

                  <div>

                    <strong>
                      Check my emails
                    </strong>

                    <span>
                      See your unread messages
                    </span>

                  </div>

                </button>


                <button
                  onClick={() =>
                    useSuggestion(
                      "What events do I have today?"
                    )
                  }
                >

                  <div className="suggestion-icon">
                    📅
                  </div>

                  <div>

                    <strong>
                      Check my calendar
                    </strong>

                    <span>
                      See today's schedule
                    </span>

                  </div>

                </button>

              </div>

            </div>

          ) : (

            <div className="messages">

              {messages.map(
                (msg, index) => (

                  <div
                    key={index}
                    className={`message ${
                      msg.role === "user"
                        ? "user-message"
                        : "assistant-message"
                    }`}
                  >

                    <div className="message-avatar">
                      {msg.role === "user"
                        ? "Y"
                        : "L"}
                    </div>


                    <div className="message-wrapper">

                      {msg.role ===
                        "assistant" &&
                        msg.category &&
                        msg.category !==
                          "ERROR" && (

                          <div className="agent-category">
                            {msg.category}
                          </div>

                      )}


                      <div className="message-content">
                        {msg.content}
                      </div>

                    </div>

                  </div>

                )
              )}


              {/* TYPING */}

              {loading && (

                <div className="message assistant-message">

                  <div className="message-avatar">
                    L
                  </div>

                  <div className="message-wrapper">

                    <div className="agent-category">
                      LARVI
                    </div>

                    <div className="typing-box">

                      <span className="typing-dot"></span>

                      <span className="typing-dot"></span>

                      <span className="typing-dot"></span>

                      <span className="typing-text">
                        LARVI is thinking
                      </span>

                    </div>

                  </div>

                </div>

              )}


              <div ref={messagesEndRef} />

            </div>

          )}

        </section>


        {/* ================================================= */}
        {/* INPUT */}
        {/* ================================================= */}

        <div className="input-container">

          <div className="input-box">

            <button
              className="attach-btn"
              type="button"
              title="More options"
            >
              ＋
            </button>


            <input
              ref={inputRef}
              type="text"
              placeholder="Ask LARVI anything..."
              value={message}
              onChange={(e) =>
                setMessage(e.target.value)
              }
              onKeyDown={handleKeyDown}
              disabled={loading}
            />


            <button
              className="send-btn"
              onClick={sendMessage}
              disabled={
                loading ||
                !message.trim()
              }
              title="Send message"
            >
              ➤
            </button>

          </div>


          <p className="input-note">
            Press Enter to send • Shift +
            Enter for a new line
          </p>

        </div>

      </main>

    </div>
  );
}

export default App;
