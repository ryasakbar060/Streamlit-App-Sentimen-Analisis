import streamlit as st
import pandas as pd
import string
import re
import nltk
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from io import BytesIO
import xlsxwriter
import base64

# Fungsi untuk melakukan preprocessing pada teks
def preprocess_text(text, lowercase=True, cleansing=True, remove_number=True,remove_punctuation=True, remove_single_char=True, remove_duplicate=True):
    # Pembersihan teks dari tab, newline, link, hastag, URL, backslice, rt
    if cleansing:
        text = text.replace('\\t'," ").replace('\\n', " ").replace('\\u', " ").replace('\\'," ")
        text = text.encode('ascii','replace').decode('ascii')
        text = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)","",text).split())
        text = re.sub(r'RT', '', text)
        text = text.replace("http://", "").replace("https://", "")
        df['Text'] = df['Text'].str.lstrip()
    
    # Mengubah huruf menjadi huruf kecil
    if lowercase:
        text = text.lower()

    # Menghapus angka (Remove Number)
    if remove_number:
        text = re.sub(r"\d+", "", text)

    # Menghilangkan tanda baca (Remove punctuation)
    if remove_punctuation:
        text = text.translate(str.maketrans("","",string.punctuation))

    # Remove single char
    if remove_single_char:
        text = re.sub(r"\b[a-zA-Z]\b", "", text)

    # Remove duplicates
    if remove_duplicate:
        df.drop_duplicates(subset ='Text', keep ='first', inplace = True)
    
    # Mengembalikan teks yang telah dipreprocessing
    return text
# Main program
st.title("Preprocessing Data")

# Mengunggah file Excel
uploaded_file = st.file_uploader("Unggah file Dataset Excel", type="xlsx")
if uploaded_file is not None:
    # Membaca file Excel
    df = pd.read_excel(uploaded_file)

    # Menampilkan teks dalam bentuk tabel
    st.write(df)

    # Checkbox untuk pembersihan teks dari tab, newline, link, hastag, URL, backslice, rt
    cleansing = st.checkbox("Cleaning Unique Char")

    # Checkbox untuk mengubah huruf menjadi huruf kecil
    lowercase = st.checkbox("Lower Case")

    # Checkbox untuk remove number
    remove_number = st.checkbox("Remove Number")

    # Checkbox untuk menghilangkan tanda baca
    remove_punctuation = st.checkbox("Remove Punctuation")

    # Checkbox untuk remove single char
    remove_single_char = st.checkbox("Remove Single Char")
    
    # Checkbox untuk remove duplikat
    remove_duplicate = st.checkbox("Remove Duplicate")

    # Button untuk memulai preprocessing
    if st.button("Preprocessing"):
        # Melakukan preprocessing pada setiap teks dalam file Excel

        for i in range(len(df)):
            if i in df.index:
                text = df.loc[i, "Text"]
            else:
                print(f"Index {i} is not valid for DataFrame")
            # text = df.loc[i, "Text"]
            preprocessed_text = preprocess_text(text, lowercase=lowercase, cleansing=cleansing,
            remove_number=remove_number,remove_punctuation=remove_punctuation, remove_single_char=remove_single_char, remove_duplicate=remove_duplicate)
            df.loc[i, "Text"] = preprocessed_text
        
        df.reset_index(drop=True, inplace=True)

        # Menampilkan hasil preprocessing dalam bentuk tabel
        st.write(df)

        def download_excel(df):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            processed_data = output.getvalue()
            b64 = base64.b64encode(processed_data)
            href = f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="processing-data.xlsx">Download Hasil Preprocessing</a>'
            return href

        st.markdown(download_excel(df), unsafe_allow_html=True)
