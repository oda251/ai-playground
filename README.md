# 概要

- 初心者が`Google ADK`を使って AI エージェント構築をする記事です
  - `ADK`：google が開発した AI エージェントフレームワーク
    - 参考：[Qiita | 🤖 Google Agent Development Kit (ADK) 入門ガイド](https://qiita.com/okikusan-public/items/9f351edda089f431ed26)
- 本記事では、ブラウザ上でエージェントと対話し、以下ができるところまでやります - 入力->エージェント A->スクリプト i->エージェント B->出力
  ![Drawing 2025-04-20 01.22.59.excalidraw.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3298811/706e1a29-c39c-4e2b-8995-75aa14040de8.png)

# 環境構築

#### 1. Ollama を手にいれよう！

- Ollama は、ローカル LLM を簡単に動かせるアプリ！

1. [Ollama | Download](https://ollama.com/download)からインストール
2. モデルをダウンロードしてみよう

```bash
ollama pull gemma3
ollama pull mistral-small3.1
```

- 本記事で使うのは、基本的に上記２モデルです
- 興味がある人は、[Ollama | Models](https://ollama.com/search)から好きなモデルを選んで動かしてみてください

#### 2. AI を走らせてみよう

```bash
ollama run gemma3
```

- ターミナル上で会話が始まるぞ！

![スクリーンショット 2025-04-19 202510.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3298811/6f679391-78d4-4487-9a47-fc86e6a83dcc.png)

#### 3. python 環境をセットアップしよう

1. [Installing uv](https://docs.astral.sh/uv/getting-started/installation/)を参考に `uv`をインストール
   - `uv`は、Python バージョン管理ツール
2. python をインストール
   - `uv install python`

参考:
[Python Coding Best Practice](https://cyberagentailab.github.io/BestPracticesForPythonCoding/)

#### 4. ライブラリをインストールしよう

```bash
uv pip install google-adk litellm
```

- `google-adk`:
  - google が開発した AI エージェントフレームワーク！
- `litellm`:
  - LLM の API インターフェース！

# エージェントを構築しよう

- ここからコードを書くよ！

## 1. 簡単な対話エージェントを構築してみよう

### ディレクトリ構成

```
.
├── chat_agent
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-313.pyc
│   │   └── agent.cpython-313.pyc
│   └── agent.py
├── .env
├── pyproject.toml
└── uv.lock
```

### コード

```python:__init__.py
# おまじない
from . import agent
```

```.env
# 環境変数をフレームワークが読みに行って、やり取りしてくれる
OPENAI_API_BASE=http://localhost:11434/v1
OPENAI_API_KEY=anything
```

```python:agent.py
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

root_agent = LlmAgent(
    model=LiteLlm(model="ollama_chat/gemma3"),
    name="chat_agent",
    description=(
        "chat agent that can chat with users and answer questions."
    ),
    instruction="""
        You are a chat agent that can answer questions and have conversations
        with users. You can also perform calculations and provide information
        about various topics.
    """,
)
```

- コードが書けたら、`uv run adk web`でサーバが立ちあがる！
- `localhost:8000`（デフォルト）にブラウザからアクセスすると、エージェントがいるはず！とりあえず動きました！🎉
  ![スクリーンショット 2025-04-19 203024.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3298811/db642dee-ef23-4c48-9dd2-618833d4973a.png)

## 2. AI に python スクリプトを実行してもらおう

- `tools`として、AI に python スクリプトを渡します
- `tool`の説明は丁寧に書こう！I/O の形式まで書けると Good
- 参考：[Agent Development Kit | Function tools](https://google.github.io/adk-docs/tools/function-tools/)

### ディレクトリ構成

```
.
├── die_agent
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-313.pyc
│   │   └── agent.cpython-313.pyc
│   ├── .env
│   ├── agent.py
│   └── tools             # 新しいやつ！
│       └── roll_die.py
├── pyproject.toml
└── uv.lock
```

### コード

```python:agent.py
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from pydantic import BaseModel, Field
from die_agent.tools.roll_die import roll_die

root_agent = LlmAgent(
    model=LiteLlm(model="ollama_chat/mistral-small3.1"),
    name="dir_agent",
    description=("Agent that can roll a die."),
    instruction=("You can ask user to roll a die."),
    tools=[
        roll_die,
    ],
)
```

```python:tools/roll_die.py
import random

def roll_die():
    """
    Roll an 6-sided die and return the result.
    Args:
        None
    Returns:
        dict: {"result": int, "status": str}
    """
    return {
        "result": random.randint(1, 6),
        "status": "success",
    }
```

- コードが書けたら、`uv run adk web`をして、`localhost:8000`にアクセス！動きましたか？
  ![スクリーンショット 2025-04-19 234336.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3298811/e31b2683-92df-4510-a563-f5f192ad8e4e.png)

## 3. マルチエージェントにしてみよう

- いよいよマルチエージェント！エージェント A のダイスの結果を使って、エージェント B におみくじをひいてもらいます
- 増える概念：
  - `output_key`：各エージェントの出力は、context にキーバリューで保存されます。その key を指定する
  - `Sequential agents`：サブエージェントに登録したエージェントを、順番に呼び出してくれる
- 注釈：
  - うちの PC が悲鳴をあげたので、この項ではモデルを gemini にしました
  - gemini を使う場合、`.env`には以下が必要。`AI Studio`で無料発行できます
    - `GOOGLE_API_KEY="XXX"`
- 参考：[Agent Development Kit | Sequential agents](https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/)

### ディレクトリ構成

```
.
├── README.md
├── omikuji_agent
│   ├── __init__.py
│   ├── agent.py
│   ├── agents
│   │   ├── die_agent.py
│   │   └── omikuji_agent.py
│   └── tools
│       ├── omikuji.py
│       └── roll_die.py
├── .env
├── pyproject.toml
└── uv.lock
```

### コード

```python:omikuji_agent/agent.py
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents import LlmAgent
from omikuji_agent.agents.die_agent import die_agent
from omikuji_agent.agents.omikuji_agent import omikuji_agent

root_agent = SequentialAgent(
    name="CodePipelineAgent",
    sub_agents=[die_agent, omikuji_agent],
)
```

```python:omikuji_agent/agents/die_agent.py
from google.adk.agents import LlmAgent
from omikuji_agent.tools.roll_die import roll_die

die_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="die_agent",
    description=("Agent that can roll a die."),
    instruction=("You can ask user to roll a die."),
    tools=[
        roll_die,
    ],
    output_key="die_result",
)
```

```python:omikuji_agent/agents/omikuji_agent.py
from google.adk.agents import LlmAgent
from omikuji_agent.tools.omikuji import omikuji

omikuji_agent = LlmAgent(
    # model=LiteLlm(model="ollama_chat/mistral-small3.1"),
    model="gemini-2.0-flash",
    name="omikuji_agent",
    description=("Agent that can give a omikuji result. "),
    instruction=(
        """
		You can draw an omikuji.
		Take the number proveded in the session state key 'die_result' as a parameter.
		"""
    ),
    tools=[
        omikuji,
    ],
)
```

```python:omikuji_agent/tools/roll_die.py
import random

def roll_die():
    """
    Roll an 6-sided die and return the result.
    Args:
        None
    Returns:
        dict: {"result": int, "status": str}
    """
    return {
        "result": random.randint(1, 6),
        "status": "success",
    }
```

```python:omikuji_agent/tools/omikuji.py
def omikuji(id: int):
    """
    Returns a omikuji result based on the given id. id is 1-based. If id is out of range, return error.
    Args:
        id (int): The id of the fortune result.
    Returns:
        dict: {"result": str, "status": str, "input": dict}
    """
    fortunes = [
        "大吉",
        "中吉",
        "小吉",
        "吉",
        "凶",
        "大凶",
    ]

    if id < 0 or id > len(fortunes):
        return {"result": "Invalid fortune id.", "status": "error", "input": {"id": id}}
    id -= 1
    return {
        "result": fortunes[id],
        "input": {"id": id},
        "status": "success",
    }
```

- コードが書けたら、`uv run adk web`をして、`localhost:8000`にアクセス！動いたら OK！
  ![スクリーンショット 2025-04-20 003927.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3298811/dc5a6425-e4af-4a19-9932-ec46461cb6a2.png)

# まとめ

- 短いコードでエーアイが動いて嬉しい！
- 次は MCP サーバとかで色々動かす記事を書こうと思う
- 不足や誤りを発見しましたら、ご指摘いただけると助かります。
