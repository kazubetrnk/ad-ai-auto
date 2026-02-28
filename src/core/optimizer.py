"""AI Bid Optimizer — AI駆動の入札最適化エンジン"""
from __future__ import annotations
import json
from dataclasses import dataclass, asdict
from src.config import config


@dataclass
class OptimizationAction:
    campaign_name: str
    action: str          # increase_bid, decrease_bid, pause, increase_budget, decrease_budget
    reason: str
    current_value: float
    recommended_value: float
    confidence: str      # high, medium, low
    priority: str        # urgent, normal, low


class BidOptimizer:
    """AI-powered bid & budget optimization."""

    ANALYSIS_PROMPT = """あなたは広告運用の最適化エキスパートです。
以下のキャンペーンパフォーマンスデータを分析し、最適化アクションを提案してください。

【パフォーマンスデータ】
{performance_data}

【最適化目標】
- 目標ROAS: {target_roas}x
- 最大CPA: ¥{max_cpa}
- 日予算上限: ¥{daily_budget_cap}

以下のJSON配列で出力してください：
[
    {{
        "campaign_name": "キャンペーン名",
        "action": "increase_bid|decrease_bid|pause|increase_budget|decrease_budget",
        "reason": "理由（簡潔に）",
        "current_value": 現在の値,
        "recommended_value": 推奨値,
        "confidence": "high|medium|low",
        "priority": "urgent|normal|low"
    }}
]

分析ルール:
- ROAS < 1.0 → 入札下げるか一時停止を検討
- ROAS > 3.0 & 予算消化率高い → 予算増加を検討
- CTR < 1% → 広告文の改善を示唆
- CPC が高すぎる → 入札引き下げ
- CV数ゼロ & 費用発生 → 一時停止検討
- JSONのみ出力"""

    def _call_ai(self, prompt: str) -> str:
        if config.ai_provider == "anthropic":
            import anthropic
            client = anthropic.Anthropic(api_key=config.anthropic_api_key)
            resp = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.content[0].text
        else:
            import openai
            client = openai.OpenAI(api_key=config.openai_api_key)
            resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.choices[0].message.content

    def analyze(
        self,
        performance_data: list[dict],
        target_roas: float = 3.0,
        max_cpa: float = 5000,
        daily_budget_cap: float = 50000,
    ) -> list[OptimizationAction]:
        """パフォーマンスデータを分析し最適化アクションを生成"""
        prompt = self.ANALYSIS_PROMPT.format(
            performance_data=json.dumps(performance_data, ensure_ascii=False, indent=2),
            target_roas=target_roas,
            max_cpa=max_cpa,
            daily_budget_cap=daily_budget_cap,
        )
        raw = self._call_ai(prompt)
        start = raw.find("[")
        end = raw.rfind("]") + 1
        actions_data = json.loads(raw[start:end])

        return [OptimizationAction(**a) for a in actions_data]

    def generate_report(self, actions: list[OptimizationAction]) -> str:
        """最適化レポートをHTML形式で生成（Telegram送信用）"""
        if not actions:
            return "✅ <b>最適化チェック完了</b>\n現在すべてのキャンペーンは正常範囲内です。"

        lines = ["🤖 <b>AI最適化レポート</b>\n"]
        priority_icons = {"urgent": "🔴", "normal": "🟡", "low": "🟢"}
        action_labels = {
            "increase_bid": "⬆️ 入札UP",
            "decrease_bid": "⬇️ 入札DOWN",
            "pause": "⏸ 一時停止",
            "increase_budget": "💰 予算UP",
            "decrease_budget": "💸 予算DOWN",
        }

        for a in sorted(actions, key=lambda x: {"urgent": 0, "normal": 1, "low": 2}[x.priority]):
            icon = priority_icons.get(a.priority, "⚪")
            label = action_labels.get(a.action, a.action)
            lines.append(
                f"{icon} <b>{a.campaign_name}</b>\n"
                f"   {label}: ¥{a.current_value:,.0f} → ¥{a.recommended_value:,.0f}\n"
                f"   理由: {a.reason}\n"
                f"   確信度: {a.confidence}"
            )

        urgent = sum(1 for a in actions if a.priority == "urgent")
        if urgent:
            lines.append(f"\n⚠️ <b>{urgent}件の緊急対応が必要です</b>")

        return "\n".join(lines)
