import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage, 
    HumanMessage, 
    AIMessage
)
from langchain.callbacks import get_openai_callback

# API キーを変数として設定
api_key = "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"


def init_page():  # ページ設定
    st.set_page_config(
        page_title="on the way to product release",
        page_icon="🤗"
    )
    # hedder
    st.header("プロダクト開発の道の辺.🤗")
    
    # sidebar
    st.sidebar.title("options")

def init_messages():     # チャット履歴、コストの初期化
    clear_button = st.sidebar.button("やり取りをクリアする", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="#背景 あなたは戦略コンサルタントとして10年間活動をした後、ベンチャー企業のプロダクト開発マネージャーに転職した異色の経歴のPdMです。常に、「ユニークな」回答を心がけてください。#回答の基本ルール -ユーザーからの問いかけには、まず置かれている状況を詳しく説明するように問い直してください。 - ユーザーが具体的な状況を提示したら、回答してください。 - 弱い関西弁口調です #ユニークな回答のルール - 回答に対して、より「具体的な内容」を聞きたいかユーザーに問いかけてください。もしユーザーが、「具体的な内容」を求めてきたら、具体のケースで答えるようにしてください。")
    ]
    st.session_state.costs = []

def select_model(): # 使っていないが、モデルの選択
    model = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
    if model == "GPT-3.5":
        model_name = "gpt-3.5-turbo-0613"
    else:
        model_name = "gpt-4"
    return ChatOpenAI(temperature=0.7, model_name=model_name)

def get_answer(llm, messages):
    with get_openai_callback() as cb:
        answer = llm(messages)
    return answer.content, cb.total_cost

def main():
    init_page()
    init_messages()

    # ChatOpenAI インスタンスを作成し、API キーを渡す
    llm = ChatOpenAI(
        openai_api_key=api_key,
        temperature=0.7
    )

    # ユーザーの入力を監視
    if user_input := st.chat_input("気になっていることを入力してください。Enterで送信、shift+Enterで改行。"):
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("スライムナイトが考え中 ..."):
            answer , cost = get_answer(llm, st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=answer))
        st.session_state.costs.append(cost)

    # チャット履歴の表示
    messages = st.session_state.get("messages", [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        else:
            st.write(f"プロダクト開発はときには休憩が必要です。気になることをスライムナイトに聞いてみましょう。") #System message: {message.content}

    # コストの表示
    st.sidebar.markdown("## 相談料")
    st.sidebar.markdown("**Total**")

    costs = st.session_state.get('costs', [])
    for const in costs:
        st.sidebar.markdown(f"- ¥{cost* 150:.5f}")
    

if __name__ == "__main__":
    main()