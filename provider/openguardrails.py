from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from openguardrails import OpenGuardrails


class OpenGuardrailsProvider(ToolProvider):

    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            # 获取API密钥
            api_key = credentials.get("api_key")
            if not api_key:
                raise ToolProviderCredentialValidationError("API key is required")

            # 验证API密钥有效性，通过一个简单的测试调用
            client = OpenGuardrails(api_key)
            # 使用一个简单的测试来验证API密钥
            test_result = client.check_prompt("test")

            # 如果调用成功并返回了结果，则验证通过
            if hasattr(test_result, 'suggest_action'):
                return  # 验证成功
            else:
                raise ToolProviderCredentialValidationError("Invalid API key response format")

        except Exception as e:
            if "API key" in str(e).lower() or "auth" in str(e).lower():
                raise ToolProviderCredentialValidationError("Invalid API key")
            else:
                raise ToolProviderCredentialValidationError(f"Credential validation failed: {str(e)}")

    #########################################################################################
    # If OAuth is supported, uncomment the following functions.
    # Warning: please make sure that the sdk version is 0.4.2 or higher.
    #########################################################################################
    # def _oauth_get_authorization_url(self, redirect_uri: str, system_credentials: Mapping[str, Any]) -> str:
    #     """
    #     Generate the authorization URL for openguardrails OAuth.
    #     """
    #     try:
    #         """
    #         IMPLEMENT YOUR AUTHORIZATION URL GENERATION HERE
    #         """
    #     except Exception as e:
    #         raise ToolProviderOAuthError(str(e))
    #     return ""
        
    # def _oauth_get_credentials(
    #     self, redirect_uri: str, system_credentials: Mapping[str, Any], request: Request
    # ) -> Mapping[str, Any]:
    #     """
    #     Exchange code for access_token.
    #     """
    #     try:
    #         """
    #         IMPLEMENT YOUR CREDENTIALS EXCHANGE HERE
    #         """
    #     except Exception as e:
    #         raise ToolProviderOAuthError(str(e))
    #     return dict()

    # def _oauth_refresh_credentials(
    #     self, redirect_uri: str, system_credentials: Mapping[str, Any], credentials: Mapping[str, Any]
    # ) -> OAuthCredentials:
    #     """
    #     Refresh the credentials
    #     """
    #     return OAuthCredentials(credentials=credentials, expires_at=-1)
