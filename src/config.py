"""Ad AI Auto — Configuration"""
import os
from dataclasses import dataclass


@dataclass
class Config:
    # Google Ads
    google_ads_developer_token: str = os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN", "")
    google_ads_client_id: str = os.getenv("GOOGLE_ADS_CLIENT_ID", "")
    google_ads_client_secret: str = os.getenv("GOOGLE_ADS_CLIENT_SECRET", "")
    google_ads_refresh_token: str = os.getenv("GOOGLE_ADS_REFRESH_TOKEN", "")
    google_ads_customer_id: str = os.getenv("GOOGLE_ADS_CUSTOMER_ID", "")

    # Meta Ads
    meta_access_token: str = os.getenv("META_ACCESS_TOKEN", "")
    meta_app_id: str = os.getenv("META_APP_ID", "")
    meta_app_secret: str = os.getenv("META_APP_SECRET", "")
    meta_ad_account_id: str = os.getenv("META_AD_ACCOUNT_ID", "")

    # AI
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    ai_provider: str = os.getenv("AI_PROVIDER", "anthropic")

    # Telegram
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")

    # General
    timezone: str = os.getenv("TIMEZONE", "Asia/Manila")
    language: str = os.getenv("LANGUAGE", "ja")


config = Config()
