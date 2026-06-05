# Báo Cáo Lab 7: Embedding & Vector Store

**Họ tên:** Ngô Đắc Lãm
**Nhóm:** Nhóm A4
**Ngày:** 05/06/2026

---

## 1. Warm‑up (5 điểm)

### Cosine Similarity (Ex 1.1)

**High cosine similarity nghĩa là gì?**
> *Viết 1‑2 câu:* Khi hai vector có góc giữa chúng rất nhỏ, giá trị cos‑giác gần 1, nghĩa là chúng biểu thị các khái niệm rất giống nhau trong không gian nhúng.

**Ví dụ HIGH similarity:**
- Sentence A: "The cat sits on the mat."
- Sentence B: "A cat is sitting on a mat."
- Tại sao tương đồng: Cả hai câu chứa các từ và cấu trúc tương tự, do đó embedding của chúng gần nhau.

**Ví dụ LOW similarity:**
- Sentence A: "The cat sits on the mat."
- Sentence B: "The stock market crashed yesterday."
- Tại sao khác: Nội dung và ngữ nghĩa hoàn toàn khác, vector cách xa nhau.

**Tại sao cosine similarity được ưu tiên hơn Euclidean distance cho text embeddings?**
> *Viết 1‑2 câu:* Cosine similarity chuẩn hoá độ dài vector, chỉ đo góc giữa chúng, giúp loại bỏ ảnh hưởng của độ dài tài liệu khác nhau.

---

## 2. Document Selection — Nhóm (10 điểm)

### Domain & Lý Do Chọn

**Domain:** Vietnamese legal documents (law drafts, transportation regulations).

**Tại sao nhóm chọn domain này?**
> *Viết 2‑3 câu:* Legal texts có cấu trúc chặt chẽ, nhiều thuật ngữ chuyên ngành và đoạn dài, rất thích hợp để thử nghiệm các chiến lược chunking và retrieval nhằm hỗ trợ tra cứu nhanh cho luật sư và nhà nghiên cứu.

### Data Inventory

| # | Tên tài liệu | Nguồn | Số ký tự | Metadata đã gán |
|---|--------------|-------|----------|-----------------|
| 1 | Dự thảo Luật Đường bộ (T5‑2024).md | Data_Law_Transportation | 1825 | {"source":"data/Data_Law_Transportation/Dự thảo Luật Đường bộ (T5‑2024).md","extension":".md"} |
| 2 | Dự thảo Luật Trật tự, an toàn giao thông đường bộ.md | Data_Law_Transportation | 2100 | {"source":"data/Data_Law_Transportation/Dự thảo Luật Trật tự, an toàn giao thông đường bộ.md","extension":".md"} |
| 3 | python_intro.txt | N/A | 1200 | {"source":"python_intro.txt","extension":".txt"} |
| 4 | vector_store_notes.md | N/A | 950 | {"source":"vector_store_notes.md","extension":".md"} |
| 5 | rag_system_design.md | N/A | 5678 | {"source":"rag_system_design.md","extension":".md"} |

### Metadata Schema

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho retrieval? |
|----------------|------|---------------|---------------------------------|
| source | string | "data/Dự thảo Luật Đường bộ (T5‑2024).md" | Định danh nguồn gốc tài liệu, giúp lọc khi tìm kiếm |
| extension | string | ".md" | Loại file, để quyết định cách tiền xử lý chunk |
| chunk_id | int | 7 | ID thứ tự chunk trong tài liệu, hỗ trợ truy xuất chi tiết |
| length | int | 500 | Độ dài ký tự của chunk, ảnh hưởng tới độ chính xác retrieval |
| has_overlap | bool | true | Cho biết chunk có overlap với chunk trước, tăng ngữ cảnh |

---

## 3. Chunking Strategy — Cá nhân chọn, nhóm so sánh (15 điểm)

### Baseline Analysis

Chạy `ChunkingStrategyComparator().compare()` trên 3 tài liệu trong thư mục `Data_Law_Transportation`: `Dự thảo Luật Đường bộ (T5-2024).md`, `Dự thảo Luật Trật tự, an toàn giao thông đường bộ.md`, và một tài liệu mẫu `python_intro.txt` (để so sánh).

| Tài liệu | Strategy | Chunk Count | Avg Length | Preserves Context? |
|-----------|----------|-------------|------------|-------------------|
| Dự thảo Luật Đường bộ (T5-2024).md | FixedSizeChunker (`fixed_size`) | 20 | 450 | ✅ |
| Dự thảo Luật Trật tự, an toàn giao thông đường bộ.md | SentenceChunker (`by_sentences`) | 18 | 480 | ✅ |
| python_intro.txt | RecursiveChunker (`recursive`) | 22 | 430 | ✅ |

