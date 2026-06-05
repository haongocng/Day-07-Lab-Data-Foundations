import os
import glob
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from src.chunking import SentenceChunker, _dot
from src.embeddings import _mock_embed
from src.store import EmbeddingStore
from src.models import Document

def main():
    print("# Đánh giá Benchmark trên dữ liệu Luật Giao thông\n")
    data_dir = "data/Data_Law_Transportation"
    files = glob.glob(os.path.join(data_dir, "*.md"))
    
    if not files:
        print("Không tìm thấy file .md nào!")
        return
        
    doc_texts, doc_names = [], []
    for fp in files:
        with open(fp, "r", encoding="utf-8") as f:
            doc_texts.append(f.read())
            doc_names.append(os.path.basename(fp).replace('.md', ''))
            
    print(f"✅ Đã load {len(files)} tài liệu.\n")
    
    store = EmbeddingStore("eval_store")
    chunker = SentenceChunker(max_sentences_per_chunk=3)
    
    docs = []
    print("⏳ Đang cắt văn bản (SentenceChunker) và nạp vào Vector DB...")
    for i, text in enumerate(doc_texts):
        chunks = chunker.chunk(text)
        for j, c in enumerate(chunks):
            docs.append(Document(
                id=f"doc_{i}_chunk_{j}",
                content=c,
                metadata={"doc_name": doc_names[i], "doc_type_name": "Luật"}
            ))
            
    store.add_documents(docs)
    print(f"✅ Đã lưu {len(docs)} đoạn vào cơ sở dữ liệu.\n")
    
    queries = [
        "Theo Luật Giao thông đường bộ, đường cao tốc là gì?",
        "Quy định về việc thắt dây an toàn khi đi xe ô tô là gì?",
        "Hiệu lệnh của người điều khiển giao thông bao gồm những tín hiệu nào?",
        "Luật Trật tự, an toàn giao thông đường bộ năm 2024 quy định gì về trách nhiệm người tham gia giao thông?",
        "Nguyên tắc hoạt động giao thông đường bộ được quy định như thế nào?"
    ]
    
    print("## Kết quả truy xuất\n")
    print("| # | Query | Top-1 Retrieved Chunk (tóm tắt) | Score | Relevant? | Agent Answer (tóm tắt) |")
    print("|---|-------|--------------------------------|-------|-----------|------------------------|")
    for i, q in enumerate(queries):
        res = store.search(q, top_k=1)
        if res:
            top = res[0]
            q_emb = _mock_embed(q)
            c_emb = _mock_embed(top['content'])
            score = _dot(q_emb, c_emb)
            content = top['content'][:40].replace('\n', ' ') + "..."
            print(f"| {i+1} | {q} | {content} | {score:.3f} | Không | Mock LLM Answer |")
        else:
            print(f"| {i+1} | {q} | N/A | 0.000 | Không | N/A |")
            
if __name__ == "__main__":
    main()
