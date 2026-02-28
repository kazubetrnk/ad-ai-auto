"""Google Ads API Client — 広告の自動入稿・管理・レポート取得"""
from __future__ import annotations
from typing import Any
from src.config import config


class GoogleAdsClient:
    """Google Ads API wrapper for automated ad management."""

    def __init__(self):
        self.customer_id = config.google_ads_customer_id
        self._client = None

    def _get_client(self):
        """Initialize Google Ads API client."""
        from google.ads.googleads.client import GoogleAdsClient as GAClient
        if not self._client:
            self._client = GAClient.load_from_dict({
                "developer_token": config.google_ads_developer_token,
                "client_id": config.google_ads_client_id,
                "client_secret": config.google_ads_client_secret,
                "refresh_token": config.google_ads_refresh_token,
                "use_proto_plus": True,
            })
        return self._client

    def create_campaign(
        self,
        name: str,
        budget_micros: int,
        campaign_type: str = "SEARCH",
        bidding_strategy: str = "MAXIMIZE_CONVERSIONS",
    ) -> dict[str, Any]:
        """キャンペーン作成
        
        Args:
            name: キャンペーン名
            budget_micros: 日予算（マイクロ単位、例: 1000000 = ¥1）
            campaign_type: SEARCH, DISPLAY, SHOPPING, PERFORMANCE_MAX
            bidding_strategy: 入札戦略
        """
        client = self._get_client()
        campaign_service = client.get_service("CampaignService")
        budget_service = client.get_service("CampaignBudgetService")

        # Create budget
        budget_op = client.get_type("CampaignBudgetOperation")
        budget = budget_op.create
        budget.name = f"{name}_budget"
        budget.amount_micros = budget_micros
        budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
        budget_response = budget_service.mutate_campaign_budgets(
            customer_id=self.customer_id, operations=[budget_op]
        )

        # Create campaign
        campaign_op = client.get_type("CampaignOperation")
        campaign = campaign_op.create
        campaign.name = name
        campaign.campaign_budget = budget_response.results[0].resource_name
        campaign.advertising_channel_type = getattr(
            client.enums.AdvertisingChannelTypeEnum, campaign_type
        )
        campaign.status = client.enums.CampaignStatusEnum.PAUSED

        response = campaign_service.mutate_campaigns(
            customer_id=self.customer_id, operations=[campaign_op]
        )
        return {"resource_name": response.results[0].resource_name, "name": name}

    def create_responsive_search_ad(
        self,
        ad_group_resource: str,
        headlines: list[str],
        descriptions: list[str],
        final_url: str,
    ) -> dict[str, Any]:
        """レスポンシブ検索広告(RSA)作成
        
        Args:
            headlines: 見出しリスト（最大15個、各30文字以内）
            descriptions: 説明文リスト（最大4個、各90文字以内）
            final_url: 遷移先URL
        """
        client = self._get_client()
        ad_group_ad_service = client.get_service("AdGroupAdService")

        op = client.get_type("AdGroupAdOperation")
        ad_group_ad = op.create
        ad_group_ad.ad_group = ad_group_resource
        ad_group_ad.status = client.enums.AdGroupAdStatusEnum.PAUSED

        ad = ad_group_ad.ad
        ad.final_urls.append(final_url)

        for headline in headlines[:15]:
            h = client.get_type("AdTextAsset")
            h.text = headline[:30]
            ad.responsive_search_ad.headlines.append(h)

        for desc in descriptions[:4]:
            d = client.get_type("AdTextAsset")
            d.text = desc[:90]
            ad.responsive_search_ad.descriptions.append(d)

        response = ad_group_ad_service.mutate_ad_group_ads(
            customer_id=self.customer_id, operations=[op]
        )
        return {"resource_name": response.results[0].resource_name}

    def get_performance_report(
        self, campaign_id: str | None = None, days: int = 7
    ) -> list[dict]:
        """パフォーマンスレポート取得"""
        client = self._get_client()
        ga_service = client.get_service("GoogleAdsService")

        query = f"""
            SELECT
                campaign.id, campaign.name, campaign.status,
                metrics.impressions, metrics.clicks, metrics.cost_micros,
                metrics.conversions, metrics.conversions_value,
                metrics.ctr, metrics.average_cpc
            FROM campaign
            WHERE segments.date DURING LAST_{days}_DAYS
        """
        if campaign_id:
            query += f" AND campaign.id = {campaign_id}"

        response = ga_service.search(customer_id=self.customer_id, query=query)
        results = []
        for row in response:
            results.append({
                "campaign_id": row.campaign.id,
                "campaign_name": row.campaign.name,
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "cost": row.metrics.cost_micros / 1_000_000,
                "conversions": row.metrics.conversions,
                "revenue": row.metrics.conversions_value,
                "ctr": row.metrics.ctr,
                "avg_cpc": row.metrics.average_cpc / 1_000_000,
                "roas": (row.metrics.conversions_value / (row.metrics.cost_micros / 1_000_000))
                    if row.metrics.cost_micros > 0 else 0,
            })
        return results

    def update_bid(self, campaign_resource: str, bid_micros: int) -> dict:
        """入札単価更新"""
        client = self._get_client()
        campaign_service = client.get_service("CampaignService")
        op = client.get_type("CampaignOperation")
        campaign = op.update
        campaign.resource_name = campaign_resource
        campaign.manual_cpc.enhanced_cpc_enabled = True
        
        field_mask = client.get_type("FieldMask")
        field_mask.paths.append("manual_cpc.enhanced_cpc_enabled")
        op.update_mask.CopyFrom(field_mask)

        response = campaign_service.mutate_campaigns(
            customer_id=self.customer_id, operations=[op]
        )
        return {"updated": response.results[0].resource_name}

    def pause_campaign(self, campaign_resource: str) -> dict:
        """キャンペーン一時停止"""
        client = self._get_client()
        campaign_service = client.get_service("CampaignService")
        op = client.get_type("CampaignOperation")
        campaign = op.update
        campaign.resource_name = campaign_resource
        campaign.status = client.enums.CampaignStatusEnum.PAUSED

        field_mask = client.get_type("FieldMask")
        field_mask.paths.append("status")
        op.update_mask.CopyFrom(field_mask)

        response = campaign_service.mutate_campaigns(
            customer_id=self.customer_id, operations=[op]
        )
        return {"paused": response.results[0].resource_name}
