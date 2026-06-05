import os
import glob
from src.chunking import SentenceChunker

def main():
    data_dir = "data/Data_Law_Transportation"
    # Lấy danh sách tất cả các file .md trong thư mục
    files = glob.glob(os.path.join(data_dir, "*.md"))
    
    if not files:
        print(f"Không tìm thấy file .md nào trong {data_dir}")
        return
        
    print("\n" + "="*50)
    print("DANH SÁCH TÀI LIỆU LUẬT GIAO THÔNG")
    print("="*50)
    
    for i, file_path in enumerate(files):
        print(f"[{i+1}] {os.path.basename(file_path)}")
        
    print("="*50)
    choice = input("Nhập số thứ tự của file bạn muốn chạy thử: ")
    
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(files):
            print("❌ Lựa chọn không hợp lệ!")
            return
    except ValueError:
        print("❌ Vui lòng nhập một số!")
        return
        
    selected_file = files[idx]
    print(f"\nĐang đọc file: {os.path.basename(selected_file)}")
    
    with open(selected_file, 'r', encoding='utf-8') as f:
        text = f.read()
        
    print(f"Tổng số ký tự: {len(text)}")
    print("\n⏳ Đang chạy SentenceChunker của bạn (max_sentences_per_chunk=3)...")
    
    # Chạy chiến lược SentenceChunker
    chunker = SentenceChunker(max_sentences_per_chunk=3)
    chunks = chunker.chunk(text)
    
    print(f"\n✅ KẾT QUẢ:")
    print(f"  - Số lượng Chunk (đoạn): {len(chunks)}")
    if chunks:
        avg_len = sum(len(c) for c in chunks) / len(chunks)
        print(f"  - Độ dài trung bình: {avg_len:.1f} ký tự/chunk")
        
        print("\n" + "-"*50)
        print("👉 XEM THỬ ĐOẠN ĐẦU TIÊN (CHUNK 1):")
        print("-" * 50)
        print(chunks[0])
        print("-" * 50)

if __name__ == "__main__":
    main()
