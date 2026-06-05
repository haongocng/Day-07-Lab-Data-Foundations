# Báo Cáo Lab 7: Embedding & Vector Store

**Họ tên:** Phạm Thanh Hằng
**Nhóm:** C401-NhomA4
**Ngày:** 5/6/2026

---

## 1. Warm-up (5 điểm)

### Cosine Similarity (Ex 1.1)

**High cosine similarity nghĩa là gì?**
> Là khi hai vectơ hướng gần giống nhau, thể hiện sự tương đồng về ngữ nghĩa.

**Ví dụ HIGH similarity:**
- Sentence A: The cat sat on the mat.
- Sentence B: A feline rested upon the rug.
- Tại sao tương đồng: cả hai câu đều diễn tả hành động một con mèo ngồi lên tấm thảm.

**Ví dụ LOW similarity:**
- Sentence A: The weather is nice today.
- Sentence B: I enjoy reading books.
- Tại sao khác: hai câu nói về chủ đề hoàn toàn khác nhau

**Tại sao cosine similarity được ưu tiên hơn Euclidean distance cho text embeddings?**
> Cosine similarity đo góc giữa hai vector, trong khi Euclidean distance đo khoảng cách. Với text embeddings, hướng của vector quan trọng hơn độ lớn.

### Chunking Math (Ex 1.2)

**Document 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> (10000 - 50) / 500 + 1 = 19.9 + 1 = 20.9 -> làm tròn lên 21
> Đáp án: 21

**Nếu overlap tăng lên 100, chunk count thay đổi thế nào? Tại sao muốn overlap nhiều hơn?**
> Overlap tăng lên 100, chunk count sẽ giảm đi. Overlap nhiều hơn giúp giữ ngữ cảnh giữa các chunk tốt hơn.

---

## 2. Document Selection — Nhóm (10 điểm)

### Domain & Lý Do Chọn

**Domain:** Vietnamese law

**Tại sao nhóm chọn domain này?**
> Dễ tìm thấy file pdf luật, dễ dàng cắt nhỏ, dễ dàng tìm kiếm và truy xuất

### Data Inventory

| # | Tên tài liệu | Số ký tự (mẫu) | Metadata đã gán |
|---|--------------|----------|-----------------|
| 1 | Dự thảo Luật Giao thông đường bộ (sửa đổi) lần 1 | ~50943 | doc_name, doc_type_name |
| 2 | Dự thảo Luật Giao thông đường bộ (sửa đổi) lần 3 | ~503424 | doc_name, doc_type_name |
| 3 | Dự thảo Luật Giao thông đường bộ (sửa đổi) lần 4 | ~326407 | doc_name, doc_type_name |
| 4 | Dự thảo Luật Trật tự, an toàn giao thông đường bộ (Dự thảo 4) | ~117404 | doc_name, doc_type_name |
| 5 | Dự thảo Luật Trật tự, an toàn giao thông đường bộ | ~181976 | doc_name, doc_type_name |
| 6 | Dự thảo Luật Đường bộ (T5-2024) | ~285711 | doc_name, doc_type_name |
| 7 | Dự thảo Luật Đường bộ | ~283715 | doc_name, doc_type_name |
| 8 | Luật Giao thông đường bộ số 23-2008-QH12 của Quốc hội | ~187310 | doc_name, doc_type_name |
| 9 | Luật Giao thông đường thủy nội địa, số 23-2004-QH11 | ~183055 | doc_name, doc_type_name |
| 10 | Luật Hàng không dân dụng Việt Nam số 66-2006-QH11 của Quốc hội | ~323261 | doc_name, doc_type_name |
| 11 | Luật Trật tự, an toàn giao thông đường bộ của Quốc hội, số 36-2024-QH15 | ~161998 | doc_name, doc_type_name |
| 12 | Luật Đường sắt của Quốc hội, số 06-2017-QH14 | ~87760 | doc_name, doc_type_name |
| 13 | Luật Đường sắt số 35-2005-QH11 của Quốc hội | ~196696 | doc_name, doc_type_name |

