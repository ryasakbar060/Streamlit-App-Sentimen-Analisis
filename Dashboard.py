import streamlit as st
from PIL import Image

# Name Page
st.set_page_config(
    page_title="Dashboard" 
)

# Mengatur posisi judul di tengah halaman
st.write("<h1 style='text-align: center;'>Sentiment Analyze App</h1>", unsafe_allow_html=True)

# Mengatur posisi gambar di tengah halaman
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    image = Image.open('images/uyu.png')
    st.image(image, use_column_width=True)
st.subheader('\n\n')

st.write("<h4 style='text-align: center;'>Sentiment Analysis Opini Publik Terhadap Penggunaan Kendaraan Listrik Di Indonesia Pada Media Sosial Twitter Dengan Metode Algoritma Naive Bayes Classifier</h4>", unsafe_allow_html=True)
st.subheader('\n')

st.write("<h6 style='text-align: center;'>L. M. RYAS AMIN AKBAR<br>F1B019076</h6>", unsafe_allow_html=True)

st.sidebar.success("Welcome To System")