# データ辞書

| 項目 | 内容 |
|------|------|
| dataset | `analysis_dataset` |
| source | mock survey responses（合成データ） |
| version | 1.0 |

## 変数一覧

| 変数名 | 型 | 説明 |
|--------|-----|------|
| `respondent_id` | string | 回答者ID（匿名化） |
| `age_group` | categorical | 年齢区分（Q1）。値: 10代 / 20代 / 30代 / 40代 / 50代以上 |
| `visit_purpose` | categorical | 訪問目的（Q2） |
| `companion` | categorical | 同伴者（Q3） |
| `memorable_exhibit` | categorical | 印象的な展示（Q4） |
| `experience_rating` | integer | 体験全体の評価（Q5, 1–5） |
| `primary_emotion` | categorical | 主な感情（Q6 から代表値を抽出） |
| `emotion_intensity` | integer | 感情の強さ（Q7, 1–5） |
| `revisit_intention` | categorical | 再訪意向（Q8） |
| `is_romantic_context` | boolean | デート目的または恋人同伴か（派生変数） |

## 備考

- Q6 は複数選択だが、モックでは `primary_emotion` として1値に集約する。
- 設問定義の正本は `docs/questionnaire/questionnaire.md`。
