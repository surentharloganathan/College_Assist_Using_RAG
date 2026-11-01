
import { useState, useEffect, useRef } from "react";
import SuggestQuestion from "./suggest_question.jsx";
import MessageBubble from "./message_bubble.jsx";
import InputChat from "./input_chat.jsx";

function ChatWindow({ resetKey }) {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const chatEndRef = useRef(null);

  // Clear conversation when New Chat is clicked
  useEffect(() => {
    setMessages([]);
    setIsLoading(false);
  }, [resetKey]);

  // Automatically scroll to the latest message
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth"
    });
  }, [messages, isLoading]);

  const questions = [
    "What is the IT placement percentage?",
    "Explain the IT department curriculum.",
    "What are the semester regulations?",
    "Tell me about the college placement statistics."
  ];

  async function handleSend(question) {
    if (isLoading) return;

    const userMessage = {
      id: Date.now(),
      message: question,
      sender: "user"
    };

    setMessages((previousMessages) => [
      ...previousMessages,
      userMessage
    ]);

    setIsLoading(true);

    try {
      const response = await fetch(
        "http://localhost:8080/api/ask",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            question: question
          })
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.error || "Unable to get an answer from the server."
        );
      }

      if (!data.answer) {
        throw new Error("The server returned an empty answer.");
      }

      const assistantMessage = {
        id: Date.now() + 1,
        message: data.answer,
        sender: "assistant"
      };

      setMessages((previousMessages) => [
        ...previousMessages,
        assistantMessage
      ]);

    } catch (error) {
      console.error("Chat API Error:", error);

      const errorMessage = {
        id: Date.now() + 1,
        message: `Sorry, something went wrong: ${error.message}`,
        sender: "assistant"
      };

      setMessages((previousMessages) => [
        ...previousMessages,
        errorMessage
      ]);

    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section className="chat-window">

      {messages.length === 0 ? (
        <div className="chat-welcome">
          <h1>College Assist</h1>

          <p>
            Your AI assistant for college-related questions.
          </p>

          <p className="welcome-description">
            Ask about curriculum, regulations, placements,
            and other college information.
          </p>

          <div className="suggested-questions">
            <h2>Suggested questions</h2>

            <div className="suggestion-list">
              {questions.map((question) => (
                <SuggestQuestion
                  key={question}
                  question={question}
                  onClick={handleSend}
                />
              ))}
            </div>
          </div>
        </div>
      ) : (
        <div className="chat-messages">
          {messages.map((item) => (
            <MessageBubble
              key={item.id}
              message={item.message}
              sender={item.sender}
            />
          ))}

          {isLoading && (
            <div className="assistant-loading">
              College Assist is thinking...
            </div>
          )}

          <div ref={chatEndRef} />
        </div>
      )}

      <div className="chat-input-container">
        <InputChat
          onSend={handleSend}
          disabled={isLoading}
        />
      </div>

    </section>
  );
}

export default ChatWindow;
