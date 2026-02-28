# 🤖 Ad AI Auto — 広告AI自動運用ツール

[AgentKits Marketing](https://github.com/aitytech/agentkits-marketing)をベースにした、AI駆動の広告自動運用プラットフォーム。

## 🎯 できること

| 機能 | 説明 |
|------|------|
| **広告文AI生成** | 製品情報を入力→Google RSA/Meta広告コピーを自動生成＆バリデーション |
| **自動入稿** | Google Ads / Meta Ads APIで広告を自動作成 |
| **パフォーマンス分析** | AIがCTR・ROAS・CPAを分析し改善アクションを提案 |
| **入札自動最適化** | パフォーマンスデータに基づきAIが入札・予算を自動調整 |
| **Telegram通知** | 日次レポート・異常アラート・承認フローをTelegramに配信 |
| **マーケティング知識** | 18エージェント・93コマンド・28スキルの総合マーケ基盤（AgentKitsベース） |

## 📁 プロジェクト構成

```
src/
├── config.py                        # 環境変数設定
├── core/
│   ├── ad_generator.py             # AI広告文生成エンジン
│   └── optimizer.py                # AI入札最適化エンジン
└── integrations/
    ├── google-ads/client.py        # Google Ads API連携
    ├── meta-ads/client.py          # Meta Ads API連携
    └── telegram/notifier.py        # Telegram通知
```

## 🚀 セットアップ

```bash
# 依存パッケージインストール
pip install -r requirements.txt

# 環境変数設定
cp .env.example .env
# .envファイルを編集してAPIキーを設定
```

## 📋 必要なAPIキー

1. **Google Ads API** — [developers.google.com/google-ads/api](https://developers.google.com/google-ads/api/docs/first-call/overview)
2. **Meta Marketing API** — [developers.facebook.com](https://developers.facebook.com/docs/marketing-apis/)
3. **Anthropic API** or **OpenAI API** — AI広告文生成・分析用
4. **Telegram Bot Token** — 通知配信用

## 🔄 ロードマップ

- [x] Phase 1: 基盤（API連携骨格、AI生成、通知）
- [ ] Phase 2: コア機能（自動入稿フロー、日次レポート）
- [ ] Phase 3: 自動最適化（入札自動調整、A/Bテスト）
- [ ] Phase 4: ダッシュボード（リアルタイム可視化）

## 📜 ライセンス

MIT License（AgentKits Marketingベース）
