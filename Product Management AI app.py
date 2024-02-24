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
        page_title="プロダクト占いの館",
        page_icon="🤗"
    )
    # hedder
    st.header("プロダクト占いの館.🤗")
    
    # sidebar
    st.sidebar.title("options")

def init_messages():     # チャット履歴、コストの初期化
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="あなたは経験を積んだProduct Managerです。ユーザーからのネガティブな問いかけには元気づけるように返答してください")
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
    if user_input := st.chat_input("あなたのお困りを入力してください。Enterで送信、shift+Enterで改行。"):
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("ChatGPT is typing ..."):
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
            st.write(f"プロダクト開発で困っていることがありますか？ありますよね？") #System message: {message.content}

    # コストの表示
    st.sidebar.markdown("## 占い料")
    st.sidebar.markdown("**Total**")

    costs = st.session_state.get('costs', [])
    for const in costs:
        st.sidebar.markdown(f"- ${cost:.5f}")
    

if __name__ == "__main__":
    main()