from langchain.chat_models import init_chat_model
from langchain_core.rate_limiters import InMemoryRateLimiter

from app.adapters.model.protocol import ModelAdapter


class LiveChatModelAdapter(ModelAdapter):
    """
    Generic provider-backed model adapter mapping LangChain's generic BaseChatModel
    to our internal ModelAdapter protocol.
    """

    def __init__(
        self,
        model_name: str,
        api_key: str | None = None,
        api_base: str | None = None,
        requests_per_minute: float | None = 60.0,
    ):
        """
        Initializes the model dynamically. `init_chat_model` relies on the fact
        that specific provider packages (e.g., langchain-openai) are installed.
        """
        kwargs = {}
        if api_key:
            kwargs["api_key"] = api_key
        if api_base:
            kwargs["base_url"] = api_base
        if requests_per_minute and requests_per_minute > 0:
            # TODO: DEFERRED. Replace InMemoryRateLimiter with a distributed rate limiter
            # (e.g., Redis) before exposing to production workloads.
            kwargs["rate_limiter"] = InMemoryRateLimiter(
                requests_per_second=requests_per_minute / 60.0,
                check_every_n_seconds=0.1,
                max_bucket_size=max(1, int(requests_per_minute / 2)),
            )

        self.client = init_chat_model(model=model_name, **kwargs)

    def generate(self, prompt: str) -> str:
        """
        Generates content from the configured model based on a prompt.
        """
        response = self.client.invoke(prompt)
        return str(response.content)
