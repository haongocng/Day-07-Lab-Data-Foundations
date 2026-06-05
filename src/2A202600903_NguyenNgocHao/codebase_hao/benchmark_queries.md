# Benchmark Queries & Gold Answers
# Phase 2 - Group Task: Vietnamese Legal Documents

## Query 1: Factual (Simple)
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

---

## Query 2: Factual (Specific Regulation)
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

---

## Query 3: Multi-paragraph (Complex Information)
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

---

## Query 4: Metadata-sensitive (Document Name Filtering)
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

**Note:** Query này test khả năng filter theo `doc_name` để chỉ tìm trong văn bản cụ thể.

---

## Query 5: Multi-paragraph (Policy & Principles)
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

---

## Summary

| Query | Type | Complexity | Metadata Filter | Expected Chunks |
|-------|------|------------|-----------------|-----------------|
| Q1 | Factual | Low | doc_type_name | 1 chunk |
| Q2 | Factual | Low | doc_type_name | 1 chunk |
| Q3 | Multi-paragraph | Medium | doc_type_name | 2-3 chunks |
| Q4 | Metadata-sensitive | Medium | doc_name | 1-2 chunks |
| Q5 | Multi-paragraph | High | doc_type_name | 3-4 chunks |

## Testing Strategy

### Without Metadata Filter
```python
results = store.search(query, top_k=3)
```

### With Metadata Filter
```python
# Filter by document type (Luật vs Dự thảo)
results = store.search_with_filter(
    query=query,
    top_k=3,
    metadata_filter={"doc_type_name": "Luật"}
)

# Filter by specific document
results = store.search_with_filter(
    query=query,
    top_k=3,
    metadata_filter={"doc_name": "Luật Giao thông đường bộ số 23-2008-QH12 của Quốc hội"}
)
```

### Expected Improvements with Filtering:
- **Q1, Q2, Q3, Q5**: Should return only official laws (Luật), not drafts (Dự thảo)
- **Q4**: Should return only chunks from the specific 2024 law document
