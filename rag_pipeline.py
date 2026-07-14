# rag_pipeline.py - Updated for TF-IDF
from local_llm import LocalLLM

class ResearchRAG:
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore
        self.retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        self.llm = LocalLLM()
        self.history = []
        print("✅ RAG Pipeline initialized")
    
    def get_context(self, query, k=5):
        """Get relevant context for query"""
        docs = self.retriever.get_relevant_documents(query)
        if not docs:
            return "No relevant content found."
        
        # Combine chunks with sources
        context_parts = []
        for doc in docs[:k]:
            source = doc.metadata.get('source', 'Unknown')
            text = doc.page_content[:800]  # Limit length
            context_parts.append(f"Source: {source}\n{text}")
        
        return "\n\n---\n\n".join(context_parts)
    
    def summarize(self):
        """Generate summary"""
        context = self.get_context("summary of the research paper")
        prompt = f"""Context:
{context}

Please generate a comprehensive summary of this research paper."""
        return self.llm.generate(prompt)
    
    def literature_review(self, topic):
        """Generate literature review"""
        context = self.get_context(topic)
        prompt = f"""Context:
{context}

Topic: {topic}

Please generate a literature review on the topic above."""
        return self.llm.generate(prompt)
    
    def compare_papers(self):
        """Compare papers"""
        context = self.get_context("compare research papers")
        prompt = f"""Context:
{context}

Please compare and contrast these research papers."""
        return self.llm.generate(prompt)
    
    def get_citations(self):
        """Generate citations"""
        context = self.get_context("citation")
        prompt = f"""Context:
{context}

Please generate APA citations for these papers."""
        return self.llm.generate(prompt)
    
    def ask_question(self, question):
        """Answer a question"""
        context = self.get_context(question)
        prompt = f"""Context:
{context}

Question: {question}

Please answer the question based on the research papers."""
        answer = self.llm.generate(prompt)
        
        self.history.append({
            "question": question,
            "answer": answer,
            "context": context[:500]
        })
        
        return answer