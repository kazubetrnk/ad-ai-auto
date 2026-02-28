"""Ad AI Auto — デモ: AI広告文生成 + Telegram通知"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from src.core.ad_generator import AdGenerator
from src.integrations.telegram.notifier import TelegramNotifier


def main():
    generator = AdGenerator()
    notifier = TelegramNotifier()

    print("🤖 広告文を生成中...")

    # Google RSA広告生成
    google_ad, errors = generator.generate_google_ad(
        product="AI広告自動運用ツール - Ad AI Auto",
        target_audience="中小企業のマーケター、広告運用担当者",
        usp="AIが広告文生成・入札最適化・レポートを全自動。運用コスト80%削減。",
        language="ja",
    )

    print(f"\n📝 Google RSA広告:")
    print(f"  見出し ({len(google_ad.headlines)}個):")
    for i, h in enumerate(google_ad.headlines, 1):
        mark = "✅" if len(h) <= 30 else "❌"
        print(f"    {mark} {i}. {h} ({len(h)}文字)")
    print(f"  説明文 ({len(google_ad.descriptions)}個):")
    for i, d in enumerate(google_ad.descriptions, 1):
        mark = "✅" if len(d) <= 90 else "❌"
        print(f"    {mark} {i}. {d} ({len(d)}文字)")
    if errors:
        print(f"  ⚠️ バリデーションエラー: {errors}")

    # Meta広告生成
    meta_ad = generator.generate_meta_ad(
        product="AI広告自動運用ツール - Ad AI Auto",
        target_audience="中小企業のマーケター、広告運用担当者",
        usp="AIが広告文生成・入札最適化・レポートを全自動。運用コスト80%削減。",
        language="ja",
    )

    print(f"\n📝 Meta広告:")
    print(f"  本文: {meta_ad.primary_text} ({len(meta_ad.primary_text)}文字)")
    print(f"  見出し: {meta_ad.headline} ({len(meta_ad.headline)}文字)")
    print(f"  説明: {meta_ad.description} ({len(meta_ad.description)}文字)")

    # Telegram通知
    print("\n📱 Telegramに結果を送信中...")
    msg = (
        "🤖 <b>Ad AI Auto — 広告文生成デモ</b>\n\n"
        "📌 <b>Google RSA広告</b>\n"
    )
    for h in google_ad.headlines[:5]:
        msg += f"  • {h}\n"
    msg += f"  ...他{len(google_ad.headlines)-5}個\n\n"
    msg += (
        "📌 <b>Meta広告</b>\n"
        f"  本文: {meta_ad.primary_text}\n"
        f"  見出し: {meta_ad.headline}\n\n"
        "✅ Phase 2 動作確認完了！"
    )
    notifier.send_message(msg)
    print("✅ 送信完了！")


if __name__ == "__main__":
    main()
