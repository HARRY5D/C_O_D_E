"""
Section Detector — automatically identifies tax law sections in extracted text.
Detects sections like 80C, 80D, 24(b), 10(13A), etc.
"""
import re
from typing import List, Dict, Any


# Patterns for common tax sections
SECTION_PATTERNS = [
    # Format: Section 80C, Sec. 80C, u/s 80C, under section 80C
    (r"\b[Ss]ection\s+(\d+[A-Z]?(?:\([^)]+\))*)\b", "section"),
    (r"\b[Ss]ec\.\s*(\d+[A-Z]?(?:\([^)]+\))*)\b", "section"),
    (r"\bu/s\s+(\d+[A-Z]?(?:\([^)]+\))*)\b", "section"),
    (r"\bRule\s+(\d+[A-Z]?(?:\([^)]+\))*)\b", "rule"),
    (r"\bSchedule\s+([IVXLCDM]+)\b", "schedule"),
]

# Known important sections → topic mapping
SECTION_TOPIC_MAP = {
    "80C": "deduction_investments",
    "80CCC": "deduction_pension",
    "80CCD": "deduction_nps",
    "80CCD(1)": "deduction_nps_employee",
    "80CCD(1B)": "deduction_nps_additional",
    "80CCD(2)": "deduction_nps_employer",
    "80D": "deduction_health_insurance",
    "80E": "deduction_education_loan",
    "80G": "deduction_donation",
    "80GG": "deduction_rent",
    "80TTA": "deduction_savings_interest",
    "80TTB": "deduction_senior_savings",
    "24": "home_loan_interest",
    "24(b)": "home_loan_interest",
    "10(13A)": "hra_exemption",
    "10(5)": "lta_exemption",
    "10(10D)": "life_insurance_maturity",
    "87A": "rebate",
    "115BAC": "new_regime",
    "44ADA": "presumptive_professional",
    "44AD": "presumptive_business",
    "112A": "ltcg_equity",
    "111A": "stcg_equity",
}


def detect_sections(text: str) -> List[str]:
    """Find all section references mentioned in a text block."""
    found = set()
    for pattern, _ in SECTION_PATTERNS:
        matches = re.findall(pattern, text)
        found.update(matches)
    return sorted(found)


def get_primary_section(text: str) -> str:
    """Return the most prominent section in the text (first match)."""
    for pattern, _ in SECTION_PATTERNS:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return "general"


def get_topic(section: str) -> str:
    """Map a section number to a topic label."""
    return SECTION_TOPIC_MAP.get(section, "general_tax_law")


def tag_page_with_sections(page: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich a page dict with section detection metadata."""
    text = page.get("text", "")
    sections = detect_sections(text)
    primary = get_primary_section(text)
    topic = get_topic(primary)

    return {
        **page,
        "sections_found": sections,
        "primary_section": primary,
        "topic": topic,
    }
