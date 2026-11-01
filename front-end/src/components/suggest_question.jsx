
function SuggestQuestion({ question, onClick }) {
  return (
    <button
      className="suggest-question"
      onClick={() => onClick(question)}
    >
      {question}
    </button>
  );
}

export default SuggestQuestion;
