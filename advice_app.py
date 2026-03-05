import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
api_key = os.environ.get("OPENAI_API_KEY")

# 簡単な Streamlit アプリ: ユーザーから相談内容を受け取り、OpenAI のチャット補完で
# 健康に関するアドバイスを取得して表示します。

if not api_key:
    st.title("ザ・アドバイザーアプリ")
    st.error("環境変数 OPENAI_API_KEY が設定されていません。アプリを実行する前に設定してください。")
    st.stop()

# OpenAI クライアントを初期化します。
client = OpenAI(api_key=api_key)

# アプリタイトルと簡単な説明を表示
st.title("ザ・アドバイザーアプリ")
st.write("あなたの相談の種類を選んで、具体的な状況を入力してください。")

# ラジオボタンで相談タイプを選択できるようにする
advisor_type = st.radio("相談タイプを選択", ("健康アドバイザー", "睡眠改善アドバイザー", "食事改善アドバイザー"))

# 相談タイプに応じて system メッセージ（アシスタントの振る舞い）を切り替える
if advisor_type == "健康アドバイザー":
    system_message = "あなたは健康に関するアドバイザーです。安全なアドバイスを提供してください。医学的な診断はできないことを明確にし、専門家受診を促してください。"
    default_prompt = "最近眠れないのですが、どうしたらいいですか？"
elif advisor_type == "睡眠改善アドバイザー":
    # 睡眠改善アドバイザー用のより具体的な振る舞い指示
    system_message = (
        "あなたは睡眠改善に特化したアドバイザーです。睡眠衛生、生活習慣、リラックス法、睡眠環境の改善などの実践的な助言を、"
        "安全かつやさしい口調で提供してください。深刻な睡眠障害が疑われる場合は医療機関受診を勧めてください。"
    )
    default_prompt = "寝付きが悪く、夜中に何度も目が覚めます。どうすれば改善できますか？"
else:
    # 食事改善アドバイザー用の振る舞い指示
    system_message = (
        "あなたは食事改善に特化したアドバイザーです。バランスの良い食事、タイミング、食品の選び方、簡単に実践できるレシピや習慣改善の提案を、"
        "実用的かつ安全に提供してください。特定疾患やアレルギーが疑われる場合は医療機関や栄養士の受診を勧めてください。"
    )
    default_prompt = "朝食を抜きがちで、栄養バランスが気になります。改善方法を教えてください。"

# デフォルトの相談テキスト（相談タイプごとに変える）
user_input = st.text_area("相談内容", value=default_prompt)

# ボタンが押されたら OpenAI に問い合わせて応答を表示する
if st.button("相談する"):
    # API 呼び出しは例外が発生する可能性があるため try/except で保護する
    try:
        # system メッセージでアシスタントに振る舞いを指示する
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_input},
            ],
            temperature=0.5,
        )

        # レスポンスからアシスタントの応答テキストを取り出して表示
        # SDK の応答形式によっては access path が異なる場合があるため、この行は
        # 必要に応じて調整してください。
        answer = response.choices[0].message.content
        st.subheader("アドバイス")
        st.write(answer)
    except Exception as e:
        # エラー内容をユーザーにわかりやすく表示
        st.error(f"エラーが発生しました: {e}")
