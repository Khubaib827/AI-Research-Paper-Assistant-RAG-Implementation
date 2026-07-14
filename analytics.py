from collections import Counter

class ResearchAnalytics:
    def __init__(self, documents):
        self.documents = documents
        self.texts = [doc.page_content for doc in documents]
        print(f"✅ Analytics initialized with {len(documents)} documents")
    
    def get_word_frequency(self, n=20):
        all_words = []
        for text in self.texts:
            words = text.lower().split()
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 
                         'for', 'of', 'with', 'without', 'by', 'from', 'up', 'down', 
                         'off', 'over', 'under', 'above', 'below', 'between', 'among',
                         'this', 'that', 'these', 'those', 'then', 'than', 'so', 'too',
                         'very', 'just', 'would', 'could', 'should', 'might', 'must'}
            words = [w for w in words if w.isalnum() and w not in stop_words]
            all_words.extend(words)
        word_freq = Counter(all_words)
        return word_freq.most_common(n)
    
    def get_paper_stats(self):
        stats = []
        for doc in self.documents:
            stats.append({
                "source": doc.metadata.get("source", "Unknown"),
                "pages": doc.metadata.get("pages", 0),
                "words": len(doc.page_content.split()),
                "characters": len(doc.page_content)
            })
        return stats
    
    def generate_report(self):
        stats = self.get_paper_stats()
        word_freq = self.get_word_frequency(10)
        
        total_words = sum(s['words'] for s in stats)
        
        report = f"""
📊 RESEARCH ANALYTICS REPORT
{'=' * 40}

📈 PAPER STATISTICS
- Total Papers: {len(self.documents)}
- Total Words: {total_words:,}
- Average Words per Paper: {total_words // len(self.documents) if len(self.documents) > 0 else 0:,}

🔤 TOP KEYWORDS
"""
        for word, count in word_freq:
            report += f"  - {word}: {count}\n"
        
        report += f"\n📚 PAPERS ANALYZED\n"
        for idx, stat in enumerate(stats, 1):
            report += f"  {idx}. {stat['source']}: {stat['words']:,} words, {stat['pages']} pages\n"
        
        return report
    
    def get_summary_stats(self):
        stats = self.get_paper_stats()
        return {
            "total_papers": len(self.documents),
            "total_words": sum(s['words'] for s in stats),
            "paper_sources": [s['source'] for s in stats]
        }
