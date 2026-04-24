from pydantic import BaseModel, Field

# ==========================================
# ROLE 1: LEAD DATA ARCHITECT
# Unified schema that every data source must conform to.
# ==========================================

class UnifiedDocument(BaseModel):
    """
    Chuẩn dữ liệu duy nhất (Unified Schema) cho toàn hệ thống.
    Mọi nguồn (PDF, Video...) phải được chuẩn hoá về 6 trường dưới đây
    trước khi ghi vào knowledge base.
    """
    document_id: str = Field(..., description="Unique identifier of the document")
    source_type:  str = Field(..., description="Origin type: 'PDF' or 'Video'")
    author:       str = Field(..., description="Author or creator name")
    category:     str = Field(..., description="Subject/topic category")
    content:      str = Field(..., description="Cleaned main body text / transcript")
    timestamp:    str = Field(..., description="Creation or publication timestamp")
