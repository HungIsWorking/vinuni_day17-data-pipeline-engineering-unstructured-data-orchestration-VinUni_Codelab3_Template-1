import os
import json
import glob

# Import các thành phần
from schema import UnifiedDocument
from process_unstructured import process_pdf_data, process_video_data
from quality_check import run_semantic_checks

# ==========================================
# ROLE 4: DEVOPS & INTEGRATION SPECIALIST
# Wires together the ETL pipeline end-to-end:
#   raw JSON files -> process -> quality gate -> knowledge base JSON
# ==========================================

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(BASE_DIR, "..", "raw_data")
OUTPUT_FILE  = os.path.join(BASE_DIR, "..", "processed_knowledge_base.json")


def run_pipeline():
    final_kb = []

    # ── Group A: PDFs ──────────────────────────────────────────────────────────
    pdf_files = glob.glob(os.path.join(RAW_DATA_DIR, "group_a_pdfs", "*.json"))
    print(f"[Pipeline] Found {len(pdf_files)} PDF file(s) to process.")

    for file_path in pdf_files:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        # Bước 1: Gọi hàm xử lý PDF
        processed = process_pdf_data(raw_data)

        # Bước 2: Kiểm tra chất lượng — chỉ thêm nếu đạt
        if run_semantic_checks(processed):
            # Validate schema (raises ValidationError if fields are missing/wrong type)
            doc = UnifiedDocument(**processed)
            final_kb.append(doc.model_dump())
            print(f"  [OK]  {os.path.basename(file_path)} -> {doc.document_id}")
        else:
            print(f"  [SKIP] {os.path.basename(file_path)} — failed quality gate")

    # ── Group B: Videos ────────────────────────────────────────────────────────
    video_files = glob.glob(os.path.join(RAW_DATA_DIR, "group_b_videos", "*.json"))
    print(f"[Pipeline] Found {len(video_files)} Video file(s) to process.")

    for file_path in video_files:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        # Gọi hàm xử lý Video
        processed = process_video_data(raw_data)

        # Kiểm tra chất lượng — chỉ thêm nếu đạt
        if run_semantic_checks(processed):
            doc = UnifiedDocument(**processed)
            final_kb.append(doc.model_dump())
            print(f"  [OK]  {os.path.basename(file_path)} -> {doc.document_id}")
        else:
            print(f"  [SKIP] {os.path.basename(file_path)} — failed quality gate")

    # ── Lưu kết quả ────────────────────────────────────────────────────────────
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_kb, f, indent=4, ensure_ascii=False)

    print(f"\n[Pipeline] Finished! Saved {len(final_kb)} record(s) -> {OUTPUT_FILE}")


if __name__ == "__main__":
    run_pipeline()
