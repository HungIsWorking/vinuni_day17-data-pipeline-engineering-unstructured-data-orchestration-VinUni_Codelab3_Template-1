from pydantic import BaseModel, Field

# ==========================================
# ROLE 1: LEAD DATA ARCHITECT
# ==========================================

class UnifiedDocument(BaseModel):
    """
    Hợp đồng dữ liệu (Data Contract) chung cho toàn bộ Knowledge Base.
    Mọi nguồn (PDF, Video, ...) sau khi ETL phải fit vào schema này.
    """

    document_id: str = Field(..., description="ID duy nhất của tài liệu (vd: pdf-001, vid_993)")
    source_type: str = Field(..., description="Nguồn gốc dữ liệu: 'PDF' hoặc 'Video'")
    author: str = Field(default="", description="Tác giả / creator. Cho phép rỗng nếu nguồn thiếu.")
    category: str = Field(default="Uncategorized", description="Chủ đề / phân loại nội dung")
    content: str = Field(..., description="Nội dung text đã được làm sạch (bỏ header/footer/noise)")
    timestamp: str = Field(default="", description="Thời điểm tạo / xuất bản (ISO string)")