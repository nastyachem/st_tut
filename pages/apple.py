import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from  datetime import datetime

st.set_page_config(page_title='Котировки компании Apple',page_icon='🍏',layout='wide')


if st.button('← Главная страница'):
    st.switch_page("home.py")

@st.cache_data
def load_data(ticker, start_date, end_date):
    data = yf.Ticker(ticker)
    return data.history(period='1d', start=start_date, end=end_date)

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg",width=100)
    st.markdown("[Сайт Apple](https://www.apple.com)", unsafe_allow_html=True)
    st.subheader("Настройки данных")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Начальная дата", value=datetime(2010, 1, 1))
    with col2:
        end_date = st.date_input("Конечная дата", value=datetime.today())
    st.subheader("Дополнительно")
    show_raw_data = st.checkbox("Показать исторические данные")
    #chart_theme = st.selectbox("Тема графиков", ["light", "dark"])

st.title('Котировки компании Apple')
st.markdown('''Сайт предоставляет информацию о котировках компании Apple''')
         
try:
    df = load_data('AAPL', start_date, end_date)
# tickerSymbol = 'AAPL'
    st.subheader('Ключевые показатели')
    col1, col2, col3 = st.columns(3)
    col1.metric('Текущая цена', f"${df['Close'].iloc[-1]:.2f}",
                f"{df['Close'].iloc[-1] - df['Close'].iloc[-2]:.2f}")
    col2.metric("Максимальная цена", f"${df['High'].max():.2f}",
                f"Дата: {df['High'].idxmax().strftime('%Y-%m-%d')}")
    col3.metric("Средний объем", f"{df['Volume'].mean():,.0f} акций")
# tickerData = yf.Ticker(tickerSymbol)
    st.subheader('Динамика цен закрытия')
    st.line_chart(df['Close'], use_container_width=True)

    st.subheader('Объемы торгов')
    st.area_chart(df['Volume'], use_container_width=True)

    st.subheader('Анализ волатильность')
    df['Daily Return'] = df['Close'].pct_change()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,5))
    sns.histplot(df['Daily Return'].dropna(), bins=100, color='blue', ax=ax1)
    ax1.set_title('Рапределение дневных изменений')

    sns.boxplot(x=df['Daily Return'].dropna(),ax=ax2)
    ax2.set_title('Boxplot дневных изменений')
    st.pyplot(fig)

    if show_raw_data:
        st.subheader('Исторические данные')
        st.dataframe(df.sort_index(ascending=False).style.format({
            'Open': '{:.2f}',
            'High': '{:.2f}',
            'Low': '{:.2f}',
            'Close':'{:.2f}',
            'Volume':'{:,}'
        }), use_container_width=True)

except Exception as e:
    st.error(f'Произошла ошибка при загрузке данных: {e}')
    st.info('Попробуйте изменить даты или проверьте подключение к интернету')

st.markdown('---')