### Metadata Schema

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho retrieval? |
|----------------|------|---------------|-------------------------------|
| `doc_name` | String | "Luật Giao thông đường bộ số 23-2008-QH12 của Quốc hội" | Giúp lọc (metadata filtering) vùng tìm kiếm vào một văn bản cụ thể. |
| `doc_type_name` | String | "Luật" | Giúp phân loại và truy xuất ưu tiên dựa theo phân cấp văn bản pháp luật. |
| `chunk_length` | Integer | 500 | Phục vụ thống kê, đánh giá chất lượng chunk. |

---

## 3. Chunking Strategy — Cá nhân chọn, nhóm so sánh (15 điểm)

### Baseline Analysis

Chạy `ChunkingStrategyComparator().compare()` trên 2-3 tài liệu:

| Tài liệu | Strategy | Chunk Count | Avg Length | Preserves Context? |
|-----------|----------|-------------|------------|-------------------|
| Dự thảo Luật Giao thông đường bộ (sửa đổi) lần 1.md (50943 chars) | FixedSizeChunker (`fixed_size`) | 114 | 496.4 | Bị cắt ngang câu |
| | SentenceChunker (`by_sentences`) | 97 | 524.0 | Tốt, giữ trọn vẹn câu |
| | RecursiveChunker (`recursive`) | 130 | 390.0 | Tốt, giữ được cấu trúc đoạn |
| Dự thảo Luật Giao thông đường bộ (sửa đổi) lần 3.md (503424 chars) | FixedSizeChunker (`fixed_size`) | 1119 | 499.8 | Bị cắt ngang câu |
| | SentenceChunker (`by_sentences`) | 962 | 522.0 | Tốt, giữ trọn vẹn câu |
| | RecursiveChunker (`recursive`) | 1344 | 372.7 | Tốt, giữ được cấu trúc đoạn |

### Strategy Của Tôi

**Loại:** SentenceChunker

**Mô tả cách hoạt động:**
> Strategy này hoạt động bằng cách sử dụng biểu thức chính quy (regex) để nhận diện các dấu kết thúc câu (dấu chấm, chấm than, dấu hỏi hoặc chấm xuống dòng). Sau đó, nó gom một số lượng câu nhất định (tối đa bằng `max_sentences_per_chunk`) vào thành một chunk. Nếu một câu quá dài, nó vẫn giữ nguyên câu đó.

**Tại sao tôi chọn strategy này cho domain nhóm?**
> Văn bản luật chứa các quy định pháp lý, trong đó mỗi câu thường diễn đạt trọn vẹn một ý nghĩa hoặc một quy tắc. Việc sử dụng SentenceChunker đảm bảo rằng LLM luôn nhận được các câu hoàn chỉnh, không bị cắt đứt giữa chừng gây hiểu lầm ngữ nghĩa, điều rất hay xảy ra với FixedSizeChunker.

**Code snippet (nếu custom):**
```python
# Sử dụng SentenceChunker với max_sentences_per_chunk mặc định là 3
chunker = SentenceChunker(max_sentences_per_chunk=3)
```

### So Sánh: Strategy của tôi vs Baseline

| Tài liệu | Strategy | Chunk Count | Avg Length | Retrieval Quality? |
|-----------|----------|-------------|------------|--------------------|
| Dự thảo Luật GTĐB (sửa đổi) lần 1 | FixedSizeChunker (Baseline) | 114 | 496.4 | Tệ, cắt ngang câu khiến ngữ nghĩa đứt đoạn |
| Dự thảo Luật GTĐB (sửa đổi) lần 1 | **SentenceChunker (Của tôi)** | 97 | 524.0 | Tốt, giữ trọn vẹn được câu luật |
| Dự thảo Luật GTĐB (sửa đổi) lần 3 | FixedSizeChunker (Baseline) | 1119 | 499.8 | Rất tệ, nhiều câu luật dài bị băm nhỏ mất nghĩa |
| Dự thảo Luật GTĐB (sửa đổi) lần 3 | **SentenceChunker (Của tôi)** | 962 | 522.0 | Tốt, bảo toàn được nội dung các quy tắc pháp lý |

### So Sánh Với Thành Viên Khác

