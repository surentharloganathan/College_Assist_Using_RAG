
function MessageBubble({ message, sender }) {
  const isUser = sender === "user";

  return (
    <div
      className={`message-row ${isUser ? "user-row" : "assistant-row"}`}
    >
      <div
        className={`message-bubble ${isUser ? "user-bubble" : "assistant-bubble"}`}
      >
        {message}
      </div>
    </div>
  );
}

export default MessageBubble;
