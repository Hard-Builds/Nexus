from app.dto.open_ai_dto import OpenAIChatReqDto


class OpenAIService:
    def chat_completion_func(self, req_dto: OpenAIChatReqDto):
        """Get Profile details"""
        """Weighted Round robin for load balancing of the keys"""
        """Invoking openai sdk with exp backoff"""
        """Appening log file"""