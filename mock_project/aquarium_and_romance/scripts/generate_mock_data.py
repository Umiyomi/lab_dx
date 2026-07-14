"""Generate synthetic survey responses and processed analysis dataset."""

from __future__ import annotations

import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOCK_DIR = ROOT / "data" / "mock"
PROCESSED_DIR = ROOT / "data" / "processed"

AGE_GROUPS = ["10代", "20代", "30代", "40代", "50代以上"]
VISIT_PURPOSES = ["デート", "家族レジャー", "友人とのレジャー", "一人での観光", "その他"]
COMPANIONS = ["恋人・配偶者", "家族", "友人", "一人", "その他"]
EXHIBITS = ["クラゲゾーン", "ペンギン館", "イルカショー", "熱帯魚トンネル", "触れ合いプール", "その他"]
EMOTIONS = ["ワクワク", "癒し", "感動", "ロマンチック", "驚き", "特にない"]
REVISIT = ["ぜひ行きたい", "行きたい", "どちらとも言えない", "行きたくない"]

RAW_FIELDS = [
    "respondent_id",
    "age_group",
    "visit_purpose",
    "companion",
    "memorable_exhibit",
    "experience_rating",
    "primary_emotion",
    "emotion_intensity",
    "revisit_intention",
]


def _biased_rating(purpose: str, companion: str) -> int:
    base = 3
    if purpose == "デート" or companion == "恋人・配偶者":
        base += 1
    return max(1, min(5, base + random.choice([-1, 0, 0, 1])))


def _pick_emotion(purpose: str, companion: str) -> str:
    if purpose == "デート" or companion == "恋人・配偶者":
        return random.choice(["ロマンチック", "癒し", "感動", "ワクワク"])
    return random.choice(EMOTIONS)


def _pick_revisit(rating: int, intensity: int) -> str:
    score = rating + intensity
    if score >= 8:
        return random.choice(["ぜひ行きたい", "行きたい"])
    if score >= 6:
        return random.choice(["行きたい", "どちらとも言えない"])
    return random.choice(["どちらとも言えない", "行きたくない"])


def generate_rows(n: int = 120, seed: int = 42) -> list[dict[str, str | int | bool]]:
    random.seed(seed)
    rows: list[dict[str, str | int | bool]] = []

    for i in range(1, n + 1):
        purpose = random.choice(VISIT_PURPOSES)
        companion = random.choice(COMPANIONS)
        rating = _biased_rating(purpose, companion)
        emotion = _pick_emotion(purpose, companion)
        intensity = max(1, min(5, rating + random.choice([-1, 0, 1])))
        revisit = _pick_revisit(rating, intensity)
        romantic = purpose == "デート" or companion == "恋人・配偶者"

        rows.append(
            {
                "respondent_id": f"R{i:03d}",
                "age_group": random.choice(AGE_GROUPS),
                "visit_purpose": purpose,
                "companion": companion,
                "memorable_exhibit": random.choice(EXHIBITS),
                "experience_rating": rating,
                "primary_emotion": emotion,
                "emotion_intensity": intensity,
                "revisit_intention": revisit,
                "is_romantic_context": romantic,
            }
        )

    return rows


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = generate_rows()
    raw_rows = [{k: v for k, v in row.items() if k in RAW_FIELDS} for row in rows]
    write_csv(MOCK_DIR / "survey_responses_mock.csv", raw_rows, RAW_FIELDS)
    write_csv(PROCESSED_DIR / "analysis_dataset.csv", rows, RAW_FIELDS + ["is_romantic_context"])
    print(f"Wrote {MOCK_DIR / 'survey_responses_mock.csv'}")
    print(f"Wrote {PROCESSED_DIR / 'analysis_dataset.csv'}")


if __name__ == "__main__":
    main()
