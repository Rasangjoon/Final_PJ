import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import locale

def main():
    df = pd.read_csv('all.csv')
    st.title('주식추천')
    st.subheader('주식 변동 추이')
    stocks = sorted(df['Name'].unique())
    selected_stocks = st.sidebar.multiselect('Select Brands', stocks, default=stocks[0])

    default_start_date = pd.to_datetime(df['Date']).min().to_pydatetime().date()  # 수정된 부분
    start_date = st.sidebar.date_input('Start Date', value=default_start_date)
    end_date = st.sidebar.date_input('End Date', value=datetime.now())
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    fig = go.Figure()

    for stock in selected_stocks:
        stock_data = df[(df['Name'] == stock) & (df['Date'] >= start_date) & (df['Date'] <= end_date)]
        fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'], name=stock,
                                 hovertemplate='날짜: %{x}<br>주식 가격: %{y:,.0f}'))
        price_diff = stock_data['Close'].diff()
        color = ['blue' if diff < 0 else 'red' for diff in price_diff]
        fig.add_trace(go.Bar(x=stock_data['Date'], y=stock_data['High'] - stock_data['Low'],
                             base=stock_data['Low'], name='Price Range', marker=dict(color=color),
                             hovertemplate='날짜: %{x}<br>가격 범위: %{y:,.0f}'))

        fig.update_layout(
            title='주식 가격 변동 추이',
            xaxis_title='날짜',
            yaxis_title='주식 가격',
            hovermode='x',
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            barmode='stack',
            autosize=False,
            width=800,
            height=500
        )

    # 천단위 쉼표 추가
    locale.setlocale(locale.LC_ALL, '')
    fig.update_yaxes(tickformat=",.0f")

    # 그래프 출력
    st.plotly_chart(fig)

    # 추가 그래프
    with st.expander('추가 그래프'):
        st.subheader('추가 그래프 선택')
        selected_indicators = st.multiselect('주가 지표를 선택하세요', ['MA', 'fast_%K', 'slow_%K'])

        for stock in selected_stocks:
            stock_data = df[(df['Name'] == stock) & (df['Date'] >= start_date) & (df['Date'] <= end_date)]
            fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'], name=stock,
                                    hovertemplate='날짜: %{x}<br>주식 가격: %{y:,.0f}'))

            for indicator in selected_indicators:
                if indicator == 'MA':
                    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['MA'], name=f'MA - {stock}',
                                            hovertemplate='날짜: %{x}<br>MA: %{y:.2f}'))
                elif indicator == 'fast_%K':
                    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['fast_%K'], name=f'fast_%K - {stock}',
                                            hovertemplate='날짜: %{x}<br>fast_%K: %{y:.2f}'))
                elif indicator == 'slow_%K':
                    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['slow_%K'], name=f'slow_%K - {stock}',
                                            hovertemplate='날짜: %{x}<br>slow_%K: %{y:.2f}'))


if __name__ == '__main__':
    main()