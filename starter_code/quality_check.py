# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# Semantic Quality Gate — blocks bad records from entering the knowledge base.
# ==========================================

# Minimum acceptable content length (characters)
_MIN_CONTENT_LENGTH = 10

# Keywords that indicate a corrupt / erroneous record
_TOXIC_KEYWORDS = [
    "Null pointer exception",
    "OCR Error",
    "Traceback",
]


def run_semantic_checks(doc_dict: dict) -> bool:
    """
    Validate a processed document dictionary before it is persisted.

    Returns:
        True  — record is clean and should be added to the knowledge base.
        False — record failed one or more checks and must be discarded.

    Checks performed:
        1. Content length: content must be ≥ _MIN_CONTENT_LENGTH characters.
        2. Toxic keyword filter: content must not contain known error strings.
    """
    content = doc_dict.get("content", "")

    # 1. Kiểm tra độ dài: Nếu content trống hoặc < 10 ký tự -> False
    if len(content) < _MIN_CONTENT_LENGTH:
        return False

    # 2. Kiểm tra từ khóa lỗi
    for keyword in _TOXIC_KEYWORDS:
        if keyword in content:
            return False

    return True
