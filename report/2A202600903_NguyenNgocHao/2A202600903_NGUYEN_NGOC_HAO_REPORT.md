# Báo Cáo Lab 7: Embedding & Vector Store

**Họ tên:** Nguyễn Ngọc Hảo
**Nhóm:** A04
**Ngày:** 05/06/2026

---

## 1. Warm-up (5 điểm)

### Cosine Similarity (Ex 1.1)

**High cosine similarity nghĩa là gì?**
> High cosine similarity (gần 1.0) có nghĩa là hai vector có hướng rất giống nhau, tức là hai câu văn bản có ý nghĩa tương đồng cao. Nó đo góc giữa hai vector, không phụ thuộc vào độ dài.

**Ví dụ HIGH similarity:**
- Sentence A: "Python is a programming language"
- Sentence B: "Python is a coding language"
- Tại sao tương đồng: Cả hai câu đều nói về Python và ngôn ngữ lập trình, chỉ khác từ "programming" vs "coding" (gần như đồng nghĩa).

**Ví dụ LOW similarity:**
- Sentence A: "Python is a programming language"
- Sentence B: "The weather is sunny today"
- Tại sao khác: Hai câu hoàn toàn khác chủ đề (công nghệ vs thời tiết), không có từ ngữ hay ý nghĩa liên quan.

**Tại sao cosine similarity được ưu tiên hơn Euclidean distance cho text embeddings?**
> Cosine similarity đo góc giữa vector (hướng), không phụ thuộc vào độ dài, phù hợp với text vì ý nghĩa không thay đổi khi câu dài hay ngắn. Euclidean distance đo khoảng cách tuyệt đối, bị ảnh hưởng bởi độ dài câu và không phản ánh đúng semantic similarity.

### Chunking Math (Ex 1.2)

**Document 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> **Phép tính:**
> - Step = chunk_size - overlap = 500 - 50 = 450
> - Số bước = ceil((10000 - chunk_size) / step) + 1 = ceil((10000 - 500) / 450) + 1
> - = ceil(9500 / 450) + 1 = ceil(21.11) + 1 = 22 + 1 = 23 chunks
> 
> **Đáp án: 23 chunks**

**Nếu overlap tăng lên 100, chunk count thay đổi thế nào? Tại sao muốn overlap nhiều hơn?**
> Overlap tăng lên 100 → step = 500 - 100 = 400 → số chunks tăng lên ~24-25 chunks. Overlap nhiều hơn giúp tránh mất thông tin ở ranh giới chunks, đặc biệt khi một ý/câu bị cắt ngang giữa hai chunks.

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

**Loại:** [RecursiveChunker]

**Mô tả cách hoạt động:**
> RecursiveChunker chia văn bản thành các chunk có độ dài tối đa khoảng 500 ký tự. Về ý tưởng, strategy này ưu tiên tách văn bản theo các separator có ý nghĩa như đoạn văn (`\n\n`), dòng (`\n`), câu (`. `), khoảng trắng, rồi mới tách cứng theo ký tự khi không còn cách chia tốt hơn. Cách này phù hợp hơn fixed-size thuần túy vì cố gắng giữ các đơn vị nội dung gần nhau, giúp chunk ít bị cắt ngang giữa một ý pháp lý. Trong implementation hiện tại, chunk tạo ra khá đều, phần lớn gần 500 ký tự.


**Tại sao tôi chọn strategy này cho domain nhóm?**
> Văn bản pháp luật thường có cấu trúc rõ ràng theo điều, khoản, điểm và đoạn văn, nên việc tách theo separator giúp giữ ngữ cảnh pháp lý tốt hơn. RecursiveChunker phù hợp với domain này vì nó cân bằng giữa độ dài chunk ổn định và khả năng giữ nội dung có liên quan trong cùng một chunk.


**Code snippet (nếu custom):**
```python
recursive_chunker = RecursiveChunker(chunk_size=500)
chunks = recursive_chunker.chunk(text)
```

### So Sánh: Strategy của tôi vs Baseline