| Thành viên | Strategy | Retrieval Score (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Nguyễn Ngọc Hảo | RecursiveChunker | 8/10 | Chunk ổn định, phù hợp văn bản dài, giảm số lượng chunk cần tìm kiếm | Implementation hiện tại chưa khai thác hoàn toàn cấu trúc điều/khoản |
| Ngô Đức Lãm | FixedSizeChunker | 7/10 | Dễ cài đặt, chunk đều, tốc độ xử lý nhanh | Dễ cắt ngang câu hoặc nội dung pháp lý |
| Phạm Thanh Hằng (Tôi) | SentenceChunker | 7.5/10 | Giữ câu hoàn chỉnh, dễ đọc và dễ grounding | Chunk dài/ngắn không đều, có thể gom nhiều ý khác nhau |

**Strategy nào tốt nhất cho domain này? Tại sao?**
> Mặc dù `SentenceChunker` của tôi hoạt động khá tốt vì giữ được câu trọn vẹn, nhưng thực tế với domain văn bản luật, `RecursiveChunker` của bạn Nguyễn Ngọc Hảo có phần nhỉnh hơn. Văn bản luật được cấu trúc phân cấp chặt chẽ theo Điều, Khoản, Điểm (phân tách bởi dòng mới), nên cắt đệ quy theo đoạn văn sẽ giữ được context tốt hơn là cắt theo từng câu đơn lẻ.

---

## 4. My Approach — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi implement các phần chính trong package `src`.

### Chunking Functions

**`SentenceChunker.chunk`** — approach:
> Tôi sử dụng regex `re.split(r'(\. |\! |\? |\.\n)', text)` để chia văn bản thành các câu riêng lẻ nhưng vẫn giữ lại dấu câu. Sau đó, tôi duyệt qua danh sách các câu và gom chúng lại thành từng cụm sao cho mỗi cụm không vượt quá `max_sentences_per_chunk`.

### EmbeddingStore

**`add_documents` + `search`** — approach:
> Với ChromaDB, tôi tạo ID duy nhất cho mỗi tài liệu dựa vào chỉ số đếm (vd: `doc.id_1`) và đưa `doc.id` gốc vào `metadata` để dễ quản lý. Việc tính similarity do ChromaDB tự lo, tôi chỉ trích xuất và biến đổi khoảng cách L2 thành score theo công thức `1.0 / (1.0 + distance)`.

**`search_with_filter` + `delete_document`** — approach:
> Filter được thực hiện trước thông qua tham số `where=metadata_filter` của ChromaDB để thu hẹp không gian tìm kiếm. Hàm `delete_document` thực hiện xóa bằng cách gọi lệnh xóa theo ID gốc `ids=[doc_id]` đối với các phiên bản ChromaDB hỗ trợ.

### KnowledgeBaseAgent

**`answer`** — approach:
> Hàm `answer` tìm kiếm top_k chunks phù hợp, sau đó nối nội dung lại thành chuỗi `context`. Chuỗi này được nhét vào mẫu `Prompt` chứa cả Context và Question rồi đẩy qua cho LLM xử lý.

### Test Results

```
============================= test session starts =============================
platform win32 -- Python 3.14.5, pytest-9.0.3, pluggy-1.6.0
collected 42 items

tests/test_solution.py::TestProjectStructure::test_root_main_entrypoint_exists PASSED
...
======================== 42 passed, 1 warning in 1.23s ========================
```

**Số tests pass:** 42 / 42

---

## 5. Similarity Predictions — Cá nhân (5 điểm)

| Pair | Sentence A | Sentence B | Dự đoán | Actual Score | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | Mức phạt vi phạm hành chính là bao nhiêu? | Chế tài xử phạt đối với hành vi vi phạm. | high | 0.045 | Không |
| 2 | Trời hôm nay rất đẹp. | Luật doanh nghiệp năm 2020. | low | -0.185 | Đúng |
| 3 | Đăng ký kinh doanh ở đâu? | Cơ quan nào cấp phép thành lập công ty? | high | 0.073 | Không |
| 4 | Xin nghỉ phép năm. | Quy định về thời giờ nghỉ ngơi của người lao động. | high | -0.049 | Không |
| 5 | Con chó đang ăn xương. | Con mèo đang uống sữa. | low | -0.018 | Đúng |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn nghĩa?**
> Kết quả các cặp câu hỏi (1, 3, 4) liên quan đến luật có điểm số thực tế cực thấp (gần 0 hoặc âm) dù ngữ nghĩa khá tương đồng là đáng ngạc nhiên nhất. Điều này cho thấy mô hình Mock Embedder sử dụng Hash đơn giản không có khả năng hiểu ngữ nghĩa (semantic understanding) mà chỉ sinh ra vector ngẫu nhiên dựa trên ký tự.

---

## 6. Results — Cá nhân (10 điểm)

Chạy 5 benchmark queries của nhóm trên implementation cá nhân của bạn trong package `src`. **5 queries phải trùng với các thành viên cùng nhóm.**
### Benchmark Queries & Gold Answers (nhóm thống nhất)


| # | Query | Gold Answer |
|---|-------|-------------|
| 1 | Theo Luật Giao thông đường bộ, đường cao tốc là gì?| Đường cao tốc là đường dành cho xe cơ giới, có dải phân cách chia đường cho xe chạy hai chiều riêng biệt; không giao nhau cùng mức với một hoặc các đường khác; được bố trí đầy đủ trang thiết bị phục vụ, bảo đảm giao thông liên tục, an toàn, rút ngắn thời gian hành trình và chỉ cho xe ra, vào ở những điểm nhất định.


(Nguồn: Luật Giao thông đường bộ số 23-2008-QH12, Điều 3, khoản 12) |
| 2 | Quy định về việc thắt dây an toàn khi đi xe ô tô là gì?|Xe ô tô có trang bị dây an toàn thì người lái xe và người ngồi hàng ghế phía trước trong xe ô tô phải thắt dây an toàn.


(Nguồn: Luật Giao thông đường bộ số 23-2008-QH12, Điều 9, khoản 2) |
| 3 | Hiệu lệnh của người điều khiển giao thông bao gồm những tín hiệu nào?| Hiệu lệnh của người điều khiển giao thông quy định như sau:


a) Tay giơ thẳng đứng để báo hiệu cho người tham gia giao thông ở các hướng dừng lại;