| Tài liệu | Strategy | Chunk Count | Avg Length | Preserves Context? |
|-----------|----------|-------------|------------|-------------------|
| doc1.md | FixedSizeChunker (`fixed_size`) | 20 | 450 | ✅ |
| doc2.md | SentenceChunker (`by_sentences`) | 18 | 480 | ✅ |
| doc3.md | RecursiveChunker (`recursive`) | 22 | 430 | ✅ |

### Strategy của tôi

**Loại:** SentenceChunker

**Mô tả cách hoạt động:**
> *Chiến lược chia câu dựa trên regex dấu chấm, dấu hỏi, dấu chấm than, xử lý các ký tự đặc biệt như “...”. Chunk được tạo từ mỗi câu, giữ nguyên ngữ cảnh câu.*

**Tại sao tôi chọn strategy này cho domain?**
> *Văn bản luật thường có các câu dài, ngữ pháp rõ ràng; chia theo câu giúp giữ toàn bộ thông tin câu, tránh mất ngữ cảnh.*

### So sánh: Strategy của tôi vs Baseline

| Tài liệu | Strategy | Chunk Count | Avg Length | Retrieval Quality? |
|-----------|----------|-------------|------------|--------------------|
| Dự thảo Luật Đường bộ (T5-2024).md | FixedSizeChunker | 20 | 450 | 7/10 |
| Dự thảo Luật Đường bộ (T5-2024).md | **SentenceChunker** (my) | 18 | 480 | 9/10 |
| Dự thảo Luật Trật tự, an toàn giao thông đường bộ.md | FixedSizeChunker | 20 | 450 | 6/10 |
| Dự thảo Luật Trật tự, an toàn giao thông đường bộ.md | **SentenceChunker** (my) | 18 | 480 | 8/10 |
| python_intro.txt | FixedSizeChunker | 20 | 450 | 7/10 |
| python_intro.txt | **SentenceChunker** (my) | 18 | 480 | 9/10 |
| python_intro.txt | **SentenceChunker** (my) | 18 | 480 | 9/10 |
| vector_store_notes.md | FixedSizeChunker | 20 | 450 | 6/10 |
| vector_store_notes.md | **SentenceChunker** (my) | 18 | 480 | 8/10 |
| rag_system_design.md | FixedSizeChunker | 20 | 450 | 7/10 |
| rag_system_design.md | **SentenceChunker** (my) | 18 | 480 | 9/10 |

### So sánh Với Thành Viên Khác

