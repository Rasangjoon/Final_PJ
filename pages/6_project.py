import streamlit as st
import pandas as pd
import altair as alt

def main():
    df = pd.read_csv('all.csv')
    st.title('주린이들을 위한 주식추천')

    st.subheader('주식 변동 추이')

    stocks = sorted(df['Name'].unique())

    date = sorted(df['Date'].unique())

    # 사이드 바에서 종목명과 날짜를 고를 수 있게.
    selected_stocks = st.sidebar.multiselect('Select Brands', stocks, default=stocks)
    start_year, end_year = st.sidebar.select_slider('Select Year Range', options=date, value=(date[0], date[-1]))

    # 선택에 맞게 필터 만들기
    mask = (
        df['Name'].isin(selected_stocks) &
        (df['Date'] >= start_year) & (df['Date'] <= end_year)
    )
    df_filtered = df.loc[mask]

    # y_value를 선택하면 나올 수 있게 만들기
    y_values = st.sidebar.multiselect("Select y value", ["Close", "Open", "High", "Low", "Change", "MA_5", "slow_%K"])

    # 선택한 y 값으로 새로운 열 생성
    df_selected = df_filtered[["Date", "Name"] + y_values].copy()
    df_selected = df_selected.melt(id_vars=["Date", "Name"], value_vars=y_values, var_name="y_value", value_name="y")

    # 색상 설정을 위한 범주 리스트 생성
    color_scale = alt.Scale(domain=y_values, range=["red", "blue", "green", "orange", "purple", "pink", "brown"])

    # 라인 차트 생성
    line_chart = alt.Chart(df_selected).mark_line().encode(
        x="Date:T",
        y=alt.Y("y:Q", title="Y Value"),
        color=alt.Color("y_value:N", scale=color_scale, legend=alt.Legend(title="Y Value"))
    ).properties(
        width=1000,
        height=600
    )

    st.altair_chart(line_chart)

if __name__ == '__main__':
    main()