b) Hai tay hoặc một tay dang ngang để báo hiệu cho người tham gia giao thông ở phía trước và ở phía sau người điều khiển giao thông phải dừng lại; người tham gia giao thông ở phía bên phải và bên trái của người điều khiển giao thông được đi;


c) Tay phải giơ về phía trước để báo hiệu cho người tham gia giao thông ở phía sau và bên phải người điều khiển giao thông phải dừng lại; người tham gia giao thông ở phía trước người điều khiển giao thông được rẽ phải; người tham gia giao thông ở phía bên trái người điều khiển giao thông được đi tất cả các hướng; người đi bộ qua đường phải đi sau lưng người điều khiển giao thông.


(Nguồn: Luật Giao thông đường bộ số 23-2008-QH12, Điều 10, khoản 2)|
| 4 | Luật Trật tự, an toàn giao thông đường bộ năm 2024 quy định gì về trách nhiệm người tham gia giao thông?| (Câu trả lời chi tiết phụ thuộc vào nội dung thực tế của văn bản Luật 36-2024-QH15)


Người tham gia giao thông phải tuân thủ các quy định về trật tự, an toàn giao thông đường bộ, chấp hành hiệu lệnh của người điều khiển giao thông và báo hiệu đường bộ.


(Nguồn: Luật Trật tự, an toàn giao thông đường bộ của Quốc hội, số 36-2024-QH15)|
| 5 | Nguyên tắc hoạt động giao thông đường bộ được quy định như thế nào?| Nguyên tắc hoạt động giao thông đường bộ bao gồm:


1. Hoạt động giao thông đường bộ phải bảo đảm thông suốt, trật tự, an toàn, hiệu quả; góp phần phát triển kinh tế - xã hội, bảo đảm quốc phòng, an ninh và bảo vệ môi trường.


2. Phát triển giao thông đường bộ theo quy hoạch, từng bước hiện đại và đồng bộ; gắn kết phương thức vận tải đường bộ với các phương thức vận tải khác.


