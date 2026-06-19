import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(
    page_title="🌍 글로벌 시총 TOP10 주식 대시보드",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #f8fbff 0%, #eef4ff 100%);
}
h1, h2, h3 {
    color: #1f2937;
}
.metric-card {
    padding: 18px;
    border-radius: 18px;
    background: white;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

st.title("🌍 글로벌 시가총액 TOP10 주식 대시보드")
st.caption("최근 1년간 주가 변화율을 Plotly로 시각화합니다.")

stocks = {
    "NVIDIA": "NVDA",
    "Alphabet": "GOOGL",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "TSMC": "TSM",
    "Broadcom": "AVGO",
    "Saudi Aramco": "2222.SR",
    "Tesla": "TSLA",
    "Meta": "META"
}

selected_companies = st.multiselect(
    "📌 비교할 기업을 선택하세요",
    options=list(stocks.keys()),
    default=list(stocks.keys())
)

end_date = datetime.today()
start_date = end_date - timedelta(days=365)

@st.cache_data
def load_stock_data(tickers, start, end):
    data = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False
    )

    if len(tickers) == 1:
        close = data[["Close"]]
        close.columns = tickers
    else:
        close = data["Close"]

    return close.dropna(how="all")

if selected_companies:
    selected_tickers = [stocks[name] for name in selected_companies]

    df = load_stock_data(selected_tickers, start_date, end_date)
    df = df.rename(columns={v: k for k, v in stocks.items()})

    normalized_df = df / df.iloc[0] * 100
    change_rate = ((df.iloc[-1] / df.iloc[0]) - 1) * 100

    col1, col2, col3 = st.columns(3)

    best_company = change_rate.idxmax()
    worst_company = change_rate.idxmin()
    avg_change = change_rate.mean()

    col1.metric("🚀 최고 상승 기업", best_company, f"{change_rate[best_company]:.2f}%")
    col2.metric("📉 최저 수익률 기업", worst_company, f"{change_rate[worst_company]:.2f}%")
    col3.metric("📊 평균 변화율", f"{avg_change:.2f}%")

    st.subheader("📈 최근 1년 주가 변화율 비교")
    st.caption("시작일 주가를 100으로 맞춰 기업별 상승·하락 흐름을 비교합니다.")

    fig = px.line(
        normalized_df,
        x=normalized_df.index,
        y=normalized_df.columns,
        title="글로벌 시총 TOP10 최근 1년 주가 변화",
        labels={
            "value": "기준화 주가",
            "Date": "날짜",
            "variable": "기업"
        }
    )

    fig.update_layout(
        height=650,
        hovermode="x unified",
        template="plotly_white",
        legend_title_text="기업",
        title_font_size=24
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏆 기업별 1년 수익률 순위")

    ranking_df = change_rate.sort_values(ascending=False).reset_index()
    ranking_df.columns = ["기업", "1년 변화율(%)"]

    fig_bar = px.bar(
        ranking_df,
        x="1년 변화율(%)",
        y="기업",
        orientation="h",
        text="1년 변화율(%)",
        title="최근 1년 수익률 순위",
    )

    fig_bar.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig_bar.update_layout(
        height=550,
        template="plotly_white",
        yaxis=dict(autorange="reversed")
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("💵 실제 종가 데이터")
    st.dataframe(df.tail(10), use_container_width=True)

else:
    st.warning("비교할 기업을 1개 이상 선택해주세요.")
