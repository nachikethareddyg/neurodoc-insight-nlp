from pathlib import Path
import re
from collections import Counter


STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "with", "for", "to", "of", "in", "on",
    "no", "not", "has", "have", "been", "is", "are", "was", "were", "be", "as",
    "this", "that", "it", "at", "by", "from", "into", "up", "down", "over",
    "patient", "reports", "denies", "recommended"
}

MEDICAL_HINTS = {
    "headache", "nausea", "fever", "migraine", "pain", "chest", "breath",
    "hydration", "rest", "sleep", "shortness"
}


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\.]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_keywords(text: str, top_k: int = 8):
    tokens = [t for t in re.split(r"\s+", text) if t and t not in STOPWORDS]
    counts = Counter(tokens)
    return counts.most_common(top_k)


def simple_summary(original_text: str) -> str:
    # Simple: take first 1–2 sentences as summary
    sentences = re.split(r"(?<=[\.])\s+", original_text.strip())
    summary = " ".join(sentences[:2]).strip()
    return summary if summary else original_text.strip()


def extract_medical_terms(text: str):
    tokens = set(re.split(r"\s+", text))
    found = sorted([t for t in tokens if t in MEDICAL_HINTS])
    return found


def main():
    repo_root = Path(__file__).resolve().parents[1]
    note_path = repo_root / "data" / "sample_note.txt"

    original = note_path.read_text(encoding="utf-8")
    cleaned = clean_text(original)

    keywords = extract_keywords(cleaned)
    med_terms = extract_medical_terms(cleaned)
    summary = simple_summary(original)

    print("\n=== NeuroDoc Insight (Demo) ===\n")
    print("Summary:")
    print(summary)

    print("\nMedical Terms Detected:")
    print(", ".join(med_terms) if med_terms else "None")

    print("\nTop Keywords:")
    for word, freq in keywords:
        print(f"- {word}: {freq}")

    print("\nInput file:", note_path)


if __name__ == "__main__":
    main()
