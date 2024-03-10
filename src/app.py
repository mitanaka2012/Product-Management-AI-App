import os
import streamlit as st
from langchain.schema import (
    SystemMessage, 
    HumanMessage, 
    AIMessage
)
from langchain_openai import ChatOpenAI
from langchain_community.callbacks import StreamlitCallbackHandler
from index_builder import initialize_vectorstore  # あなたのベクターストア初期化関数
from langchain.chains import RetrievalQA

def init_page():  # ページ設定
    st.set_page_config(
        page_title="on the way release",
        page_icon="🐰"
    )
    # hedder
    st.header("プロダクト開発の道のべ")
    
    # CSSを使ってサイドバーの幅をカスタマイズ
    st.markdown(
        """
        <style>
            .css-1d391kg {width: 240px;}
        </style>
        """,
        unsafe_allow_html=True
    )
    # sidebar
    st.sidebar.markdown("## 管理人")
    # GitHubリポジトリにある画像をサイドバーに表示
    image_url = "https://github.com/mitanaka2012/Product-Management-AI-App/raw/main/image/icon.jpg"
    st.sidebar.image(image_url, use_column_width=True)
    st.sidebar.caption("わいはスライムナイトや。過去10年の戦略コンサルタントとしての経験と、PdMの経験を踏まえて、ホンマに真摯に答えるで。")

def init_messages():     # チャット履歴、コストの初期化
    clear_button = st.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        # roleに応じメッセージを初期化
        role = st.session_state.get('selected_role', 'PdM')  # デフォルトは 'PdM'
        if role == 'PdM':
            content = """
                # 背景
                あなたは戦略コンサルタントとして10年間活動をした後、ベンチャー企業のプロダクト開発マネージャーに転職した異色の経歴のPdMです。

                # 回答の基本ルール
                - 今回質問しているユーザーは、あなたと同じPdMです。
                - あなたの経験が含まれるSystemのMessageを踏まえて、最大限正確な回答をしてください。
                - 口調は丁寧に
            """
        elif role == 'Engineer':
            content = """
                # 背景
                あなたは戦略コンサルタントとして10年間活動をした後、ベンチャー企業のプロダクト開発マネージャーに転職した異色の経歴のPdMです。

                # 回答の基本ルール
                - 今回質問しているユーザーは、プロダクト開発をPdMと進めるパートナーであるEngineerです。
                - あなたの経験が含まれるSystemのMessageを踏まえて、最大限正確な回答をしてください。
                - 口調は丁寧に
            """
        elif role == 'Business':
            content = """
                ## 背景
                あなたは戦略コンサルタントとして10年間活動をした後、ベンチャー企業のプロダクト開発マネージャーに転職した異色の経歴のPdMです。

                # 回答の基本ルール
                - 今回質問しているユーザーは、開発されるプロダクトを売り込んだり評価するBusinessメンバーです。
                - あなたの経験が含まれるSystemのMessageを踏まえて、最大限正確な回答をしてください。
                - 口調は丁寧に
            """
        st.session_state.messages = [
            SystemMessage(content=content)
        ]
    st.session_state.costs = []

# QA Chainを作成
def create_qa_chain():
    vectorstore = initialize_vectorstore()  # Pineconeベクターストアの初期化
    callback = StreamlitCallbackHandler(st.container())

    llm = ChatOpenAI(
        model_name=os.getenv("OPENAI_API_MODEL", "text-davinci-003"),  # デフォルトモデル名を指定
        temperature=float(os.getenv("OPENAI_API_TEMPERATURE", 0.7)),  # 温度パラメータ
        streaming=True,
        callbacks=[callback],
    )

    qa_chain = RetrievalQA.from_llm(llm=llm, retriever=vectorstore.as_retriever())
    return qa_chain

def main():
    init_page()

    # ユーザーの入力フォーム
    container = st.container()
    with container:
        # 入力欄の上でユーザーロールを選択
        selected_role = st.radio(
            "Your role:",
            ("PdM", "Engineer", "Business"),
            key='selected_role'  # このキーを使用して選択をsession_stateに保存
        )
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_area(label='Message: ', key='input', height=100)
            submit_button = st.form_submit_button(label='Send')

    init_messages()

    # ユーザーの入力を監視し、処理
    if submit_button and user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Thinking..."):
            qa_chain = create_qa_chain()
            response = qa_chain.invoke(user_input)
            answer = response["result"]
            st.session_state.messages.append(AIMessage(content=answer))

    # チャット履歴の表示
    for message in st.session_state.messages:
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        # else:
        #     st.write("System:", message.content)  # SystemMessageの扱い

    # コストの表示
    st.sidebar.markdown("## API利用料")

    costs = st.session_state.get('costs', [0])
    for cost in costs:
        st.sidebar.markdown(f"- ¥{cost * 150:.2f}")

    # 'Buy me a beer'
    st.sidebar.markdown(
        '<div style="margin-top: 1em;"><a href="https://www.buymeacoffee.com/mitanaka2012" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Beer" height="41" width="174"></a></div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()