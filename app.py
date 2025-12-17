import streamlit as st
import pandas as pd
import numpy as np

# --- 計算邏輯 ---
def calculate_bmr(w, h_cm, age, gender):
    # Mifflin-St Jeor 公式
    val = (10 * w) + (6.25 * h_cm) - (5 * age)
    return val + 5 if gender == 'M' else val - 161

# --- 網頁設定 ---
st.set_page_config(page_title="體重模擬器", layout="wide")
st.title("⚖️ 體重變化動態模擬器")

# --- 側邊欄：輸入參數 ---
with st.sidebar:
    st.header("👤 個人基本資料")
    gender = st.selectbox("性別", ["M", "F"])
    height = st.number_input("身高 (cm)", value=175.0, step=0.1)
    weight = st.number_input("目前體重 (kg)", value=70.0, step=0.1)
    age = st.number_input("年齡", value=25, step=1)
    
    st.divider()
    st.header("🏃 生活型態")
    activity_map = {
        "久坐 (辦公室工作)": 1.2,
        "輕度 (每周運動 1-3 天)": 1.375,
        "中度 (每周運動 3-5 天)": 1.55,
        "高度 (每周運動 6-7 天)": 1.725,
        "極高 (高強度體力勞動)": 1.9
    }
    activity_label = st.selectbox("活動等級", options=list(activity_map.keys()))
    activity_val = activity_map[activity_label]
    
    intake = st.number_input("每日計畫攝取熱量 (kcal)", value=2000, step=50)

# --- 數據計算 ---
bmr = calculate_bmr(weight, height, age, gender)
tdee = bmr * activity_val
daily_diff = intake - tdee
# 預測 30 天體重路徑
days = np.arange(31)
weight_path = weight + (daily_diff * days / 7700)
final_weight = weight_path[-1]

# --- 主畫面顯示 ---
col1, col2, col3 = st.columns(3)
col1.metric("基礎代謝 (BMR)", f"{bmr:.0f} kcal")
col2.metric("每日消耗 (TDEE)", f"{tdee:.0f} kcal", f"{intake - tdee:.0f} kcal (缺口)", delta_color="inverse")
col3.metric("30天後預測體重", f"{final_weight:.2f} kg", f"{final_weight - weight:.2f} kg")

st.divider()

# --- 趨勢圖表 ---
st.subheader("📈 未來 30 天體重趨勢預測")
chart_data = pd.DataFrame({
    '天數': days,
    '預測體重 (kg)': weight_path
}).set_index('天數')

st.line_chart(chart_data)

# --- 科學小提示 ---
with st.expander("💡 關於計算邏輯"):
    st.write(f"""
    - **計算公式**：使用 Mifflin-St Jeor 公式。
    - **熱量缺口**：科學界普遍認為減少 7700 kcal 的熱量可減輕約 1 公斤體重。
    - **提醒**：此模擬器僅供參考，實際體重受水分、肌肉量及代謝補償影響，建議諮詢營養師。
    """)
