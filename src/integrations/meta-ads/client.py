"""Meta Ads API Client — Facebook/Instagram広告の自動管理"""
from __future__ import annotations
from typing import Any
from src.config import config


class MetaAdsClient:
    """Meta Marketing API wrapper."""

    def __init__(self):
        self.ad_account_id = config.meta_ad_account_id
        self._api = None

    def _get_api(self):
        from facebook_business.api import FacebookAdsApi
        if not self._api:
            self._api = FacebookAdsApi.init(
                config.meta_app_id,
                config.meta_app_secret,
                config.meta_access_token,
            )
        return self._api

    def create_campaign(
        self,
        name: str,
        objective: str = "OUTCOME_LEADS",
        daily_budget: int = 1000,
        status: str = "PAUSED",
    ) -> dict[str, Any]:
        """キャンペーン作成
        
        Args:
            name: キャンペーン名
            objective: OUTCOME_TRAFFIC, OUTCOME_LEADS, OUTCOME_SALES, etc.
            daily_budget: 日予算（セント単位）
            status: ACTIVE or PAUSED
        """
        from facebook_business.adobjects.adaccount import AdAccount
        from facebook_business.adobjects.campaign import Campaign

        self._get_api()
        account = AdAccount(f"act_{self.ad_account_id}")

        campaign = account.create_campaign(params={
            Campaign.Field.name: name,
            Campaign.Field.objective: objective,
            Campaign.Field.status: status,
            Campaign.Field.special_ad_categories: [],
            "daily_budget": daily_budget,
        })
        return {"id": campaign["id"], "name": name}

    def create_ad_creative(
        self,
        name: str,
        page_id: str,
        message: str,
        headline: str,
        description: str,
        link_url: str,
        image_hash: str | None = None,
    ) -> dict[str, Any]:
        """広告クリエイティブ作成"""
        from facebook_business.adobjects.adaccount import AdAccount
        from facebook_business.adobjects.adcreative import AdCreative

        self._get_api()
        account = AdAccount(f"act_{self.ad_account_id}")

        creative_data = {
            AdCreative.Field.name: name,
            AdCreative.Field.object_story_spec: {
                "page_id": page_id,
                "link_data": {
                    "message": message,
                    "link": link_url,
                    "name": headline,
                    "description": description,
                },
            },
        }
        if image_hash:
            creative_data[AdCreative.Field.object_story_spec]["link_data"]["image_hash"] = image_hash

        creative = account.create_ad_creative(params=creative_data)
        return {"id": creative["id"], "name": name}

    def get_insights(
        self,
        campaign_id: str | None = None,
        days: int = 7,
    ) -> list[dict]:
        """パフォーマンスデータ取得"""
        from facebook_business.adobjects.adaccount import AdAccount

        self._get_api()
        account = AdAccount(f"act_{self.ad_account_id}")

        params = {
            "time_range": {"since": f"{{days_ago:{days}}}", "until": "today"},
            "fields": [
                "campaign_name", "impressions", "clicks", "spend",
                "actions", "cost_per_action_type", "ctr", "cpc",
            ],
            "level": "campaign",
        }
        if campaign_id:
            params["filtering"] = [{"field": "campaign.id", "operator": "EQUAL", "value": campaign_id}]

        insights = account.get_insights(params=params)
        results = []
        for row in insights:
            conversions = 0
            if "actions" in row:
                for action in row["actions"]:
                    if action["action_type"] in ("lead", "purchase", "complete_registration"):
                        conversions += int(action["value"])

            results.append({
                "campaign_name": row.get("campaign_name", ""),
                "impressions": int(row.get("impressions", 0)),
                "clicks": int(row.get("clicks", 0)),
                "spend": float(row.get("spend", 0)),
                "conversions": conversions,
                "ctr": float(row.get("ctr", 0)),
                "cpc": float(row.get("cpc", 0)),
            })
        return results

    def update_budget(self, campaign_id: str, daily_budget: int) -> dict:
        """予算更新（セント単位）"""
        from facebook_business.adobjects.campaign import Campaign
        self._get_api()
        campaign = Campaign(campaign_id)
        campaign.api_update(params={"daily_budget": daily_budget})
        return {"updated": campaign_id, "new_budget": daily_budget}
