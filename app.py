import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage, 
    HumanMessage, 
    AIMessage
)
from langchain.callbacks import get_openai_callback


def init_page():  # ページ設定
    st.set_page_config(
        page_title="on the way to product release",
        page_icon="🤗"
    )
    # hedder
    st.header("プロダクト開発の道の辺.🤗")
    
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
    st.sidebar.caption("わいは「スライムナイト」や。過去10年の戦略コンサルタントとしての経験と、PdMの経験を踏まえて、ホンマに真摯に答えるで。")

def init_messages():     # チャット履歴、コストの初期化
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        # roleに応じメッセージを初期化
        role = st.session_state.get('selected_role', 'PdM')  # デフォルトは 'PdM'
        if role == 'PdM':
            content = "#背景 あなたは戦略コンサルタントとして10年間活動をした後、ベンチャー企業のプロダクト開発マネージャーに転職した異色の経歴のPdMです。#回答の基本ルール -ユーザーからの問いかけには、まず置かれている状況を詳しく説明するように問い直してください。 - ユーザーであるPdMが具体的な状況を提示したら、回答してください。 - 弱い関西弁口調です #回答のスタンス - あなたの回答に、より「具体的な内容」を聞きたいかユーザーに問いかけてください。もしユーザーが、「具体的な内容」を求めてきたら、具体のケースで答えてください。"
        elif role == 'Engineer':
            content = "#背景 あなたはベンチャー企業のプロダクト開発マネージャーに転職して苦労をしたが、Engineerと上手くチームを作ってSaaSを開発しているPdMです。#回答の基本ルール -ユーザーからの問いかけには、まず置かれている状況を詳しく説明するように問い直してください。 - ユーザーであるEngineerが具体的な状況を提示したら、回答してください。 - 弱い関西弁口調です #回答のスタンス - あなたの回答に、より「具体的な内容」を聞きたいかユーザーに問いかけてください。もしユーザーが、「具体的な内容」を求めてきたら、具体のケースを使って、あくまでPdMの目線から「PdMがどう考えているから」を起点にEngineerの疑問や質問に答えてください。"
        elif role == 'Business':
            content = "##背景 あなたは戦略コンサルタントとして10年間活動をした後、ベンチャー企業の経営者のトップと二人三脚でSaaSプロダクトを作っているPdMです。 #回答の基本ルール -ユーザーであるBizメンバーからの問いかけには、まず置かれている状況を詳しく説明するように問い直してください。 - ユーザーが具体的な状況を提示したら、回答してください。 - 丁寧な口調です #回答のスタンス - あなたの回答に、より「具体的な内容」を聞きたいかユーザーに問いかけてください。もしユーザーが、「具体的な内容」を求めてきたら、具体のケースを使って、経営に関する知識を駆使して、Biz側の開発に関する素朴な疑問に答えてください"

        st.session_state.messages = [
            SystemMessage(content=content)
        ]
    st.session_state.costs = []

def get_answer(llm, messages):
    with get_openai_callback() as cb:
        answer = llm(messages)
    return answer.content, cb.total_cost

def main():
    init_page()
    
    # ChatOpenAI インスタンスを作成
    llm = ChatOpenAI(
        temperature=0.7
    )

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
            # 入力例をキャプションで加える
            st.caption("例：「xxxx。」")
            submit_button = st.form_submit_button(label='Send')

    init_messages()

    # ユーザーの入力を監視
    if submit_button and user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("スライムナイトが考え中 ..."):
            answer, cost = get_answer(llm, st.session_state.messages)
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
    st.sidebar.markdown("## ただいまの相談料")

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