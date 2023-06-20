import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title='Multipage App',
    page_icon = "!@!@",
)

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data


def analyze_financials(company_data):
    company_data["재정상태"] = company_data["자산총계"] - company_data["부채총계"]
    recent_trend = company_data["재정상태"].iloc[-1] > company_data["재정상태"].iloc[0]
    positive_trend = "긍정적" if recent_trend else "부정적"
    return company_data, positive_trend

def analyze_stock_price(company_data):
    company_data["주가"] = company_data["시가총액"] / company_data["연간 총매출액"]
    return company_data

def analyze_profitability(company_data):
    company_data["수익성"] = company_data["매출총이익"] / company_data["총자산"]
    return company_data


st.markdown('<h1 style="font-size:30px;">- 💹주가, 기사, 재무제표 분석을 통한 데이터 분석</h1>', unsafe_allow_html=True)
st.sidebar.success("Select a page above.")

def main():
    tab11, tab12, tab13, tab14, tab15 = st.tabs(["프로젝트","데이터","테스트1","테스트2","테스트3"])
    with tab11:
        st.markdown( 
        """
        #### 1. 프로젝트 목적
        - 주식 투자 초심자들이 정보 탐색 인풋을 줄이고 안정적으로 자산을 운용할 수 있도록 돕기 위한 프로젝트입니다.
        #### 2. 프로젝트 개요
        - 주가, 기사, 재무제표 데이터를 바탕으로 종목의 주가를 분석.
        - 매도/매수 정보를 정리하여 시각화하고 그 인사이트를 제공해주는 서비스를 구현.
        
        
        """
        )
    
    with tab12:
        st.markdown(""" 
            #### - 주식 종목명을 선택해주세요.""")
        #주가데이터 
        df = load_data('all.csv')
        df1 = load_data('api.csv')
        
        grouped_data = df1.groupby("기업명")
        tab_list = list(grouped_data.groups.keys())
        
        # 탭 선택
        selected_tab = st.selectbox("기업 선택", tab_list)
        company_data = grouped_data.get_group(selected_tab)
     
        
        #여기다가는 상승 하락을 나타내주는것을 표시하면 어떨까?
        #col1, col2, col3, col4, col5, col6 = st.columns(6)
        #with col1:
        #    st.header('text')
        #
        #with col2:
        #    st.header('text')
    # 
        #with col3:
        #    st.header('text')
            
        #with col4:
        #    st.header('text')
            
        #with col5:
        #    st.header('text')
            
        #with col6:
        #    st.header('text')    
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["삼성전자", "현대차", "포스코", "셀트리온", "삼성생명"])
        
        with tab1:
            st.subheader("삼성전자")
            tab101, tab102, tab103, tab104 = st.tabs(["최근종가", "재정상태", "주가", "수익성"])
            with tab101:
                company_name = "삼성전자"
                df_samsung = df[df["Name"] == company_name]

                if not df_samsung.empty:
                    # 당일 종가 및 전날 대비 등락율 계산
                    df_samsung["Change"] = df_samsung["Close"].diff()
                    df_samsung["Change_pct"] = df_samsung["Change"] / df_samsung["Close"].shift() * 100

                    # 최신 데이터 가져오기.
                    latest_close = df_samsung["Close"].iloc[-1]
                    latest_change_pct = df_samsung["Change_pct"].iloc[-1]
                    
                    latest_close_formatted = '{:,.0f}'.format(latest_close)
                    

                    # 등락 여부에 따라 색상 설정
                    if latest_change_pct > 0:
                        change_color = "red"
                    elif latest_change_pct < 0:
                        change_color = "blue"
                    else:
                        change_color = "black"

                    # 당일 종가 메트릭 표시
                    st.metric("Latest Close Price", f"{latest_close_formatted}원")

                    # 전날 대비 등락율 텍스트 표시
                    st.markdown(f"<font color='{change_color}'>Change: {latest_change_pct:.2f}%</font>", unsafe_allow_html=True)
            with tab102:
                st.subheader("재정상태")
                analyzed_data, positive_trend = analyze_financials(company_data)
                if positive_trend == "긍정적":
                    st.write("재정상태 시간 흐름에 따른 추세:", f"<font color='red'>{positive_trend}</font>", "입니다!", unsafe_allow_html=True)
                else:
                    st.write("재정상태 시간 흐름에 따른 추세:", f"<font color='blue'>{positive_trend}</font>", "입니다!", unsafe_allow_html=True)

                st.write(analyzed_data[["사업년도", "재정상태"]])

                    
            with tab103:
                st.header('주가')
            with tab104:
                st.header('수익성')
        
        with tab2:
            st.subheader("현대차")
            tab101, tab102, tab103, tab104 = st.tabs(["최근종가", "재정상태", "주가", "수익성"])
            with tab101:
                company_name = "현대차"
                df_hyundai = df[df['Name'] == company_name]
                #당일 종가 및 전날 대비 등락율 계산
                df_hyundai["Change"] = df_hyundai["Close"].diff()
                
                df_hyundai["Change_pct"] = df_hyundai["Change"] / df_hyundai["Close"].shift() * 100
                # 최신 데이터 가져오기
                latest_close = df_hyundai["Close"].iloc[-1]
                latest_change_pct = df_hyundai["Change_pct"].iloc[-1]
                
                latest_close_formatted = '{:,.0f}'.format(latest_close)

                # 등락 여부에 따라 색상 설정
                if latest_change_pct > 0:
                    change_color = "red"
                elif latest_change_pct < 0:
                    change_color = "blue"
                else:
                    change_color = "black"

                # 당일 종가 메트릭 표시
                st.metric("Latest Close Price", f"{latest_close_formatted}원")

                # 전날 대비 등락율 텍스트 표시
                st.markdown(f"<font color='{change_color}'>Change: {latest_change_pct:.2f}%</font>", unsafe_allow_html=True)
            with tab102:
                st.header('재정상태')
            with tab103:
                st.header('주가')
            with tab104:
                st.header('수익성')
        with tab3:
            st.header("포스코")
            tab101, tab102, tab103, tab104 = st.tabs(["최근종가", "재정상태", "주가", "수익성"])
            with tab101:
                company_name = '포스코'
                df_posco = df[df["Name"] == company_name]

                df_posco["Change"] = df_posco["Close"].diff()
                
                df_posco["Change_pct"] = df_posco["Change"] / df_posco["Close"].shift() * 100
                # 최신 데이터 가져오기
                latest_close = df_posco["Close"].iloc[-1]
                latest_change_pct = df_posco["Change_pct"].iloc[-1]
                
                latest_close_formatted = '{:,.0f}'.format(latest_close)

                # 등락 여부에 따라 색상 설정
                if latest_change_pct > 0:
                    change_color = "red"
                elif latest_change_pct < 0:
                    change_color = "blue"
                else:
                    change_color = "black"

                # 당일 종가 메트릭 표시
                st.metric("Latest Close Price", f"{latest_close_formatted}원")

                # 전날 대비 등락율 텍스트 표시
                st.markdown(f"<font color='{change_color}'>Change: {latest_change_pct:.2f}%</font>", unsafe_allow_html=True)
            with tab102:
                st.header('재정상태')
                
            with tab103:
                st.header('주가')
            with tab104:
                st.header('수익성')
            
        with tab4:
            st.header("셀트리온")
            tab101, tab102, tab103, tab104 = st.tabs(["최근종가", "재정상태", "주가", "수익성"])
            with tab101:
                company_name = "셀트리온"
                df_celltrion = df[df["Name"] == company_name]
                df_celltrion["Change"] = df_celltrion["Close"].diff()
                
                df_celltrion["Change_pct"] = df_celltrion["Change"] / df_celltrion["Close"].shift() * 100
                # 최신 데이터 가져오기
                latest_close = df_celltrion["Close"].iloc[-1]
                latest_change_pct = df_celltrion["Change_pct"].iloc[-1]
                
                latest_close_formatted = '{:,.0f}'.format(latest_close)

                # 등락 여부에 따라 색상 설정
                if latest_change_pct > 0:
                    change_color = "red"
                elif latest_change_pct < 0:
                    change_color = "blue"
                else:
                    change_color = "black"

                # 당일 종가 메트릭 표시
                st.metric("Latest Close Price", f"{latest_close_formatted}원")

                # 전날 대비 등락율 텍스트 표시
                st.markdown(f"<font color='{change_color}'>Change: {latest_change_pct:.2f}%</font>", unsafe_allow_html=True)
            with tab102:
                st.header('재정상태')
            with tab103:
                st.header('주가')
            with tab104:
                st.header('수익성')
        with tab5:
            st.header("삼성생명")
            tab101, tab102, tab103, tab104 = st.tabs(["최근종가", "재정상태", "주가", "수익성"])
            with tab101:
                company_name = "삼성생명"
                df_s_life = df[df["Name"] == company_name]
                df_s_life["Change"] = df_s_life["Close"].diff()
                
                df_s_life["Change_pct"] = df_s_life["Change"] / df_s_life["Close"].shift() * 100
                # 최신 데이터 가져오기
                latest_close = df_s_life["Close"].iloc[-1]
                latest_change_pct = df_s_life["Change_pct"].iloc[-1]
                
                latest_close_formatted = '{:,.0f}'.format(latest_close)

                # 등락 여부에 따라 색상 설정
                if latest_change_pct > 0:
                    change_color = "red"
                elif latest_change_pct < 0:
                    change_color = "blue"
                else:
                    change_color = "black"

                # 당일 종가 메트릭 표시
                st.metric("Latest Close Price", f"{latest_close_formatted}원")

                # 전날 대비 등락율 텍스트 표시
                st.markdown(f"<font color='{change_color}'>Change: {latest_change_pct:.2f}%</font>", unsafe_allow_html=True)
            with tab102:
                st.header('재정상태')
            with tab103:
                st.header('주가')
            with tab104:
                st.header('수익성')
                
                
    with tab13:
        st.markdown("""
            #### 1. 전체 항목 주가데이터 그래프
            """)

        # 데이터 로드
        df = pd.read_csv('all.csv')
        stocks = sorted(df['Name'].unique())
        date = sorted(df['Date'].unique())

        # 사이드 바에서 선택할 수 있는 항목들
        selected_stocks = st.multiselect('Select Brands', stocks, default=stocks)
        start_year, end_year = st.select_slider('Select Year Range', options=date, value=(date[0], date[-1]))
        y_values = st.multiselect("Select y value", ["Close", "Open", "High", "Low", "Change", "MA_5", "slow_%K", "slow_%D,","RSI"])

        # 필터링
        mask = (
            df['Name'].isin(selected_stocks) &
            (df['Date'] >= start_year) & (df['Date'] <= end_year)
        )
        df_filtered = df.loc[mask]

        # 그래프 생성
        line_charts = []
        for y_value in y_values:
            chart = alt.Chart(df_filtered).mark_line().encode(
                x="Date:T",
                y=alt.Y(y_value + ":Q", title=y_value),
                color="Name:N"
            ).properties(
                width=1000,
                height=600
            )
            line_charts.append(chart)

        combined_chart = alt.vconcat(*line_charts)
        st.altair_chart(combined_chart)
    
    with tab14:
        st.subheader("test버전")
        
    
    with tab15:
        st.subheader("test버전")
        
    
    #파이차트: 점수 합 비율을 넣는 것 약간 매수/매도 사인 비슷할 수 있음.
    # 날씨 이미지(이모지: 크기가 조정 가능할 때), 주가 시계열 데이터 그래프, 전일 종가 데이터, 
    #CSV로 만든 그래프로 MA-5, CHANGE 보고 5일 합으로 이미지 출력하게 
    #세영님 코드 참고해서 해보기.
        



    

    
    #st.title("Title")
    #st.header("Header")
    #st.subheader("Subheader")
    
    #st.write("Write")
    
    
    
    
    #st.header("목적")
    #st.write ("주식 투자 초심자들이 정보탐색 인풋을 줄이고 안정적으로 자산을 운용할 수 있게 돕기 위해")
if __name__ == '__main__' :
    main()
    
