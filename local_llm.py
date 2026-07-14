# local_llm.py - Simple rule-based generation
import random
import re

class LocalLLM:
    def __init__(self):
        print("🔄 Initializing Local LLM...")
        self.available = True
        print("✅ Local LLM ready")
    
    def generate(self, prompt, max_length=512):
        """Generate response using simple NLP"""
        try:
            # Extract key information from prompt
            if "summary" in prompt.lower():
                return self._generate_summary(prompt)
            elif "literature review" in prompt.lower():
                return self._generate_literature_review(prompt)
            elif "compare" in prompt.lower():
                return self._generate_comparison(prompt)
            elif "citation" in prompt.lower():
                return self._generate_citations(prompt)
            elif "question" in prompt.lower() or "?" in prompt:
                return self._answer_question(prompt)
            else:
                return self._generate_general(prompt)
        
        except Exception as e:
            return f"❌ Error: {e}"
    
    def _generate_summary(self, prompt):
        # Extract context
        context = self._extract_context(prompt)
        
        if not context:
            return "No content found to summarize."
        
        # Simple summary generation
        sentences = re.split(r'[.!?]+', context)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if len(sentences) < 3:
            return context[:500] + "..."
        
        # Create structured summary
        summary = f"""
### 📝 Summary

**Overview:**
{sentences[0]}

**Key Findings:**
- {sentences[1] if len(sentences) > 1 else 'Key findings not available'}
- {sentences[2] if len(sentences) > 2 else 'Additional findings not available'}

**Conclusion:**
{sentences[-1]}

*Note: This is an AI-generated summary based on the provided text.*
"""
        return summary
    
    def _generate_literature_review(self, prompt):
        context = self._extract_context(prompt)
        
        if not context:
            return "No content found for literature review."
        
        sentences = re.split(r'[.!?]+', context)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        review = f"""
### 📚 Literature Review

**Introduction:**
{sentences[0] if sentences else 'Introduction not available'}

**Theoretical Framework:**
- Based on the research, key theoretical perspectives are discussed

**Methodological Approaches:**
- Various methods are employed in the research
- {sentences[1] if len(sentences) > 1 else 'Methodology details not available'}

**Key Findings:**
{sentences[2] if len(sentences) > 2 else 'Findings not available'}

**Future Directions:**
- Further research is needed in this area
- {sentences[-1] if sentences else 'Additional research suggested'}

*Note: This is an AI-generated literature review.*
"""
        return review
    
    def _generate_comparison(self, prompt):
        context = self._extract_context(prompt)
        
        if not context:
            return "No content found for comparison."
        
        sentences = re.split(r'[.!?]+', context)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        comparison = f"""
### ⚖️ Paper Comparison

**Similarities:**
- Research objectives align with current trends
- {sentences[0] if sentences else 'Similarities not available'}

**Differences:**
- Methodological approaches vary
- {sentences[1] if len(sentences) > 1 else 'Differences not available'}

**Strengths:**
- {sentences[2] if len(sentences) > 2 else 'Strengths not available'}

**Weaknesses:**
- {sentences[3] if len(sentences) > 3 else 'Weaknesses not available'}

*Note: This is an AI-generated comparison.*
"""
        return comparison
    
    def _generate_citations(self, prompt):
        context = self._extract_context(prompt)
        
        citations = """
### 📖 Citations (APA 7th Edition)

1. **Paper 1**: Author, A. A. (2020). Title of the paper. *Journal Name, Volume*(Issue), pages. DOI: 10.xxxx/xxxx

2. **Paper 2**: Author, B. B., & Author, C. C. (2021). Title of the research. *Journal Name, Volume*(Issue), pages. DOI: 10.xxxx/xxxx

3. **Paper 3**: Author, D. D. (2022). Title of the study. *Journal Name, Volume*(Issue), pages. DOI: 10.xxxx/xxxx

*Note: Please verify the actual authors, titles, and publication details from the original papers.*
"""
        return citations
    
    def _answer_question(self, prompt):
        context = self._extract_context(prompt)
        
        # Extract question
        question_match = re.search(r'Question:\s*(.+?)(?:\n|$)', prompt)
        if question_match:
            question = question_match.group(1).strip()
        else:
            question = "the question"
        
        if not context:
            return f"❌ I couldn't find information to answer your question about '{question}'."
        
        sentences = re.split(r'[.!?]+', context)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        answer = f"""
### 💬 Answer

**Question:** {question}

**Answer:**
Based on the research papers analyzed:

{sentences[0] if sentences else 'Answer not available'}

{sentences[1] if len(sentences) > 1 else ''}

**Confidence Level:** Medium

*Note: This answer is based on the provided research papers.*
"""
        return answer
    
    def _generate_general(self, prompt):
        context = self._extract_context(prompt)
        
        if not context:
            return "No content found. Please upload research papers first."
        
        sentences = re.split(r'[.!?]+', context)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 30][:5]
        
        response = "Based on the research papers:\n\n"
        for i, s in enumerate(sentences, 1):
            response += f"{i}. {s}.\n"
        
        return response
    
    def _extract_context(self, prompt):
        """Extract context from prompt"""
        # Look for context between markers
        context_match = re.search(r'context:\s*(.+?)(?:\n\n|$)', prompt, re.IGNORECASE)
        if context_match:
            return context_match.group(1).strip()
        
        # Look for content after common keywords
        for keyword in ['context', 'papers:', 'content:', 'text:']:
            match = re.search(f'{keyword}\\s*(.+?)(?:\n\n|$)', prompt, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Return the prompt itself
        return prompt