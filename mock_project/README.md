# データ管理構造のモック
標準リポジトリ構成を`mock_project`に、NASの構想を`nas_mock`に配している。

## 検討事項
### 中間生成物をどこに置くか
機密と成果の散逸を防ぐために、一切の中間生成物をローカルに保存せずNAS送りにするという運用は難しいか

```
.
├── README.md
└── mock_project
    ├── aquarium_and_romance
    │   ├── README.md
    │   ├── data
    │   ├── docs
    │   ├── main.py
    │   ├── metadata
    │   ├── pyproject.toml
    │   ├── results
    │   ├── scripts
    │   ├── src
    │   └── uv.lock
    └── nas_mock
        ├── project
        └── raw
```