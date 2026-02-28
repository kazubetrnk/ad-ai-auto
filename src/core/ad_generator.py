"""AI Ad Copy Generator — 広告文自動生成エンジン"""
from __future__ import annotations
import json
from dataclasses import dataclass
from src.config import config


@dataclass
class GoogleAd:
    headlines: list[str]       # max 15, each ≤30 chars
    descriptions: list[str]    # max 4, each ≤90 chars
    paths: list[str]           # max 2, each ≤15 chars


@dataclass
class MetaAd:
    primary_text: str          # main body, ≤125 chars recommended
    headline: str              # ≤40 chars recommended
    description: str           # ≤30 chars recommended


class AdGenerator:
    """AI-powered ad copy generator with automatic validation."""

    GOOGLE_RSA_PROMPT = """あなたはGoogle広告のエキスパートコピーライターです。
以下の情報を元に、レスポンシブ検索広告(RSA)のコピーを生成してください。

【製品/サービス】{product}
【ターゲット】{target_audience}
【USP（強み）】{usp}
【言語】{language}

以下のJSON形式で出力してください：
{{
    "headlines": ["見出し1", ...],  // 15個、各30文字以内
    "descriptions": ["説明文1", ...],  // 4個、各90文字以内
    "paths": ["パス1", "パス2"]  // 2個、各15文字以内
}}

重要:
- 文字数制限を厳守
- CTRを最大化する訴求力のある表現
- キーワードを自然に含める
- 数字・記号を効果的に使用
- JSONのみ出力"""

    META_AD_PROMPT = """あなたはFacebook/Instagram広告のエキスパートです。
以下の情報を元に、Meta広告コピーを生成してください。

【製品/サービス】{product}
【ターゲット】{target_audience}
【USP（強み）】{usp}
【言語】{language}

以下のJSON形式で出力してください：
{{
    "primary_text": "メインテキスト（125文字以内推奨）",
    "headline": "見出し（40文字以内推奨）",
    "description": "説明文（30文字以内推奨）"
}}

重要:
- スクロール停止力のある冒頭
- 感情に訴える表現
- 明確なCTA
- JSONのみ出力"""

    def _call_ai(self, prompt: str) -> str:
        """AI APIを呼び出す"""
        if config.ai_provider == "anthropic":
            import anthropic
            client = anthropic.Anthropic(api_key=config.anthropic_api_key)
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        else:
            import openai
            client = openai.OpenAI(api_key=config.openai_api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content

    def _validate_google_ad(self, ad: GoogleAd) -> list[str]:
        """Google広告の文字数バリデーション"""
        errors = []
        for i, h in enumerate(ad.headlines):
            if len(h) > 30:
                errors.append(f"見出し{i+1}が{len(h)}文字（上限30）: {h}")
        for i, d in enumerate(ad.descriptions):
            if len(d) > 90:
                errors.append(f"説明文{i+1}が{len(d)}文字（上限90）: {d}")
        if len(ad.headlines) < 3:
            errors.append(f"見出しが{len(ad.headlines)}個（最低3個必要）")
        if len(ad.descriptions) < 2:
            errors.append(f"説明文が{len(ad.descriptions)}個（最低2個必要）")
        return errors

    def generate_google_ad(
        self,
        product: str,
        target_audience: str,
        usp: str = "",
        language: str = "ja",
    ) -> tuple[GoogleAd, list[str]]:
        """Google RSA広告文を生成＆バリデーション"""
        prompt = self.GOOGLE_RSA_PROMPT.format(
            product=product, target_audience=target_audience,
            usp=usp, language=language,
        )
        raw = self._call_ai(prompt)
        # Extract JSON
        start = raw.find("{")
        end = raw.rfind("}") + 1
        data = json.loads(raw[start:end])

        ad = GoogleAd(
            headlines=data["headlines"][:15],
            descriptions=data["descriptions"][:4],
            paths=data.get("paths", [])[:2],
        )
        errors = self._validate_google_ad(ad)
        return ad, errors

    def generate_meta_ad(
        self,
        product: str,
        target_audience: str,
        usp: str = "",
        language: str = "ja",
    ) -> MetaAd:
        """Meta広告コピーを生成"""
        prompt = self.META_AD_PROMPT.format(
            product=product, target_audience=target_audience,
            usp=usp, language=language,
        )
        raw = self._call_ai(prompt)
        start = raw.find("{")
        end = raw.rfind("}") + 1
        data = json.loads(raw[start:end])

        return MetaAd(
            primary_text=data["primary_text"],
            headline=data["headline"],
            description=data["description"],
        )
