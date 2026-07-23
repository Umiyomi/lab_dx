"""Generate figures for mock analysis results (stdlib SVG, no external deps)."""

from __future__ import annotations

from pathlib import Path


def _svg_bar_chart(
    title: str,
    labels: list[str],
    values: list[float],
    colors: list[str],
    y_max: float = 5.0,
    width: int = 640,
    height: int = 360,
) -> str:
    margin = {"left": 60, "right": 20, "top": 40, "bottom": 90}
    plot_w = width - margin["left"] - margin["right"]
    plot_h = height - margin["top"] - margin["bottom"]
    n = len(labels)
    bar_w = plot_w / max(n, 1) * 0.6
    gap = plot_w / max(n, 1)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        f'<rect width="100%" height="100%" fill="#fafafa"/>',
        f'<text x="{width/2}" y="24" text-anchor="middle" font-size="16" font-family="sans-serif">{title}</text>',
        f'<line x1="{margin["left"]}" y1="{margin["top"]}" x2="{margin["left"]}" y2="{height - margin["bottom"]}" stroke="#333"/>',
        f'<line x1="{margin["left"]}" y1="{height - margin["bottom"]}" x2="{width - margin["right"]}" y2="{height - margin["bottom"]}" stroke="#333"/>',
    ]

    for i, (label, value, color) in enumerate(zip(labels, values, colors)):
        x = margin["left"] + gap * i + (gap - bar_w) / 2
        bar_h = (value / y_max) * plot_h if y_max else 0
        y = height - margin["bottom"] - bar_h
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_h:.1f}" fill="{color}"/>')
        parts.append(
            f'<text x="{x + bar_w/2:.1f}" y="{height - margin["bottom"] + 16}" '
            f'text-anchor="middle" font-size="11" font-family="sans-serif">{label}</text>'
        )
        parts.append(
            f'<text x="{x + bar_w/2:.1f}" y="{y - 4:.1f}" text-anchor="middle" '
            f'font-size="10" font-family="sans-serif">{value:.2f}</text>'
        )

    parts.append(
        f'<text x="16" y="{margin["top"] + plot_h/2}" transform="rotate(-90 16,{margin["top"] + plot_h/2})" '
        f'text-anchor="middle" font-size="12" font-family="sans-serif">平均体験評価</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts)


def plot_exhibit_ratings(exhibit_means: dict[str, float], output_path: Path) -> None:
    labels = list(exhibit_means.keys())
    values = list(exhibit_means.values())
    svg = _svg_bar_chart(
        "展示別 平均体験評価（mock）",
        labels,
        values,
        ["#4C78A8"] * len(labels),
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(svg, encoding="utf-8")


def plot_romantic_comparison(stats: dict[str, float], output_path: Path) -> None:
    labels = ["ロマンチック文脈", "その他"]
    values = [stats["romantic_context_mean"], stats["other_context_mean"]]
    svg = _svg_bar_chart(
        "文脈別 平均体験評価（mock）",
        labels,
        values,
        ["#F58518", "#54A24B"],
        width=480,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(svg, encoding="utf-8")
