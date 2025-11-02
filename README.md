# Competency Dashboard (Python/Streamlit)

人材コンピテンシー（25項目, 0-100）を可視化するダッシュボードの最小構成。  
VS Code + git worktree + 自動テスト/静的解析 + CI を前提にしています。

## Quickstart (macOS)

```bash
# 1) 仮想環境
python3 -m venv .venv
source .venv/bin/activate

# 2) 依存
pip install -r requirements.txt

# 3) サンプルデータで起動
streamlit run app/dashboard.py
```

## テスト＆品質チェック
```bash
# すべてまとめて
ruff check . && black --check . && mypy . && pytest -q
# VS Code: ⌘⇧B で "QA All" を実行
```

## Git worktree で並行開発
```bash
# main と切り離した作業ツリーを2つ用意
git worktree add ../dashboard-feature feature/ui-tweaks
git worktree add ../dashboard-exp    exp/new-visuals
```

## データ
- `sample_data/competencies.csv`: 120人 × 25コンピテンシー（0-100, ダミー）
- 列: `PersonID, Name, Department, C01..C25`

## Streamlit 画面
- **レーダーチャート**（個人）
- **部門×コンピテンシー Heatmap**（平均）
- **コンピテンシー相関 Heatmap**

## CI (GitHub Actions)
- macOS 最新ランナーで `ruff`, `black --check`, `mypy`, `pytest` を実行

2025-11-02T03:49:38.724949
