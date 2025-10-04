
import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import plotly.express as px
import plotly.graph_objects as go

# --- 網頁配置 ---
st.set_page_config(
    page_title="簡單線性回歸分析 (CRISP-DM)",
    page_icon="📊",
    layout="wide"
)

# --- 主標題 ---
st.title("📊 HW1 - 簡單線性回歸可視化網站")
st.write("本網站將依據 **CRISP-DM** 流程，帶您從無到有建立一個簡單線性回歸模型，並將結果可視化。")

# --- CRISP-DM 流程 ---

# 1. Business Understanding (商業理解)
with st.expander("第一步：Business Understanding (商業理解)", expanded=True):
    st.header("🎯 商業理解")
    st.markdown("""
    **目標：** 我們的目標是建立一個能夠「預測」的工具。給定一個自變數 X，我們希望能夠預測出應變數 y 的值。
    
    **情境：** 假設我們想探討「廣告投入（X）」與「產品銷售額（y）」之間的關係。我們相信，廣告投得越多，銷售額應該會越高，且它們之間存在一種線性關係。
    
    **任務：**
    1.  生成一組模擬資料，代表廣告投入與銷售額。
    2.  使用簡單線性回歸模型（`y = aX + b`）來找出兩者之間的關係。
    3.  評估這個模型的好壞，例如 R² 分數和均方誤差（MSE）。
    4.  將這個模型部署成一個互動式網頁，讓使用者可以調整參數，觀察模型的變化。
    """)

# --- 使用者自訂參數 (Sidebar) ---
st.sidebar.header("⚙️ 自訂參數")
st.sidebar.markdown("請調整以下參數來生成您的模擬資料：")

a = st.sidebar.slider("真實斜率 (a)", min_value=-10.0, max_value=10.0, value=2.5, step=0.1)
b = st.sidebar.slider("真實截距 (b)", min_value=-20.0, max_value=20.0, value=5.0, step=0.5)
noise = st.sidebar.slider("雜訊強度 (noise)", min_value=0.0, max_value=20.0, value=5.0, step=0.5)
num_points = st.sidebar.slider("資料點數量 (num_points)", min_value=10, max_value=1000, value=100, step=10)

# 2. Data Understanding (資料理解)
st.header("📊 第二步：Data Understanding (資料理解)")
with st.expander("點此查看資料理解的細節", expanded=True):
    st.markdown(f"""
    我們將根據您在左側設定的參數來生成資料。
    - **自變數 X：** 我們會隨機生成 `{num_points}` 個介於 0 到 10 之間的數值，模擬「廣告投入」。
    - **應變數 y：** 根據公式 `y = {a} * X + {b} + noise` 來計算，模擬「產品銷售額」。
    - **雜訊 (Noise)：** 為了讓資料更貼近真實世界，我們加入了標準差為 `{noise}` 的隨機雜訊。
    
    下方是生成資料的預覽：
    """)
    
    # 3. Data Preparation (資料準備)
    @st.cache_data
    def generate_data(a, b, noise, num_points):
        X = np.random.rand(num_points, 1) * 10
        random_noise = np.random.randn(num_points, 1) * noise
        y = a * X + b + random_noise
        df = pd.DataFrame({'X (廣告投入)': X.flatten(), 'y (實際銷售額)': y.flatten()})
        return df, X, y

    df, X, y = generate_data(a, b, noise, num_points)
    st.dataframe(df.head())


# 4. Modeling (模型建立)
st.header("🤖 第三步 & 第四步：Data Preparation & Modeling")
with st.expander("點此查看資料準備與模型建立的細節", expanded=True):
    st.markdown("""
    **Data Preparation (資料準備):**
    - 在這一步，我們已經將生成的 `X` 和 `y` 整理成模型可以接受的格式（Numpy 陣列與 Pandas DataFrame）。
    - 由於這是模擬資料，我們不需要進行複雜的清洗或特徵工程。
    
    **Modeling (模型建立):**
    - 我們選用 `scikit-learn` 函式庫中的 `LinearRegression` 作為我們的模型。
    - 模型會學習 `X` 和 `y` 之間的線性關係，並找出最適合的「斜率」和「截距」，以最小化預測誤差。
    """)
    
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    df['y_pred (模型預測銷售額)'] = y_pred
    
    st.success("模型訓練完成！")


# 5. Evaluation (模型評估)
st.header("📈 第五步：Evaluation (模型評估)")
with st.expander("點此查看模型評估的細節", expanded=True):
    st.markdown("""
    模型的好壞需要量化指標來衡量。我們使用以下三個指標：
    - **模型斜率 (Coefficient):** 模型學習到的斜率，理想上應該接近我們設定的真實斜率 `a`。
    - **R² 分數 (R-squared):** 介於 0 到 1 之間，表示模型能解釋應變數變異的百分比。越接近 1 表示模型解釋力越強。
    - **均方誤差 (Mean Squared Error, MSE):** 預測值與真實值差距的平方平均。值越小表示模型的預測越精準。
    """)
    
    # 計算指標
    model_coef = model.coef_[0][0]
    model_intercept = model.intercept_[0]
    r2 = r2_score(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("模型斜率 (Coefficient)", f"{model_coef:.2f}", f"真實斜率 a: {a}")
    col2.metric("R² 分數 (R-squared)", f"{r2:.3f}")
    col3.metric("均方誤差 (MSE)", f"{mse:.2f}")


# 6. Deployment (部署與視覺化)
st.header("🚀 第六步：Deployment (部署與視覺化)")
with st.expander("點此查看部署與視覺化的細節", expanded=True):
    st.markdown("""
    最後一步是將我們的成果部署成一個可互動的應用程式。
    - **散點圖 (Scatter Plot):** 藍色的點代表我們生成的原始資料（廣告投入 vs. 實際銷售額）。
    - **回歸線 (Regression Line):** 紅色的線是我們的線性回歸模型，代表模型預測的趨勢。
    
    您可以試著調整左側的參數，特別是「雜訊強度」，觀察它對 R² 分數和 MSE 的影響。雜訊越大，資料點越分散，模型就越難找到一個好的趨勢線，R² 會下降，MSE 會上升。
    """)
    
    # 使用 Plotly 進行視覺化
    fig = px.scatter(
        df, x='X (廣告投入)', y='y (實際銷售額)',
        title="資料散點與線性回歸線",
        labels={'X (廣告投入)': '廣告投入 (X)', 'y (實際銷售額)': '銷售額 (y)'}
    )
    
    # 新增回歸線
    fig.add_trace(
        go.Scatter(
            x=df['X (廣告投入)'], y=df['y_pred (模型預測銷售額)'],
            mode='lines',
            name='回歸線',
            line=dict(color='red', width=3)
        )
    )
    
    fig.update_layout(
        legend_title_text='圖例',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.sidebar.info("專案由 Gemini AI Agent 完成。")
