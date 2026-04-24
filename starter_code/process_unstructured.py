import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# The Transformation Lead
# - Parses messy JSON outputs from OCR/Speech-to-Text services
# - Translates camelCase (PDF) and snake_case (Video) into UnifiedDocument schema
# - Cleans up "noise" (HEADER_PAGE_X, FOOTER_PAGE_X, music tags, trailing spaces)
# ==========================================

# Noise patterns to strip from PDF text
_NOISE_PATTERN = re.compile(
    r"(HEADER_PAGE_\d+|FOOTER_PAGE_\d+)",
    flags=re.IGNORECASE,
)

# Noise patterns to strip from video transcripts (e.g. [Music playing], [Applause])
_TRANSCRIPT_NOISE_PATTERN = re.compile(
    r"\[.*?\]",
    flags=re.IGNORECASE,
)


def _clean_pdf_text(raw_text: str) -> str:
    """Remove HEADER_PAGE_X / FOOTER_PAGE_X tokens and collapse extra whitespace."""
    text = _NOISE_PATTERN.sub("", raw_text)
    # Collapse multiple spaces/newlines into a single space, then strip edges
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _clean_transcript(raw_text: str) -> str:
    """Remove bracketed noise tags from video transcripts."""
    text = _TRANSCRIPT_NOISE_PATTERN.sub("", raw_text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def process_pdf_data(raw_json: dict) -> dict:
    """
    Parse a raw OCR JSON record from Group A (PDFs).

    Raw format (camelCase):
        docId, authorName, docCategory, extractedText, createdAt

    Unified format (snake_case):
        document_id, source_type, author, category, content, timestamp
    """
    # Bước 1: Làm sạch nhiễu (Header/Footer) khỏi văn bản
    raw_text = raw_json.get("extractedText", "")
    cleaned_content = _clean_pdf_text(raw_text)

    # Bước 2: Map dữ liệu thô sang định dạng chuẩn của UnifiedDocument
    return {
        "document_id": raw_json.get("docId", ""),
        "source_type":  "PDF",
        "author":        raw_json.get("authorName", "Unknown").strip(),
        "category":      raw_json.get("docCategory", "Uncategorized"),
        "content":       cleaned_content,
        "timestamp":     raw_json.get("createdAt", ""),
    }


def process_video_data(raw_json: dict) -> dict:
    """
    Parse a raw Speech-to-Text JSON record from Group B (Videos).

    Raw format (snake_case):
        video_id, creator_name, transcript, category, published_timestamp

    Unified format (snake_case):
        document_id, source_type, author, category, content, timestamp
    """
    # Làm sạch nhiễu từ transcript (music tags, v.v.)
    raw_transcript = raw_json.get("transcript", "")
    cleaned_content = _clean_transcript(raw_transcript)

    # Map sang định dạng chuẩn
    return {
        "document_id": raw_json.get("video_id", ""),
        "source_type":  "Video",
        "author":        raw_json.get("creator_name", "Unknown").strip(),
        "category":      raw_json.get("category", "Uncategorized"),
        "content":       cleaned_content,
        "timestamp":     raw_json.get("published_timestamp", ""),
    }
