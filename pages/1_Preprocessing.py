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
def preprocess_text(text, lowercase=True, cleansing=True, remove_number=True,remove_punctuation=True, remove_single_char=True, remove_duplicate=True, tokenization=True, stopword_removal=True, stemming=True, slang_normalization=True):
    # Pembersihan teks dari tab, newline, link, hastag, URL, backslice, rt
    if cleansing:
        text = text.replace('\\t'," ").replace('\\n', " ").replace('\\u', " ").replace('\\'," ")
        text = text.encode('ascii','replace').decode('ascii')
        text = ' '.join(re.sub("([@#][A-Za-z0-9_]+)|(\w+:\/\/\S+)","",text).split())
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
        # text = text.translate(str.maketrans("", "", string.punctuation))
        text = re.sub(r"(?<=\w)[^\s\w]+(?=\w)", " ", text)

    # Remove single char
    if remove_single_char:
        text = re.sub(r"\b[a-zA-Z]\b", "", text)
    
    # Tokenisasi
    if tokenization:
        tokens = nltk.word_tokenize(text)

    # Stopword removal
    if stopword_removal:
        list_stopwords = nltk.corpus.stopwords.words('indonesian')
        list_stopwords.extend(['yg', 'dg', 'rt', 'dgn', 'ny', 'd', 'u', 'klo',
                       'kalo', 'amp', 'biar', 'bikin', 'bilang',
                       'gak', 'ga', 'krn', 'nya', 'nih', 'sih',
                       'si', 'tau', 'tdk', 'tuh', 'utk', 'ya',
                       'jd', 'jgn', 'sdh', 'aja', 'n', 't', 'p', 'ak',
                       'nyg', 'hehe', 'pen', 'u', 'nan', 'loh', 'rt',
                       '&amp', 'yah', 'ri', 'dci', 'di', 'iims', 'ge', 
                       'eeehhhh', 'cman', 'pj', 'wkwkwkwk', 'kyk', 'jrg',
                       'nyahnyoh'])
        txt_stopword = pd.read_csv("stopwords.txt", names= ["stopwords"], header = None)
        list_stopwords.extend(txt_stopword["stopwords"][0].split(' '))
        list_stopwords = set(list_stopwords)
        tokens = [word for word in tokens if not word in list_stopwords]

    # Stemming
    if stemming:
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        tokens = [stemmer.stem(word) for word in tokens]

    # Menggabungkan kembali token-token menjadi kalimat
    text = " ".join(tokens)
    
    # Normalisasi kata slang menggunakan kamus kata slang
    if slang_normalization:
        df_slang = pd.read_excel("normalisasi.xlsx")
        slang_dict = dict(zip(df_slang['original'], df_slang['replacement']))
        text = ' '.join([slang_dict[word] if word in slang_dict else word for word in text.split()])

    # Remove duplicates
    if remove_duplicate:
        df.drop_duplicates(subset ='Text', keep ='first', inplace = True)
    
    # Mengembalikan teks yang telah dipreprocessing
    return text
# Main program
st.title("Preprocessing Data")

# Mengunggah file Excel
uploaded_file = st.file_uploader("Upload File Dataset Excel", type=["xlsx"])
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
        
    # Checkbox untuk tokenize
    tokenization = st.checkbox("Tokenizing")
    
    # Checkbox untuk stopwordwords
    stopword_removal = st.checkbox("Stopwords")
    
    # Checkbox untuk stemming
    stemming = st.checkbox("Stemming")

    # Checkbox untuk normalisasi
    slang_normalization = st.checkbox("Normalisasi")

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
            remove_number=remove_number,remove_punctuation=remove_punctuation, remove_single_char=remove_single_char, remove_duplicate=remove_duplicate, tokenization=tokenization, stopword_removal=stopword_removal, stemming=stemming, slang_normalization=slang_normalization)
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