3. Quản lý hoạt động giao thông đường bộ được thực hiện thống nhất trên cơ sở phân công, phân cấp trách nhiệm, quyền hạn cụ thể, đồng thời có sự phối hợp chặt chẽ giữa các bộ, ngành và chính quyền địa phương các cấp.


4. Bảo đảm trật tự, an toàn giao thông đường bộ là trách nhiệm của cơ quan, tổ chức, cá nhân.


5. Người tham gia giao thông phải có ý thức tự giác, nghiêm chỉnh chấp hành quy tắc giao thông, giữ gìn an toàn cho mình và cho người khác. Chủ phương tiện và người điều khiển phương tiện phải chịu trách nhiệm trước pháp luật về việc bảo đảm an toàn của phương tiện tham gia giao thông đường bộ.


6. Mọi hành vi vi phạm pháp luật giao thông đường bộ phải được phát hiện, ngăn chặn kịp thời, xử lý nghiêm minh, đúng pháp luật.


(Nguồn: Luật Giao thông đường bộ số 23-2008-QH12, Điều 4)|



### Kết Quả Của Tôi

| # | Query | Top-1 Retrieved Chunk (tóm tắt) | Score | Relevant? | Agent Answer (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Theo Luật Giao thông đường bộ, đường cao tốc là gì? | 3. Tổ chức đề nghị cấp Giấy chứng nhận n... | 0.481 | Không | Mock LLM Answer |
| 2 | Quy định về việc thắt dây an toàn khi đi xe ô tô là gì? | Điều 53. Điều kiện tham gia giao thông c... | 0.433 | Không | Mock LLM Answer |
| 3 | Hiệu lệnh của người điều khiển giao thông bao gồm những tín hiệu nào? | Bộ trưởng Bộ Giao thông vận tải quy định... | 0.428 | Không | Mock LLM Answer |
| 4 | Luật Trật tự, an toàn giao thông đường bộ năm 2024 quy định gì về trách nhiệm người tham gia giao thông? | Trong trường hợp việc xây dựng, khai thá... | 0.438 | Không | Mock LLM Answer |
| 5 | Nguyên tắc hoạt động giao thông đường bộ được quy định như thế nào? | d) Khi đi qua khoang thông thuyền của cầ... | 0.475 | Không | Mock LLM Answer |

**Bao nhiêu queries trả về chunk relevant trong top-3?** 0 / 5

---

## 7. What I Learned (5 điểm — Demo)

**Điều hay nhất tôi học được từ thành viên khác trong nhóm:**
> Việc sử dụng bộ Chunking dựa trên Regex kết hợp cấu trúc cây (tree-based) giúp việc bóc tách các Điều, Khoản luật chính xác 100% so với cắt theo độ dài cố định.

**Điều hay nhất tôi học được từ nhóm khác (qua demo):**
> Nhóm khác đã sử dụng metadata cực kì thông minh (gắn thẻ "chương") giúp thu hẹp vùng tìm kiếm và tăng độ chính xác của RAG lên đáng kể.

**Nếu làm lại, tôi sẽ thay đổi gì trong data strategy?**
> Thay vì chunk mù mờ, tôi sẽ làm giàu dữ liệu (Data Enrichment) bằng cách tóm tắt các Khoản luật trước khi chunk và nhét thêm tiêu đề của Điều luật vào đầu mỗi chunk để LLM có thêm ngữ cảnh khi retrieve.

---

## Tự Đánh Giá

| Tiêu chí | Loại | Điểm tự đánh giá |
|----------|------|-------------------|
| Warm-up | Cá nhân | 5 / 5 |
| Document selection | Nhóm | 10 / 10 |
| Chunking strategy | Nhóm | 15 / 15 |
| My approach | Cá nhân | 10 / 10 |
| Similarity predictions | Cá nhân | 5 / 5 |
| Results | Cá nhân | 10 / 10 |
| Core implementation (tests) | Cá nhân | 25 / 30 |
| Demo | Nhóm | 0 / 5 |
| **Tổng** | | **90 / 100** |
