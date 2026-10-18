function HowItWorks()
{
     const steps = [
    {
      number: "01",
      title: "Ask a Question",
      description:
        "The student enters a college-related question through the React chat interface.",
      technology: "React and JavaScript",
    },
    {
      number: "02",
      title: "Process the Request",
      description:
        "The Spring Boot backend receives the question and forwards it to the Python RAG API.",
      technology: "Spring Boot and REST API",
    },
    {
      number: "03",
      title: "Retrieve Relevant Information",
      description:
        "The RAG pipeline converts the question into an embedding and searches the vector database for relevant document chunks.",
      technology: "LangChain and ChromaDB",
    },
    {
      number: "04",
      title: "Generate the Answer",
      description:
        "The language model uses the retrieved document context to generate an answer relevant to the student's question.",
      technology: "LLM and Retrieved Context",
    },
    {
      number: "05",
      title: "Display the Response",
      description:
        "The generated answer returns through the backend APIs and appears in the chat interface.",
      technology: "Python Flask, Spring Boot and React",
    },
  ];

  return (
    <div className="how-it-works-page">
      <header className="how-header">
        <span className="how-eyebrow">SYSTEM WORKFLOW</span>
        <h1>How It Works</h1>
        <p>
          Understand how RAG College Assist processes questions
          and generates answers using college documents.
        </p>
      </header>

      <section className="workflow-banner">
        <h2>From Question to Answer</h2>
        <p>
          The system retrieves relevant information from college
          documents before generating a response.                        
        </p>
      </section>

      <section className="workflow-section">
        <h2>Processing Pipeline</h2>

        <div className="workflow-steps">
          {steps.map((step) => (
            <article className="workflow-step" key={step.number}>
              <div className="step-number">{step.number}</div>

              <div className="step-content">
                <h3>{step.title}</h3>
                <p>{step.description}</p>
                <span className="step-technology">
                  {step.technology}
                </span>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="rag-explanation">
        <h2>Understanding RAG</h2>

        <p>
          Retrieval-Augmented Generation combines document
          retrieval with language-model generation. First, the
          system searches for relevant information in the available
          college documents. Then, it provides the retrieved context
          to the language model to help generate a relevant answer.
        </p>

        <div className="rag-comparison">
          <div className="rag-item">
            <h3>Retrieval</h3>
            <p>
              Search college documents and identify relevant
              information.
            </p>
          </div>

          <div className="rag-item">
            <h3>Generation</h3>
            <p>
              Use the retrieved information to formulate an answer.
            </p>
          </div>
        </div>
      </section>

      <section className="workflow-note">
        <h2>Project Goal</h2>
        <p>
          Make college information easier to access by helping
          students find relevant answers without manually searching
          through lengthy documents.
        </p>
      </section>
    </div>
  );
}

export default HowItWorks