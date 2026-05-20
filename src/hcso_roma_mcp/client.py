"""Roma Connect SDK client wrapper."""

import logging
import os
from typing import Optional

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkroma.v2 import RomaClient
from huaweicloudsdkroma.v2.model import (
    ListApisV2Request,
    ListDatasourcesRequest,
    ListLiveDataApiV2Request,
)

logger = logging.getLogger(__name__)


class RomaConnectClient:
    """Wrapper around HuaweiCloud Roma SDK with STS auth support."""

    def __init__(
        self,
        ak: Optional[str] = None,
        sk: Optional[str] = None,
        security_token: Optional[str] = None,
        project_id: Optional[str] = None,
        iam_endpoint: Optional[str] = None,
        roma_endpoint: Optional[str] = None,
    ):
        self.ak = ak or os.environ.get("HCSO_AK", "")
        self.sk = sk or os.environ.get("HCSO_SK", "")
        self.security_token = security_token or os.environ.get("HCSO_SECURITY_TOKEN", "")
        self.project_id = project_id or os.environ.get("HCSO_PROJECT_ID", "")
        self.iam_endpoint = iam_endpoint or os.environ.get(
            "HCSO_IAM_ENDPOINT", "https://iam-pub-prevnet.la-south-6001.hcso.dataprev.gov.br"
        )
        self.roma_endpoint = roma_endpoint or os.environ.get(
            "HCSO_ROMA_ENDPOINT", "https://roma-prevnet.la-south-6001.hcso.dataprev.gov.br"
        )
        self._client: Optional[RomaClient] = None

    def _build_client(self) -> RomaClient:
        if not self.ak or not self.sk or not self.project_id:
            raise ValueError("Missing credentials: HCSO_AK, HCSO_SK, HCSO_PROJECT_ID required")

        creds = BasicCredentials(self.ak, self.sk, self.project_id).with_iam_endpoint(self.iam_endpoint)
        if self.security_token:
            creds.security_token = self.security_token

        return RomaClient.new_builder().with_credentials(creds).with_endpoint(self.roma_endpoint).build()

    @property
    def client(self) -> RomaClient:
        if self._client is None:
            self._client = self._build_client()
        return self._client

    def list_datasources(self, instance_id: str) -> list:
        """List datasources for an instance."""
        resp = self.client.list_datasources(ListDatasourcesRequest(instance_id=instance_id))
        return resp.entities if hasattr(resp, "entities") else []

    def list_apis(self, instance_id: str) -> list:
        """List published APIs for an instance."""
        resp = self.client.list_apis_v2(ListApisV2Request(instance_id=instance_id))
        return resp.apis if hasattr(resp, "apis") else []

    def list_data_apis(self, instance_id: str) -> list:
        """List Data APIs (custom backends) for an instance."""
        resp = self.client.list_live_data_api_v2(ListLiveDataApiV2Request(instance_id=instance_id))
        return resp.apis if hasattr(resp, "apis") else []
