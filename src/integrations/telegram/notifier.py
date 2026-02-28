"""Telegram Notifier — 広告レポート・アラート・承認フロー"""
from __future__ import annotations
import json
import urllib.request
from src.config import config


class TelegramNotifier:
    """Telegram Bot API for ad notifications."""

    def __init__(self):
        self.token = config.telegram_bot_token
        self.chat_id = config.telegram_chat_id
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def _send(self, method: str, data: dict) -> dict:
        req = urllib.request.Request(
            f"{self.base_url}/{method}",
            data=json.dumps(data).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())

    def send_message(self, text: str, parse_mode: str = "HTML") -> dict:
        """テキストメッセージ送信"""
        return self._send("sendMessage", {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
        })

    def send_report(self, report_data: list[dict]) -> dict:
        """📊 日次パフォーマンスレポート送信"""
        lines = ["📊 <b>広告パフォーマンスレポート</b>\n"]
        total_spend = 0
        total_conv = 0

        for camp in report_data:
            roas = camp.get("roas", camp.get("revenue", 0) / camp["spend"] if camp["spend"] > 0 else 0)
            emoji = "🟢" if roas >= 3 else "🟡" if roas >= 1.5 else "🔴"
            lines.append(
                f"{emoji} <b>{camp['campaign_name']}</b>\n"
                f"   費用: ¥{camp['spend']:,.0f} | CV: {camp['conversions']} | "
                f"ROAS: {roas:.1f}x | CTR: {camp.get('ctr', 0):.1%}"
            )
            total_spend += camp["spend"]
            total_conv += camp["conversions"]

        lines.append(f"\n💰 合計: ¥{total_spend:,.0f} | CV合計: {total_conv}")
        return self.send_message("\n".join(lines))

    def send_alert(self, alert_type: str, message: str) -> dict:
        """⚠️ アラート送信"""
        icons = {
            "budget": "💸", "performance": "📉", "error": "🚨",
            "opportunity": "✨", "approval": "👆",
        }
        icon = icons.get(alert_type, "⚠️")
        return self.send_message(f"{icon} <b>広告アラート</b>\n\n{message}")

    def send_approval_request(
        self, action: str, details: str, callback_data: str
    ) -> dict:
        """承認リクエスト（インラインボタン付き）"""
        return self._send("sendMessage", {
            "chat_id": self.chat_id,
            "text": f"👆 <b>承認待ち</b>\n\n{action}\n\n{details}",
            "parse_mode": "HTML",
            "reply_markup": {
                "inline_keyboard": [[
                    {"text": "✅ 承認", "callback_data": f"approve:{callback_data}"},
                    {"text": "❌ 却下", "callback_data": f"reject:{callback_data}"},
                ]]
            },
        })
