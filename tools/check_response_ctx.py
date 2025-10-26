from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from openguardrails import OpenGuardrails

class CheckResponseCtxTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            # Get required parameters
            prompt = tool_parameters.get("prompt", "")
            response = tool_parameters.get("response", "")
            user_id = tool_parameters.get("user_id") if tool_parameters.get("user_id") is not None else None

            # Validate required parameters
            if not prompt:
                yield self.create_text_message("Error: Prompt parameter is required.")
                return

            if not response:
                yield self.create_text_message("Error: Response parameter is required.")
                return

            # Get API key
            api_key = self.runtime.credentials.get("api_key")
            if not api_key:
                yield self.create_text_message("Error: API key is required.")
                return

            # Create OpenGuardrails client and check response content (based on context)
            client = OpenGuardrails(api_key)
            result = client.check_response_ctx(prompt=prompt, response=response, user_id=user_id)

            # Extract categories field: from compliance and security not equal to "no_risk" categories list first item
            categories = []
            if result.result.compliance.risk_level != "no_risk" and result.result.compliance.categories:
                categories.append(result.result.compliance.categories[0])
            elif result.result.security.risk_level != "no_risk" and result.result.security.categories:
                categories.append(result.result.security.categories[0])
            elif result.result.data.risk_level != "no_risk" and result.result.data.categories:
                categories.append(result.result.data.categories[0])

            categories_str = ", ".join(categories)
            if categories_str:
                categories_str = f"{categories_str}"
            else:
                categories_str = ""

            # Process suggest_answer field, if not exist, set to empty string
            suggest_answer = ""
            if result.suggest_answer:
                suggest_answer = result.suggest_answer

            # Use custom variable to return result
            yield self.create_variable_message("id", result.id)
            yield self.create_variable_message("overall_risk_level", result.overall_risk_level)
            yield self.create_variable_message("suggest_action", result.suggest_action)
            yield self.create_variable_message("suggest_answer", suggest_answer)
            yield self.create_variable_message("categories", categories_str)
            yield self.create_variable_message("score", result.score)

        except Exception as e:
            # Error handling
            yield self.create_text_message(f"Error: {str(e)}")
            yield self.create_json_message({"error": str(e)})
