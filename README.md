# サービス名「プロダクト開発の道の辺」
- [https://prduct-management-ai-app.streamlit.app/](https://on-the-way-release.streamlit.app/)

## 開発経緯
- 3連休が暇だったので
- 非常に体系的にまとまった記事があったので

### 参考にした記事
- つくりながら学ぶ！AIアプリ開発入門 - LangChain & Streamlit による ChatGPT API 徹底活用
(https://zenn.dev/ml_bear/books/d1f060a3f166a5/viewer/678844)
- LangChain で社内チャットボット作ってみた
(https://zenn.dev/cloud_ace/articles/19bd3554ac8432)

## 開発内容（ファーストリリース）
- ほぼ記事を写経し、以下の機能を実装しています
  - 質問したいことをChat GPTに問いかける
  - その回答が帰ってきて、履歴として表示される
  - 履歴をクリアして、新しい問いかけができる
  - 各セッションでの、消費したクレジットが「相談料」として表示される
- オリジナルで以下を実装しました
  - ユーザーが選んだRoleによって、返答内容が変わる

## 開発内容（セカンドリリース、3/10追加）
- documents内の文章をpineconeにベクターデータとして保存する内部アプリを追加
- 追加されたベクターデータを参照して、回答するようにapp.py変更

### repository構成

repository name/

├── .streamlit/

| └── (streamlitの設定ファイル)

├── documents/

│ └── (ここには、インデックス化したい文書を置く)

├── src/

│ ├── index_builder.py (文書のインデックス化とストレージ保存を行うスクリプト)

│ └── app.py (ユーザーに対してQ&Aサービスを提供するアプリケーションのメインスクリプト)

├── requirements.txt (プロジェクトの依存関係を記述するファイル)