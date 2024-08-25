from app.dto.app_services_dto.open_ai_dto import OpenAIChatCompletion


class OpenAIServices:
    def chat_completion_func(self, req_dto: OpenAIChatCompletion):
