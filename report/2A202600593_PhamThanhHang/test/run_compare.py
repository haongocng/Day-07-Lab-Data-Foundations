import glob
from src.chunking import ChunkingStrategyComparator

# 1. Quét lấy danh sách 2 file đầu tiên trong thư mục dữ liệu
file_paths = glob.glob("data/Data_Law_Transportation/*.md")[:2]

# 2. Khởi tạo đối tượng Comparator
comparator = ChunkingStrategyComparator()

# Chuẩn bị nội dung báo cáo
report_lines = ["# Báo cáo kết quả so sánh các chiến lược Chunking\n"]

# 3. Đọc nội dung từng file và chạy phân tích
for i, path in enumerate(file_paths):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    report_lines.append(f"## Tài liệu {i+1}: `{path}`")
    report_lines.append(f"**Tổng số ký tự:** {len(text)}\n")
    report_lines.append("| Chiến lược | Số lượng Chunk | Độ dài trung bình |")
    report_lines.append("|---|---|---|")
    
    # Gọi hàm compare() để so sánh các chiến lược
    # chunk_size=500 là số lượng ký tự tối đa mong muốn cho mỗi đoạn
    results = comparator.compare(text, chunk_size=500)
    
    # Đưa kết quả chi tiết vào bảng markdown
    for strategy_name, stats in results.items():
        report_lines.append(f"| `{strategy_name}` | {stats['count']} | {stats['avg_length']:.1f} ký tự |")
    
    report_lines.append("\n")

# 4. Ghi báo cáo ra file markdown
with open("compare_report.md", "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

print("Đã xuất báo cáo ra file compare_report.md thành công!")