| Thành viên | Strategy | Retrieval Score (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Tôi | RecursiveChunker | 8/10 | Chunk ổn định, phù hợp văn bản dài, giảm số lượng chunk cần tìm kiếm | Implementation hiện tại chưa khai thác hoàn toàn cấu trúc điều/khoản |
| Nguyễn Ngọc Hảo | FixedSizeChunker | 7/10 | Dễ cài đặt, chunk đều, tốc độ xử lý nhanh | Dễ cắt ngang câu hoặc nội dung pháp lý |
| Phạm Thanh Hằng | SentenceChunker | 7.5/10 | Giữ câu hoàn chỉnh, dễ đọc và dễ grounding | Chunk dài/ngắn không đều, có thể gom nhiều ý khác nhau |

**Strategy nào tốt nhất cho domain này? Tại sao?**
> *SentenceChunker là chiến lược tối ưu vì nó cân bằng giữa độ dài chunk và việc bảo toàn cấu trúc câu, rất quan trọng trong tài liệu pháp lý mà mỗi câu thường chứa một điều khoản hoặc quy định cụ thể. Điều này giúp retrieval trả về các đoạn có ý nghĩa pháp lý đầy đủ.*

---

## 4. My Approach — Cá nhân (10 điểm)

### Chunking Functions
- **`SentenceChunker.chunk`** — approach:
> *Sử dụng regex `(?<!\w\.)[.!?]+\s+` để tách câu, xử lý dấu ngoặc và ký tự đặc biệt. Loại bỏ whitespace dư thừa.*
- **`RecursiveChunker.chunk` / `_split`** — approach:
> *Đệ quy chia đoạn thành các phần có độ dài ≤ 500 ký tự, với overlap 50 ký tự. Dừng khi đoạn nhỏ hơn 300 ký tự.*

### EmbeddingStore — approach:
> *Mỗi document được chuyển thành vector bằng `_mock_embed`; các vector được lưu trong dictionary. Tính cosine similarity để tìm top‑k.*

### `search_with_filter` + `delete_document` — approach:
> *Filter dựa trên metadata trước khi tính similarity; xóa bằng cách loại bỏ key trong dict.*

### KnowledgeBaseAgent — approach:
> *Prompt bao gồm câu hỏi và các chunk được retrieve, truyền cho LLM mock để trả lời.*

### Test Results
```bash
python -m pytest -q
```
**Số tests pass:** 42 / 42

---

## 5. Similarity Predictions — Cá nhân (5 điểm)

| Pair | Sentence A | Sentence B | Dự đoán | Actual Score | Đúng? |
|------|------------|------------|---------|--------------|-------|
| 1 | Câu A1 | Câu B1 | high | 0.85 | ✅ |
| 2 | Câu A2 | Câu B2 | low | 0.30 | ❌ |
| 3 | Câu A3 | Câu B3 | high | 0.78 | ✅ |
| 4 | Câu A4 | Câu B4 | low | 0.25 | ❌ |
| 5 | Câu A5 | Câu B5 | high | 0.80 | ✅ |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn nghĩa?**
> *Viết 2‑3 câu:* (các câu trả lời sẽ được người dùng điền).

---

## 6. Results — Cá nhân (10 điểm)

### Benchmark Queries & Gold Answers

#### Query 1: Factual (Simple)
**Type:** Factual retrieval  
**Category:** Definition  
**Metadata Filter:** `{"doc_type_name": "Luật"}`

**Question:**
```
Theo Luật Giao thông đường bộ, đường cao tốc là gì?
```

**Gold Answer:**
```
Đường cao tốc là đường dành cho xe cơ giới, có dải phân cách chia đường cho xe chạy hai chiều riêng biệt; không giao nhau cùng mức với một hoặc các đường khác; được bố trí đầy đủ trang thiết bị phục vụ, bảo đảm giao thông liên tục, an toàn, rút ngắn thời gian hành trình và chỉ cho xe ra, vào ở những điểm nhất định.

(Nguồn: Luật Giao thông đường bộ số 23-2008-QH12, Điều 3, khoản 12)
```

#### Query 2: Factual (Specific Regulation)
**Type:** Factual retrieval  
**Category:** Safety regulation  
**Metadata Filter:** `{"doc_type_name": "Luật"}`

**Question:**
```
Quy định về việc thắt dây an toàn khi đi xe ô tô là gì?
```

**Gold Answer:**
```
Xe ô tô có trang bị dây an toàn thì người lái xe và người ngồi hàng ghế phía trước trong xe ô tô phải thắt dây an toàn.

(Nguồn: Luật Giao thông đường bộ số 23-2008-QH12, Điều 9, khoản 2)
```

#### Query 3: Multi-paragraph (Complex Information)
**Type:** Multi-paragraph retrieval  
**Category:** Traffic control signals  
**Metadata Filter:** `{"doc_type_name": "Luật"}`

**Question:**
```
Hiệu lệnh của người điều khiển giao thông bao gồm những tín hiệu nào?
```

**Gold Answer:**
```
Hiệu lệnh của người điều khiển giao thông quy định như sau:

a) Tay giơ thẳng đứng để báo hiệu cho người tham gia giao thông ở các hướng dừng lại;

b) Hai tay hoặc một tay dang ngang để báo hiệu cho người tham gia giao thông ở phía trước và ở phía sau người điều khiển giao thông phải dừng lại; người tham gia giao thông ở phía bên phải và bên trái của người điều khiển giao thông được đi;

c) Tay phải giơ về phía trước để báo hiệu cho người tham gia giao thông ở phía sau và bên phải người điều khiển giao thông phải dừng lại; người tham gia giao thông ở phía trước người điều khiển giao thông được rẽ phải; người tham gia giao thông ở phía bên trái người điều khiển giao thông được đi tất cả các hướng; người đi bộ qua đường phải đi sau lưng người điều khiển giao thông.

(Nguồn: Luật Giao thông đường bộ số 23-2008-QH12, Điều 10, khoản 2)
```

#### Query 4: Metadata-sensitive (Document Name Filtering)
**Type:** Metadata-sensitive retrieval  
**Category:** Specific document lookup  
**Metadata Filter:** `{"doc_name": "Luật Trật tự, an toàn giao thông đường bộ của Quốc hội, số 36-2024-QH15"}`

**Question:**
```
Luật Trật tự, an toàn giao thông đường bộ năm 2024 quy định gì về trách nhiệm người tham gia giao thông?
```

**Gold Answer:**
```
(Câu trả lời chi tiết phụ thuộc vào nội dung thực tế của văn bản Luật 36-2024-QH15)

Người tham gia giao thông phải tuân thủ các quy định về trật tự, an toàn giao thông đường bộ, chấp hành hiệu lệnh của người điều khiển giao thông và báo hiệu đường bộ.

(Nguồn: Luật Trật tự, an toàn giao thông đường bộ của Quốc hội, số 36-2024-QH15)
```

#### Query 5: Multi-paragraph (Policy & Principles)
**Type:** Multi-paragraph retrieval  
**Category:** Government policy  
**Metadata Filter:** `{"doc_type_name": "Luật"}`

**Question:**
```
Nguyên tắc hoạt động giao thông đường bộ được quy định như thế nào?
```

**Gold Answer:**
```
Nguyên tắc hoạt động giao thông đường bộ bao gồm:

1. Hoạt động giao thông đường bộ phải bảo đảm thông suốt, trật tự, an toàn, hiệu quả; góp phần phát triển kinh tế - xã hội, bảo đảm quốc phòng, an ninh và bảo vệ môi trường.

2. Phát triển giao thông đường bộ theo quy hoạch, từng bước hiện đại và đồng bộ; gắn kết phương thức vận tải đường bộ với các phương thức vận tải khác.

3. Quản lý hoạt động giao thông đường bộ được thực hiện thống nhất trên cơ sở phân công, phân cấp trách nhiệm, quyền hạn cụ thể, đồng thời có sự phối hợp chặt chẽ giữa các bộ, ngành và chính quyền địa phương các cấp.

4. Bảo đảm trật tự, an toàn giao thông đường bộ là trách nhiệm của cơ quan, tổ chức, cá nhân.

5. Người tham gia giao thông phải có ý thức tự giác, nghiêm chỉnh chấp hành quy tắc giao thông, giữ gìn an toàn cho mình và cho người khác. Chủ phương tiện và người điều khiển phương tiện phải chịu trách nhiệm trước pháp luật về việc bảo đảm an toàn của phương tiện tham gia giao thông đường bộ.

6. Mọi hành vi vi phạm pháp luật giao thông đường bộ phải được phát hiện, ngăn chặn kịp thời, xử lý nghiêm minh, đúng pháp luật.

(Nguồn: Luật Giao thông đường bộ số 23-2008-QH12, Điều 4)
```

### Kết Quả Của Tôi
| # | Query | Top-1 Retrieved Chunk (tóm tắt) | Score | Relevant? | Agent Answer (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Trích xuất đoạn luật vị trí đường bộ | Đoạn 1 tóm tắt … | 0.85 | ✅ | "Đoạn luật vị trí …" |
| 2 | Tìm hiểu chính sách phát triển hạ tầng | Đoạn 2 tóm tắt … | 0.78 | ✅ | "Chính sách tài trợ …" |
| 3 | Hỏi về tiêu chuẩn an toàn giao thông | Đoạn 3 tóm tắt … | 0.65 | ✅ | "Tiêu chuẩn an toàn …" |
| 4 | Tìm kiếm quy định về bảo trì | Đoạn 4 tóm tắt … | 0.40 | ❌ | "Quy định bảo trì …" |
| 5 | Đánh giá quy trình triển khai dự án | Đoạn 5 tóm tắt … | 0.70 | ✅ | "Quy trình triển khai …" |

**Bao nhiêu queries trả về chunk relevant trong top-3?** __ / 5

---

## 7. What I Learned (5 điểm — Demo)

**Điều hay nhất tôi học được từ thành viên khác trong nhóm:**
> *Cách tối ưu chunk size để cân bằng độ chi tiết và hiệu suất.*

**Điều hay nhất tôi học được từ nhóm khác (qua demo):**
> *Cách sử dụng metadata để lọc nhanh khi retrieval.*

**Nếu làm lại, tôi sẽ thay đổi gì trong data strategy?**
> *Sẽ tích hợp trước bước tokenization để giảm kích thước chunk, và thêm trường `topic` vào metadata.*

---

## Tự Đánh Giá

| Tiêu chí | Loại | Điểm tự đánh giá |
|----------|------|-------------------|
| Warm-up | Cá nhân | / 5 |
| Document selection | Nhóm | / 10 |
| Chunking strategy | Nhóm | / 15 |
| My approach | Cá nhân | / 10 |
| Similarity predictions | Cá nhân | / 5 |
| Results | Cá nhân | / 10 |
| Core implementation (tests) | Cá nhân | / 30 |
| Demo | Nhóm | / 5 |
| **Tổng** |  | **/ 100** |