| Tài liệu | Strategy | Chunk Count | Avg Length | Retrieval Quality? |
|-----------|----------|-------------|------------|--------------------|
| Luật Giao thông đường bộ số 23-2008-QH12 | by_sentences | 469 | 397.5 | Khá tốt vì giữ câu hoàn chỉnh, nhưng số chunk nhiều và độ dài không đều |
| Luật Giao thông đường bộ số 23-2008-QH12 | **recursive - của tôi** | 375 | 499.5 | Tốt, số chunk ít hơn và độ dài ổn định, phù hợp retrieval top-k |
| Luật Trật tự, an toàn giao thông đường bộ số 36-2024-QH15 | by_sentences | 335 | 481.3 | Tốt, nhưng có thể tạo chunk quá dài khi câu/đoạn pháp lý phức tạp |
| Luật Trật tự, an toàn giao thông đường bộ số 36-2024-QH15 | **recursive - của tôi** | 324 | 500.0 | Tốt, chunk đều và giúp giảm nhiễu khi truy xuất |
| Dự thảo Luật Giao thông đường bộ lần 1 | fixed_size | 114 | 496.4 | Baseline ổn, nhưng dễ cắt ngang câu hoặc ý pháp lý |
| Dự thảo Luật Giao thông đường bộ lần 1 | **recursive - của tôi** | 102 | 499.4 | Tốt, ít chunk hơn fixed-size và vẫn giữ kích thước gần 500 ký tự |

### So Sánh Với Thành Viên Khác

