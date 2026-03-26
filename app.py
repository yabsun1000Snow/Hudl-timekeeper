import streamlit as st
import requests
from datetime import datetime
import pytz

# ==========================================
# ★ここに先ほど取得したGoogle Apps ScriptのURLを貼り付けます！
# ==========================================
GAS_URL = st.secrets["GAS_URL"]
# 練習メニューのリスト（必要に応じてチームのメニューに書き換えてください）
PRACTICE_MENUS = [
    "基礎練", "Kick", "Punt", "FG", 
    "D", "O", "After", "Kick After"
]

# スマホで見やすいように画面を設定
st.set_page_config(page_title="Hudl打刻アプリ", page_icon="🏈", layout="centered")

st.title("🏈 練習メニュー打刻")
st.write("メニューが始まる瞬間にボタンをタップ！")

# ボタンをスマホで押しやすいように2列に並べる
cols = st.columns(2)

for i, menu in enumerate(PRACTICE_MENUS):
    with cols[i % 2]:
        # use_container_width=True でボタンを横幅いっぱいに広げる
        if st.button(menu, use_container_width=True):
            # クラウド上でも必ず日本時間になるように設定
            tokyo_tz = pytz.timezone('Asia/Tokyo')
            now = datetime.now(tokyo_tz)
            time_str = now.strftime("%H:%M:%S")
            
            # スプレッドシート（GAS）にデータを送信
            try:
                with st.spinner('送信中...'):
                    params = {"time": time_str, "name": menu}
                    response = requests.get(GAS_URL, params=params)
                
                if response.text == "Success":
                    st.success(f"✅ {time_str} - 「{menu}」を記録しました！")
                else:
                    st.error("データの送信に失敗しました（URLが間違っている可能性があります）。")
            except Exception as e:
                st.error(f"通信エラーが発生しました: {e}")
