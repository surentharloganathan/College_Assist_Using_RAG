function AboutProject()
    {

        return(
        <div className="about-project-page">
            <header className="about-project-header">
                <span className="page-eyebrow">PROJECT OVERVIEW</span>

                <h1>About RAG College Assist</h1>

                <p>
                    our intelligent college assistant, designed to make
                    college information easier to find and understand.
                </p>
            </header>

            <section className="project-intro">
               
                <div>
                <h2>What is this project?</h2>

                <p>
                    RAG College Assist is an AI-powered question-answering
                    system that helps students find relevant information
                    from college documents. Instead of manually searching
                    through lengthy PDFs, students can ask questions in
                    natural language and receive useful answers based on
                    the available documents.
                </p>
                </div>
            </section>

            <section className="project-section">
                <h2>What can it do?</h2>

                <div className="feature-grid">
                <article className="feature-card">
                   
                    <h3>Ask Questions</h3>
                    <p>
                    Ask college-related questions using simple,
                    natural language.
                    </p>
                </article>

                <article className="feature-card">
                 
                    <h3>Find Information</h3>
                    <p>
                    Retrieve relevant information from indexed
                    college documents.
                    </p>
                </article>

                <article className="feature-card">
                 
                    <h3>AI-Powered Answers</h3>
                    <p>
                    Generate readable answers using retrieved
                    information and a language model.
                    </p>
                </article>

                <article className="feature-card">
                 
                    <h3>Save Time</h3>
                    <p>
                    Reduce the effort needed to search lengthy
                    documents manually.
                    </p>
                </article>
                </div>
            </section>

            <section className="project-section technology-section">
                <h2>Technology Stack</h2>

                <p className="section-description">
                The project combines a modern web interface with
                backend services and a retrieval-augmented AI pipeline.
                </p>

                <div className="technology-list">
                <span className="technology-tag">React</span>
                <span className="technology-tag">JavaScript</span>
                <span className="technology-tag">Spring Boot</span>
                <span className="technology-tag">Python Flask</span>
                <span className="technology-tag">LangChain</span>
                <span className="technology-tag">ChromaDB</span>
                <span className="technology-tag">Sentence Transformers</span>
                <span className="technology-tag">LLM Integration</span>
                </div>
            </section>

            <section className="project-note">
                <h2>Our Goal</h2>
                <p>
                Make college information more accessible by combining
                document retrieval with AI, helping students find
                relevant answers with less effort.
                </p>
            </section>
    </div>
        )

}
    
export default AboutProject