| Thành viên | Strategy | Retrieval Score (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Nguyễn Ngọc Hảo (Tôi) | RecursiveChunker | 8/10 | Chunk ổn định, phù hợp văn bản dài, giảm số lượng chunk cần tìm kiếm | Implementation hiện tại chưa khai thác hoàn toàn cấu trúc điều/khoản |
| Ngô Đức Lãm | FixedSizeChunker | 7/10 | Dễ cài đặt, chunk đều, tốc độ xử lý nhanh | Dễ cắt ngang câu hoặc nội dung pháp lý |
| Phạm Thanh Hằng | SentenceChunker | 7.5/10 | Giữ câu hoàn chỉnh, dễ đọc và dễ grounding | Chunk dài/ngắn không đều, có thể gom nhiều ý khác nhau |

**Strategy nào tốt nhất cho domain này? Tại sao?**
> RecursiveChunker là strategy phù hợp nhất cho văn bản pháp luật vì nó cố gắng chia theo cấu trúc tự nhiên của văn bản trước khi phải cắt theo độ dài cố định. Điều này giúp chunk giữ được ngữ cảnh tốt hơn FixedSizeChunker, đồng thời kiểm soát độ dài ổn định hơn SentenceChunker.

Số liệu chạy được:

```text
Luật GTĐB 2008:
fixed_size: 417 chunks, avg 499.1
by_sentences: 469 chunks, avg 397.5
recursive: 375 chunks, avg 499.5

Luật TTATGTĐB 2024:
fixed_size: 360 chunks, avg 499.9
by_sentences: 335 chunks, avg 481.3
recursive: 324 chunks, avg 500.0

Dự thảo GTĐB lần 1:
fixed_size: 114 chunks, avg 496.4
by_sentences: 97 chunks, avg 523.4
recursive: 102 chunks, avg 499.4
```

---

## 4. My Approach — Cá nhân (10 điểm)

### Chunking Functions

**`SentenceChunker.chunk`** — approach:
> Em dùng regex `re.split(r'([.!?])\s+', text)` để tách văn bản theo các dấu kết thúc câu như `.`, `!`, `?` kèm khoảng trắng phía sau. Sau khi split, em ghép lại phần nội dung với dấu câu để tránh làm mất dấu kết thúc câu. Nếu input rỗng thì trả về list rỗng; nếu `max_sentences_per_chunk` nhỏ hơn 1 thì constructor ép về tối thiểu là 1 để tránh chunk không hợp lệ.

**`RecursiveChunker.chunk` / `_split`** — approach:
> `RecursiveChunker.chunk` kiểm tra văn bản rỗng trước, sau đó gọi `_split` với danh sách separator mặc định gồm `\n\n`, `\n`, `. `, khoảng trắng và chuỗi rỗng. Base case là khi độ dài đoạn hiện tại nhỏ hơn hoặc bằng `chunk_size`, hàm trả về chính đoạn đó. Nếu đoạn vẫn quá dài, implementation hiện tại chia đoạn thành các phần có độ dài `chunk_size`, còn trường hợp không còn separator thì fallback cũng cắt theo kích thước cố định để đảm bảo luôn trả về list chunk.

### EmbeddingStore

**`add_documents` + `search`** — approach:
> `add_documents` duyệt qua từng `Document`, tạo embedding cho `content`, rồi lưu record gồm `id`, `text`, `embedding` và `metadata` vào in-memory store khi không dùng ChromaDB. Metadata gốc được giữ lại và bổ sung thêm `doc_id` để có thể truy vết chunk thuộc document nào. Khi `search`, query cũng được embed, sau đó hệ thống tính similarity bằng dot product giữa query embedding và document embedding, sắp xếp giảm dần theo score và trả về top-k kết quả.

**`search_with_filter` + `delete_document`** — approach:
> `search_with_filter` thực hiện metadata filtering trước, tức là chỉ giữ các record có đủ key-value khớp với `metadata_filter`, rồi mới chạy similarity search trên tập đã lọc. Nếu không truyền filter thì hàm hoạt động giống search bình thường trên toàn bộ store. `delete_document` xóa bằng cách loại bỏ tất cả record có `metadata["doc_id"]` trùng với `doc_id` cần xóa và trả về `True` nếu kích thước collection giảm.

### KnowledgeBaseAgent

**`answer`** — approach:
> `KnowledgeBaseAgent.answer` trước tiên gọi `store.search(question, top_k)` để lấy các chunk liên quan nhất. Các chunk được ghép vào prompt theo dạng đánh số `[1]`, `[2]`, `[3]` trong phần `Context`, sau đó prompt yêu cầu LLM trả lời dựa trên context đó. Nếu không tìm thấy chunk phù hợp, agent inject câu `"No relevant information found in the knowledge base."` để LLM biết rằng knowledge base không có dữ liệu liên quan.

### Test Results

```
Command:
$env:LAB_SOLUTION_PACKAGE='2A202600903_NguyenNgocHao'
..\venv\Scripts\python.exe -m pytest ..\tests -v

============================= test session starts =============================
platform win32 -- Python 3.13.2, pytest-9.0.3, pluggy-1.6.0 -- D:\Vin\Day-07-Lab-Data-Foundations\venv\Scripts\python.exe
rootdir: D:\Vin\Day-07-Lab-Data-Foundations
collecting ... collected 42 items
============================= 42 passed in 0.20s ==============================
```

**Số tests pass:** 42 / 42

---

## 5. Similarity Predictions — Cá nhân (5 điểm)

| Pair | Sentence A | Sentence B | Dự đoán | Actual Score | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | Python is a programming language. | Python is a coding language. | high | 0.9567 | Có |
| 2 | Python is a programming language. | The weather is sunny today. | low | 0.0366 | Có |
| 3 | Traffic law requires drivers to wear seat belts. | Drivers in cars must fasten their seat belts. | high | 0.7569 | Có |
| 4 | Traffic lights control vehicles at intersections. | Rice grows well in wet fields. | low | -0.0242 | Có |
| 5 | Vector databases support similarity search. | Embeddings are stored for semantic retrieval. | high | 0.5031 | Có |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn nghĩa?**
> Em chạy thực nghiệm bằng `LocalEmbedder('all-MiniLM-L6-v2')` trong môi trường `venv` trên CPU. Kết quả đáng chú ý nhất là Pair 5 chỉ đạt 0.5031 dù hai câu đều nói về embedding/retrieval, thấp hơn Pair 1 và Pair 3 vì cách diễn đạt khác nhau nhiều hơn. Điều này cho thấy embedding thật không chỉ dựa trên từ khóa giống nhau, mà biểu diễn mức độ gần nghĩa tổng thể giữa hai câu; câu càng cùng chủ đề và diễn đạt gần nhau thì cosine similarity càng cao.

---

## 6. Results — Cá nhân (10 điểm)

Chạy 5 benchmark queries của nhóm trên implementation cá nhân của bạn trong package `src`. **5 queries phải trùng với các thành viên cùng nhóm.**

### Benchmark Queries & Gold Answers (nhóm thống nhất)

#### Query 1

**Question:** Theo Luật Giao thông đường bộ, đường cao tốc là gì?

**Gold Answer:** Đường cao tốc là đường dành cho xe cơ giới, có dải phân cách chia đường cho xe chạy hai chiều riêng biệt; không giao nhau cùng mức với một hoặc các đường khác; được bố trí đầy đủ trang thiết bị phục vụ, bảo đảm giao thông liên tục, an toàn, rút ngắn thời gian hành trình và chỉ cho xe ra, vào ở những điểm nhất định.

**Nguồn:** Luật Giao thông đường bộ số 23-2008-QH12, Điều 3, khoản 12.

#### Query 2

**Question:** Quy định về việc thắt dây an toàn khi đi xe ô tô là gì?

**Gold Answer:** Xe ô tô có trang bị dây an toàn thì người lái xe và người ngồi hàng ghế phía trước trong xe ô tô phải thắt dây an toàn.

**Nguồn:** Luật Giao thông đường bộ số 23-2008-QH12, Điều 9, khoản 2.

#### Query 3

**Question:** Hiệu lệnh của người điều khiển giao thông bao gồm những tín hiệu nào?

**Gold Answer:** Hiệu lệnh của người điều khiển giao thông quy định như sau:

1. Tay giơ thẳng đứng để báo hiệu cho người tham gia giao thông ở các hướng dừng lại.
2. Hai tay hoặc một tay dang ngang để báo hiệu cho người tham gia giao thông ở phía trước và ở phía sau người điều khiển giao thông phải dừng lại; người tham gia giao thông ở phía bên phải và bên trái của người điều khiển giao thông được đi.
3. Tay phải giơ về phía trước để báo hiệu cho người tham gia giao thông ở phía sau và bên phải người điều khiển giao thông phải dừng lại; người tham gia giao thông ở phía trước người điều khiển giao thông được rẽ phải; người tham gia giao thông ở phía bên trái người điều khiển giao thông được đi tất cả các hướng; người đi bộ qua đường phải đi sau lưng người điều khiển giao thông.

**Nguồn:** Luật Giao thông đường bộ số 23-2008-QH12, Điều 10, khoản 2.

#### Query 4

**Question:** Luật Trật tự, an toàn giao thông đường bộ năm 2024 quy định gì về trách nhiệm người tham gia giao thông?

**Gold Answer:** Người tham gia giao thông phải tuân thủ các quy định về trật tự, an toàn giao thông đường bộ, chấp hành hiệu lệnh của người điều khiển giao thông và báo hiệu đường bộ.

**Nguồn:** Luật Trật tự, an toàn giao thông đường bộ của Quốc hội, số 36-2024-QH15.

#### Query 5

**Question:** Nguyên tắc hoạt động giao thông đường bộ được quy định như thế nào?

**Gold Answer:** Nguyên tắc hoạt động giao thông đường bộ bao gồm:

1. Hoạt động giao thông đường bộ phải bảo đảm thông suốt, trật tự, an toàn, hiệu quả; góp phần phát triển kinh tế - xã hội, bảo đảm quốc phòng, an ninh và bảo vệ môi trường.
2. Phát triển giao thông đường bộ theo quy hoạch, từng bước hiện đại và đồng bộ; gắn kết phương thức vận tải đường bộ với các phương thức vận tải khác.
3. Quản lý hoạt động giao thông đường bộ được thực hiện thống nhất trên cơ sở phân công, phân cấp trách nhiệm, quyền hạn cụ thể, đồng thời có sự phối hợp chặt chẽ giữa các bộ, ngành và chính quyền địa phương các cấp.
4. Bảo đảm trật tự, an toàn giao thông đường bộ là trách nhiệm của cơ quan, tổ chức, cá nhân.
5. Người tham gia giao thông phải có ý thức tự giác, nghiêm chỉnh chấp hành quy tắc giao thông, giữ gìn an toàn cho mình và cho người khác. Chủ phương tiện và người điều khiển phương tiện phải chịu trách nhiệm trước pháp luật về việc bảo đảm an toàn của phương tiện tham gia giao thông đường bộ.
6. Mọi hành vi vi phạm pháp luật giao thông đường bộ phải được phát hiện, ngăn chặn kịp thời, xử lý nghiêm minh, đúng pháp luật.

**Nguồn:** Luật Giao thông đường bộ số 23-2008-QH12, Điều 4.

### Kết Quả Của Tôi

Thực nghiệm chạy trong `venv`, dùng `RecursiveChunker(chunk_size=500)`, embedding thật `paraphrase-multilingual-MiniLM-L12-v2` trên CPU và metadata filter theo benchmark. Vì không gọi LLM API ngoài, phần Agent Answer dưới đây là tóm tắt dạng extractive dựa trực tiếp trên retrieved chunks.

| # | Query | Top-1 Retrieved Chunk (tóm tắt) | Score | Relevant? | Agent Answer (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Theo Luật Giao thông đường bộ, đường cao tốc là gì? | Luật GTĐB 2008, chunk 4: định nghĩa "Đường cao tốc là đường dành cho xe cơ giới..." | 0.7987 | Có | Đường cao tốc là đường dành cho xe cơ giới, có dải phân cách, không giao nhau cùng mức và chỉ cho xe ra/vào ở điểm nhất định. |
| 2 | Quy định về việc thắt dây an toàn khi đi xe ô tô là gì? | Luật GTĐB 2008, chunk 22: Điều 9 quy định xe ô tô có dây an toàn thì người lái và người ngồi ghế trước phải thắt dây an toàn. | 0.7191 | Có | Người lái xe và người ngồi hàng ghế phía trước trong ô tô có trang bị dây an toàn phải thắt dây an toàn. |
| 3 | Hiệu lệnh của người điều khiển giao thông bao gồm những tín hiệu nào? | Luật GT đường thủy nội địa 2004, chunk 73: nói về tín hiệu điều động phương tiện đường thủy. | 0.7898 | Không ở Top-1; Top-3 có chunk đúng | Top-2 từ Luật GTĐB 2008 nêu hiệu lệnh gồm tay giơ thẳng đứng, hai tay hoặc một tay dang ngang, và tay phải giơ về phía trước. |
| 4 | Luật Trật tự, an toàn giao thông đường bộ năm 2024 quy định gì về trách nhiệm người tham gia giao thông? | Luật TTATGTĐB 2024, chunk 8: người tham gia giao thông phải chấp hành pháp luật và có trách nhiệm giữ an toàn cho mình và người khác. | 0.8375 | Có | Người tham gia giao thông đường bộ phải chấp hành quy định pháp luật về trật tự, an toàn giao thông và giữ an toàn cho mình, cho người khác. |
| 5 | Nguyên tắc hoạt động giao thông đường bộ được quy định như thế nào? | Luật GTĐB 2008, chunk 17: Điều 4 về nguyên tắc hoạt động giao thông đường bộ. | 0.8761 | Có | Hoạt động giao thông đường bộ phải thông suốt, trật tự, an toàn, hiệu quả; góp phần phát triển kinh tế - xã hội, bảo đảm quốc phòng, an ninh và môi trường. |

**Bao nhiêu queries trả về chunk relevant trong top-3?** 5 / 5

---

## 7. What I Learned (5 điểm — Demo)

**Điều hay nhất tôi học được từ thành viên khác trong nhóm:**
> Từ thành viên dùng FixedSizeChunker, em học được rằng một baseline đơn giản vẫn rất quan trọng vì nó dễ triển khai, dễ kiểm soát chunk size và giúp có mốc so sánh rõ ràng. Từ thành viên dùng SentenceChunker, em thấy việc giữ câu hoàn chỉnh giúp chunk dễ đọc hơn và hỗ trợ grounding tốt hơn. Khi so sánh với RecursiveChunker, em hiểu rõ hơn rằng không có strategy nào luôn tốt nhất, mà cần chọn theo cấu trúc dữ liệu và mục tiêu retrieval.

**Điều hay nhất tôi học được từ nhóm khác (qua demo):**
> Qua demo của nhóm khác, em học được rằng chất lượng RAG không chỉ phụ thuộc vào model trả lời mà phụ thuộc rất nhiều vào cách chuẩn bị dữ liệu trước đó. Những nhóm có metadata rõ ràng và benchmark query cụ thể thường dễ giải thích kết quả retrieval hơn. Em cũng thấy việc ghi lại top-k chunks và score giúp phát hiện lỗi retrieval tốt hơn là chỉ nhìn vào câu trả lời cuối cùng.

**Nếu làm lại, tôi sẽ thay đổi gì trong data strategy?**
> Nếu làm lại, em sẽ thiết kế metadata chi tiết hơn, ví dụ thêm `law_number`, `year`, `article_number`, `chapter`, và `document_domain` thay vì chỉ dùng `doc_name` và `doc_type_name`. Em cũng sẽ cải thiện chunking theo cấu trúc pháp luật, ưu tiên tách theo Điều/Khoản/Điểm để tránh trường hợp top-1 bị nhiễu sang văn bản luật khác như query về hiệu lệnh giao thông. Ngoài ra, em sẽ dùng embedding multilingual thật ngay từ đầu để đánh giá semantic similarity và retrieval sát thực tế hơn.

---

## Tự Đánh Giá

| Tiêu chí | Loại | Điểm tự đánh giá |
|----------|------|-------------------|
| Warm-up | Cá nhân | 5 / 5 |
| Document selection | Nhóm | 9 / 10 |
| Chunking strategy | Nhóm | 13 / 15 |
| My approach | Cá nhân | 10 / 10 |
| Similarity predictions | Cá nhân | 5 / 5 |
| Results | Cá nhân | 9 / 10 |
| Core implementation (tests) | Cá nhân | 30 / 30 |
| Demo | Nhóm | 4 / 5 |
| **Tổng** | | **85 / 100** |
