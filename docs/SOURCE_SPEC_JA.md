# 📋 AgentKits Marketing — ソースコード仕様書

> フォーク元: [aitytech/agentkits-marketing](https://github.com/aitytech/agentkits-marketing)
> ライセンス: MIT
> バージョン: main branch (2026-02-28時点)

---

## 1. プロジェクト概要

| 項目 | 値 |
|------|------|
| 総ファイル数 | 3,444 |
| Markdownファイル数 | 570 |
| 総行数 | 129,189行 |
| エージェント数 | 20 |
| スキル数 | 28 |
| コマンド数 | 93+ |
| ワークフロー数 | 7 |
| プラグイン数 | 2 |
| 外部連携数 | 14 |
| 対応言語 | 11言語 (EN/ZH/JA/KO/ES/DE/FR/PT-BR/VI/RU/AR) |
| トレーニング | 11言語×約20レッスン |

**設計思想**: Claude Code / Cursor / GitHub Copilot等のAIアシスタントの「スキル」として動作するマーケティング自動化フレームワーク。コードを書くのではなく、**AIエージェントへの指示書（Markdown）の集合体**。

---

## 2. ディレクトリ構成

```
agentkits-marketing/
│
├── .claude/                        # ★ コア（AIアシスタントの頭脳）
│   ├── agents/          (20個)     # 専門AIエージェント定義
│   ├── commands/        (93個)     # スラッシュコマンド定義
│   ├── skills/          (28個)     # 専門スキル（知識ベース）
│   ├── workflows/       (7個)      # 業務フロー定義
│   ├── components/      (2個)      # 再利用可能UIコンポーネント
│   ├── settings.json               # Claude Code設定
│   └── metadata.json               # プラグインメタデータ
│
├── .claude-plugin/                 # プラグインマニフェスト
│   ├── plugin.json                 # プラグイン定義
│   └── marketplace.json            # マーケットプレイス情報
│
├── plugins/                        # 拡張プラグイン
│   ├── campaign-manager/           # キャンペーン管理プラグイン
│   └── content-factory/            # コンテンツ量産プラグイン
│
├── training/                       # インタラクティブ学習モジュール
│   ├── exercises/                  # 実践演習データ
│   └── README.md
│
├── src/                            # ★ 独自追加（Ad AI Auto）
│   ├── config.py
│   ├── core/                       # AI広告文生成・最適化エンジン
│   └── integrations/               # Google/Meta/Telegram連携
│
├── docs/                           # ドキュメント
├── bin/                            # CLIスクリプト
└── README.md (+ 11言語版)
```

---

## 3. エージェント一覧（20体）

### 3.1 マーケティングファネル別配置

```
認知(TOFU)          検討(MOFU)           購入(BOFU)          継続
─────────          ─────────           ─────────          ─────────
attraction-        lead-               sales-             continuity-
specialist         qualifier           enabler            specialist
    │                  │                   │                   │
seo-specialist     email-wizard        conversion-        upsell-
    │                  │               optimizer          maximizer
researcher         persona-               │
    │              builder            copywriter
brainstormer           │
                   planner
```

### 3.2 エージェント詳細

| # | エージェント | 役割 | AIモデル | 主な用途 |
|---|------------|------|---------|---------|
| 1 | **attraction-specialist** | リード獲得・TOFU専門 | Sonnet | キーワードリサーチ、LP生成、プログラマティックSEO |
| 2 | **brainstormer** | キャンペーンアイデア創出 | Sonnet | ブレスト、クリエイティブコンセプト、メッセージング |
| 3 | **brand-voice-guardian** | ブランド一貫性チェック | Sonnet | コンテンツのトーン・スタイル検証 |
| 4 | **command-helper** | コマンド案内 | Sonnet | ユーザーの意図→最適コマンド提案 |
| 5 | **continuity-specialist** | 顧客維持 | Sonnet | チャーン検知、再エンゲージメント、NPS |
| 6 | **conversion-optimizer** | CRO専門 | Sonnet | LP・メール・広告のCV率最適化 |
| 7 | **copywriter** | コピーライティング | Sonnet | 広告文、LP、メール、SNS投稿の文章作成 |
| 8 | **docs-manager** | ドキュメント管理 | Sonnet | ブランドガイドライン、マーケ資料整理 |
| 9 | **email-wizard** | メールマーケ | Sonnet | シーケンス設計、パーソナライゼーション、A/Bテスト |
| 10 | **lead-qualifier** | リードスコアリング | Sonnet | 行動分析、エンゲージメント判定、営業連携 |
| 11 | **mcp-manager** | MCP統合管理 | Sonnet | 外部ツール連携、APIディスカバリー |
| 12 | **persona-builder** | ペルソナ構築 | Sonnet | 対話型顧客プロファイル作成 |
| 13 | **planner** | キャンペーン計画 | Sonnet | マーケ計画、予算配分、スケジュール |
| 14 | **project-manager** | プロジェクト管理 | Sonnet | 進捗追跡、タスク調整、ステータスレポート |
| 15 | **researcher** | 市場調査 | Sonnet | 競合分析、オーディエンスインサイト、トレンド |
| 16 | **sales-enabler** | 営業支援 | Sonnet | ピッチ作成、反論対応スクリプト、ソーシャルプルーフ |
| 17 | **seo-specialist** | SEO最適化 | Sonnet | キーワード最適化、テクニカルSEO、コンテンツSEO |
| 18 | **solopreneur** | 個人事業主ペルソナ | Sonnet | フリーランス・小規模事業の視点でレビュー |
| 19 | **startup-founder** | スタートアップ創業者ペルソナ | Sonnet | グロースハック・バイラリティの視点でレビュー |
| 20 | **upsell-maximizer** | 収益拡大 | Sonnet | アップセル機会発見、機能利用率分析 |

### 3.3 エージェントの共通仕様

```yaml
# 各エージェントMDファイルの構成
---
name: エージェント名
version: "1.0.0"
brand: AgentKits Marketing by AityTech
description: 用途説明 + 呼び出し例
model: sonnet
---

## 本体
1. Language Directive    # ユーザー言語の自動検出・対応
2. Context Loading       # 実行前にプロジェクト情報を読み込む手順
3. Reasoning Process     # 思考の手順（ステップバイステップ）
4. Skill Integration     # 関連スキルの自動ロード
5. Data Reliability      # データ信頼性ルール（捏造禁止）
6. Output Format         # 出力フォーマット定義
```

---

## 4. スキル一覧（28個）

### 4.1 カテゴリ別分類

#### 🎯 広告・集客（Ad AI Auto で最重要）
| スキル | 説明 | リファレンス |
|-------|------|------------|
| **paid-advertising** | 有料広告戦略。Google/Meta/TikTok/LinkedIn対応 | Google Ads, Meta Ads, TikTok Ads, LinkedIn Ads, メディアプレイブック |
| **seo-mastery** | SEO総合。キーワード、テクニカル、リンク構築 | キーワードリサーチ、テクニカルSEO、リンク構築、ローカルSEO等7件 |
| **programmatic-seo** | プログラマティックSEO。テンプレ大量ページ生成 | 1件 |
| **social-media** | SNS戦略。プラットフォーム別最適化 | アルゴリズム、エンゲージメント、コンテンツ戦略等5件 |

#### ✍️ コンテンツ・コピー
| スキル | 説明 | リファレンス |
|-------|------|------------|
| **copywriting** | マーケティングコピー全般 | フレームワーク集1件 |
| **copy-editing** | 既存コピーの編集・改善 | チェックリスト1件 |
| **content-strategy** | コンテンツ計画・配信戦略 | ピラー、プレイブック、カレンダー等5件 |
| **marketing-ideas** | 140+のSaaSマーケ戦略集 | 1件 |
| **marketing-psychology** | 70+のメンタルモデル・行動心理学 | 1件 |

#### 📧 メール・シーケンス
| スキル | 説明 | リファレンス |
|-------|------|------------|
| **email-marketing** | メールキャンペーン戦略・自動化 | 配信性、自動化、セグメント等6件 |
| **email-sequence** | ドリップキャンペーン・ライフサイクルメール | 1件 |

#### 📈 CRO（コンバージョン率最適化）
| スキル | 説明 | リファレンス |
|-------|------|------------|
| **page-cro** | LP・ホームページのCV最適化 | テンプレート、チェックリスト2件 |
| **form-cro** | フォーム最適化（リード獲得、問い合わせ等） | 1件 |
| **signup-flow-cro** | サインアップフロー最適化 | 1件 |
| **onboarding-cro** | ユーザーオンボーディング最適化 | 1件 |
| **popup-cro** | ポップアップ・モーダル最適化 | 1件 |
| **paywall-upgrade-cro** | アプリ内アップセル画面最適化 | 1件 |

#### 🏗️ ブランド・戦略
| スキル | 説明 | リファレンス |
|-------|------|------------|
| **brand-building** | ブランド戦略・アイデンティティ構築 | 戦略、ポジショニング、ビジュアル等5件 |
| **marketing-fundamentals** | マーケ基礎（ファネル、顧客旅行、VP） | 心理学、フレームワーク等6件 |
| **pricing-strategy** | 価格戦略・パッケージング | 1件 |
| **launch-strategy** | 製品ローンチ戦略 | 1件 |
| **free-tool-strategy** | 無料ツールによるリード獲得 | 1件 |
| **referral-program** | 紹介プログラム設計 | 1件 |
| **competitor-alternatives** | 競合比較ページ作成 | 1件 |

#### 🔧 分析・技術
| スキル | 説明 | リファレンス |
|-------|------|------------|
| **analytics-attribution** | アトリビューション・ROI分析 | GA4実装、アトリビューションモデル等6件 |
| **ab-test-setup** | A/Bテスト設計・統計 | 統計ガイド1件 |
| **schema-markup** | 構造化データ・リッチスニペット | 1件 |
| **problem-solving** | 問題解決フレームワーク | 7件 |

### 4.2 スキルの共通構成

```yaml
---
name: スキル名
version: "1.0.0"
category: core
difficulty: beginner|intermediate|advanced
description: 発動条件・トリガーワード
triggers: [キーワードリスト]
prerequisites: [前提スキル]
related_skills: [関連スキル]
agents: [使用エージェント]
mcp_integrations:
  optional: [連携MCP]
success_metrics: [KPI]
---

# スキル本体
1. When to Use        # 発動条件
2. Core Concepts      # 基礎知識
3. Step-by-Step       # 実行手順
4. Templates          # テンプレート
5. Best Practices     # ベストプラクティス
6. References/        # 参考資料（別ファイル）
```

---

## 5. コマンド一覧（93個）

### 5.1 カテゴリ別

| カテゴリ | コマンド数 | 主なコマンド |
|---------|-----------|------------|
| **campaign/** | 4 | `plan`, `brief`, `calendar`, `analyze` |
| **content/** | 10 | `ads`, `blog`, `email`, `landing`, `social`, `cro`, `editing`, `enhance`, `fast`, `good` |
| **seo/** | 6 | `keywords`, `audit`, `competitor`, `optimize`, `programmatic`, `schema` |
| **cro/** | 6 | `page`, `form`, `popup`, `signup`, `onboarding`, `paywall` |
| **analytics/** | 3 | `report`, `funnel`, `roi` |
| **brand/** | 3 | `assets`, `book`, `voice` |
| **competitor/** | 2 | `alternatives`, `deep` |
| **leads/** | 3 | `qualify`, `score`, `nurture` |
| **sales/** | 4 | `battlecard`, `outreach`, `pitch`, `qualify` |
| **crm/** | 4 | `lifecycle`, `score`, `segment`, `sequence` |
| **sequence/** | 3 | `welcome`, `nurture`, `re-engage` |
| **growth/** | 3 | `launch`, `referral`, `free-tool` |
| **social/** | 3 | `engage`, `schedule`, `viral` |
| **research/** | 3 | `market`, `persona`, `trend` |
| **report/** | 2 | `weekly`, `monthly` |
| **ops/** | 3 | `daily`, `weekly`, `monthly` |
| **checklist/** | 6 | `campaign-launch`, `ab-testing`, `analytics-monthly`, `content-approval`, `seo-weekly`, `social-daily` |
| **marketing/** | 2 | `ideas`, `psychology` |
| **pricing/** | 1 | `strategy` |
| **test/** | 1 | `ab-setup` |
| **audit/** | 1 | `full` |
| **brainstorm** | 1 | (ルート) |
| **settings/** | 1 | `preferences` |
| **skills/** | 1 | `select` |
| **training/** | 20+/言語 | インタラクティブトレーニング |

### 5.2 広告運用で特に重要なコマンド

```
/content:ads          # 広告コピー生成（Google/Meta/TikTok/LinkedIn対応）
/campaign:plan        # キャンペーン戦略策定
/campaign:brief       # クリエイティブブリーフ作成
/campaign:analyze     # キャンペーン分析
/campaign:calendar    # コンテンツカレンダー生成
/seo:keywords         # キーワードリサーチ
/analytics:roi        # ROI分析
/analytics:report     # パフォーマンスレポート
/test:ab-setup        # A/Bテスト設計
/competitor:deep      # 競合深掘り分析
```

---

## 6. ワークフロー（7個）

### 6.1 Primary Marketing Workflow（メインフロー）
```
Research → Insights → Creative → Plan → Create → Edit → Publish → Measure
   │           │          │        │       │       │        │        │
researcher  planner  copywriter  planner  各agent  copy-   -      analytics
                    brainstormer         editor
```

### 6.2 Sales Workflow
```
Lead → MQL → SQL → Opportunity → Proposal → Negotiation → Closed
  │     │     │        │            │            │
lead- lead- sales-   sales-     copywriter    sales-
qualifier qualifier enabler    enabler                 enabler
```

### 6.3 CRM Workflow
```
Subscriber → Lead → MQL → SQL → Opportunity → Customer → Advocate
                                                    │
                                              continuity-specialist
                                              upsell-maximizer
```

### 6.4 その他のワークフロー
| ワークフロー | 目的 |
|------------|------|
| **orchestration-protocol** | エージェント間の連携プロトコル（逐次/並列チェーン） |
| **data-reliability-rules** | データ信頼性ルール（捏造禁止、ソース階層） |
| **documentation-management** | ドキュメント管理・更新ルール |
| **marketing-rules** | コンテンツ品質基準（可読性、見出し、CTA） |

---

## 7. プラグイン（2個）

### 7.1 Campaign Manager
```
plugins/campaign-manager/
├── PLUGIN.md
├── agents/
│   ├── marketing-manager.md     # キャンペーン統括
│   ├── seo-specialist.md        # SEO特化版
│   ├── conversion-optimizer.md  # CRO特化版
│   ├── solopreneur.md           # 個人事業主ペルソナ
│   ├── brand-voice-guardian.md  # ブランドチェック
│   └── startup-founder.md       # スタートアップペルソナ
├── templates/
│   ├── campaign-brief.md        # ブリーフテンプレート
│   ├── content-calendar.md      # カレンダーテンプレート
│   └── email-sequence.md        # メールシーケンステンプレート
└── commands/
    └── plan.md                  # キャンペーン計画コマンド
```

### 7.2 Content Factory
```
plugins/content-factory/
├── PLUGIN.md
├── templates/
│   ├── blog-template.md         # ブログ記事テンプレート
│   ├── social-media-template.md # SNS投稿テンプレート
│   └── video-script-template.md # 動画スクリプトテンプレート
└── commands/
    ├── generate.md              # コンテンツ一括生成
    ├── repurpose.md             # コンテンツ転用（ブログ→SNS等）
    └── schedule.md              # スケジュール生成
```

---

## 8. 外部連携（MCP Integrations）14サービス

| サービス | カテゴリ | 用途 |
|---------|---------|------|
| **Google Analytics** | アナリティクス | Webトラフィック分析、CV計測 |
| **Google Search Console** | SEO | 検索パフォーマンス、インデックス状況 |
| **Meta Ads** | 広告 | Facebook/Instagram広告データ |
| **TikTok** | 広告/SNS | TikTok広告・コンテンツ |
| **Twitter/X** | SNS | ソーシャルメディア連携 |
| **LinkedIn** | SNS/B2B | ビジネスSNS連携 |
| **HubSpot** | CRM | 顧客管理・マーケ自動化 |
| **Semrush** | SEO | キーワードリサーチ・競合分析 |
| **DataForSEO** | SEO | SEOデータAPI |
| **Notion** | プロジェクト管理 | コンテンツ管理・タスク管理 |
| **Asana** | プロジェクト管理 | タスク・プロジェクト管理 |
| **Slack** | コミュニケーション | チーム通知・連携 |
| **LINE** | メッセージング | LINE公式アカウント連携 |
| **Zalo** | メッセージング | Zalo連携（ベトナム市場向け） |
| **Crosspost** | コンテンツ配信 | マルチプラットフォーム同時投稿 |

---

## 9. トレーニングシステム

### 構成
- **11言語対応**: EN, JA, ZH, KO, ES, DE, FR, PT-BR, VI, RU, AR
- **3モジュール × 各7-8レッスン**
- **実践演習付き**: `training/exercises/markit/` に架空マーケ会社のデータ
- **所要時間**: 約4-6時間

### モジュール構成
```
Module 0: Getting Started (30min)
  ├── 0-0: コース紹介
  ├── 0-1: セットアップ確認
  └── 0-2: 最初のマーケタスク

Module 1: Core Skills (2h)
  ├── 1-1〜1-7: 基本スキルの習得
  └── ブランド、SEO、コンテンツ、メール等

Module 2: Advanced (2h)
  ├── 2-1〜2-6: 応用スキル
  └── CRO、A/Bテスト、プログラマティックSEO等

Module 3: Mastery (1h)
  ├── 3-1〜3-3: 統合演習
  └── フルキャンペーン設計・実行

Bonus:
  ├── bonus-patterns: マーケパターン集
  ├── bonus-secret: 隠し機能
  └── persona-builder: ペルソナ構築演習
```

---

## 10. UIコンポーネント

### Interactive Questions Component
全コマンドで共通の対話型質問パターン：
- AskUserQuestion ツールで構造化入力
- 1問ずつプログレッシブ開示
- 各質問2-4選択肢 + "Other"オプション
- 最大5-7問/フロー
- 実行前に確認サマリー表示

### Date Helpers Component
日付処理ユーティリティ：
- キャンペーン期間の計算
- スケジュール生成
- タイムゾーン対応

---

## 11. データ信頼性ルール（全エージェント共通）

**最重要ルール**: データの捏造禁止

### データソース信頼度階層
```
Tier 1 (最高): MCP統合（リアルタイムAPI）
  → Google Analytics, Search Console, Semrush等

Tier 2 (高): プロジェクト内ドキュメント
  → docs/, content/, brand guidelines

Tier 3 (中): Web検索結果
  → 要ソース明記

Tier 4 (低): AI推論
  → 必ず「推定」と明記
```

---

## 12. Ad AI Auto 独自追加部分

### Phase 1で追加済み
```
src/
├── config.py                           # 環境変数管理
├── core/
│   ├── ad_generator.py                 # AI広告文生成（Google RSA + Meta）
│   └── optimizer.py                    # AI入札最適化エンジン
└── integrations/
    ├── google-ads/client.py            # Google Ads API連携
    ├── meta-ads/client.py              # Meta Ads API連携
    └── telegram/notifier.py            # Telegram通知
```

### ベースとの関係
```
AgentKits Marketing（ベース）        Ad AI Auto（独自追加）
─────────────────────────          ─────────────────────
知識・戦略・テンプレート      →      実行エンジン
  ↓ スキル・エージェントが            ↓
  広告戦略を策定              →      APIで自動入稿
  ↓                                  ↓
  コピーを生成                →      バリデーション→入稿
  ↓                                  ↓
  分析フレームワーク          →      データ取得→AI分析→自動最適化
  ↓                                  ↓
  レポートテンプレート        →      Telegram自動配信
```

---

## 13. 技術的な注意点

### 動作の仕組み
- **コードではない**: 実行可能なPythonコードは含まれていない（src/は独自追加）
- **Markdownベース**: 全てMarkdownファイルでAIエージェントへの「指示書」
- **Claude Code前提**: `.claude/` ディレクトリに配置することでClaude Codeが自動認識
- **モデル**: 全エージェントが `sonnet` (Claude Sonnet) を使用

### カスタマイズポイント
1. **エージェント追加**: `.claude/agents/新エージェント.md` を作成
2. **コマンド追加**: `.claude/commands/カテゴリ/名前.md` を作成
3. **スキル追加**: `.claude/skills/スキル名/SKILL.md` + `references/` を作成
4. **連携追加**: `.claude/skills/integrations/サービス名/` を作成

### 制限事項
- API直接実行はAgentKits自体には含まれない（MCP経由が前提）
- データは外部ソースに依存（自前DBなし）
- リアルタイム広告管理機能なし（戦略・コンテンツ生成が中心）
