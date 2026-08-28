# %%
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv

load_dotenv(override=True)

model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.7,
    extra_body={
        "thinking": {
            "type": "disabled",
        }
    }
)
# %%
