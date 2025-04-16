import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import io
from PIL import Image
#Оформление страницы
st.set_page_config(page_title='Иследование чаевых', page_icon='💸', layout='wide')
if st.button('← Главная страница'):
    st.switch_page("home.py")

st.title('Исследование распределения чаевых 💰')
st.badge("Tips", icon=":material/check:", color="green")
@st.cache_data
def load_data():
    path = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv'
    return  pd.read_csv(path)
tips= load_data()
#st.dataframe(tips.head(20))
st.markdown('Выбирай критерии и смотри результат')
# st.markdown("""
# <style>
#     .stButton>button {
#         display: block;
#         margin: 0 auto;
#     }
# </style>
# """, unsafe_allow_html=True)
# Создание кнопок и их настройка
col1, col2, col3 = st.columns(3)
with col1:
    show_hist= st.button('Гистограмма счетов')
with col2:
    show_scatter_sex= st.button('Связь между полом официанта и чаевыми')    
with col3:
    show_scatter_bill = st.button('Связь счета и чаевых')

def download_fig(fig, filename, text="Скачать график"):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    st.download_button(
        label=text,
        data=buf,
        file_name=filename,
        mime="image/png"
    )
# подгрузка графиков
if show_hist:
    st.subheader('Распределение сумм счетов')
    fig, ax = plt.subplots(figsize=(10,6))
    sns.histplot(data=tips,
                 x='total_bill',
                 bins=20,
                 kde=True,
                 color='#55ccea')
    st.pyplot(fig)
    download_fig(fig, "histogram_total_bill.png", "📥 Скачать гистограмму")
if show_scatter_sex:
    st.subheader('Распределение чаевых по полу')
    fig, ax = plt.subplots(figsize=(10,6))
    sns.scatterplot(data=tips,
                x='tip',
                y='day',
                hue='sex',
                palette=['pink','lightblue'],
                s=100,
                alpha=0.6,
                edgecolor='grey',
                legend=True)
    st.pyplot(fig)
    download_fig(fig, "scatter_tip_sex.png", "📥 Скачать график")
if show_scatter_bill:
    st.subheader('Связь между размерами счета и чаевых')  
    fig, ax = plt.subplots(figsize=(10,6))
    sns.scatterplot(data=tips,
                    x='total_bill',
                    y='tip',
                    hue='time',
                    palette='coolwarm')  
    st.pyplot(fig)
    download_fig(fig, "scatter_bill_tip.png", "📥 Скачать график")

with st.expander("Показать исходные данные"):
    st.dataframe(tips)

with st.sidebar:
    uploaded_file = st.file_uploader('***Загрузи*** свой CSV файл по чаевым в твоем ресторане ', type='csv')
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("Используются загруженные данные!")
    st.write(df.head(5))
else:
    st.stop()

# Исходные данные
with st.expander("📁 Показать исходные данные"):
    st.dataframe(tips)
    csv = tips.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Скачать данные (CSV)",
        data=csv,
        file_name="tips_data.csv",
        mime="text/csv"
    )

# Линейный график
st.subheader("Динамика сумм счетов")
st.line_chart(tips['total_bill'])    
# st.dataframe(tips)
# Загрузка CSV файла







