
import { useState } from "react";

function InputChat({ onSend, disabled = false }) {
  const [message, setMessage] = useState("");

  function handleSubmit(event) {
    event.preventDefault();

    const question = message.trim();

    if (question === "" || disabled) {
      return;
    }

    onSend(question);
    setMessage("");
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      event.currentTarget.form.requestSubmit();
    }
  }

  return (
    <form className="chat-input-form" onSubmit={handleSubmit}>
      <textarea
        className="chat-input"
        value={message}
        onChange={(event) => setMessage(event.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask your college-related question..."
        rows={1}
        aria-label="Type your question"
        disabled={disabled}
      />

      <button
        className="chat-send-button"
        type="submit"
        disabled={!message.trim() || disabled}
        aria-label="Send question"
      >
        {disabled ? "Thinking..." : "Send"}
      </button>
    </form>
  );
}

export default InputChat;
