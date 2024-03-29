# -*- coding: utf-8 -*-
"""MovieSystemRecommendation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bIOv2i7pkTprpvdP8pE8Se8xssglggi2
"""

import pandas as pd

"""# Data Understanding"""

from google.colab import drive
drive.mount('/content/drive')

!unzip /content/drive/MyDrive/machineLearningTerapan/TheMoviesDataset.zip

"""##Data Movies"""

movies = pd.read_csv('/content/movies_metadata.csv')

movies.info()

# menghapus data null pada kolom title
movies.dropna(subset=['title'], inplace=True)

movies['id'] = movies['id'].astype(int)

movies.head(1)

"""## Data Links"""

links = pd.read_csv('/content/links_small.csv')

links.info()

#melakukan filter data null dan mengambil nilai dari tmdbId
links = links[links['tmdbId'].notnull()]
links = links['tmdbId'].astype('int')

links.head()

"""## Data Credits"""

credits = pd.read_csv('/content/credits.csv')

credits.info()

credits.head(2)

"""## Data Keywords"""

keywords = pd.read_csv('/content/keywords.csv')

keywords.info()

keywords.head(2)

"""## Dataset gabungan"""

# membuat dataset gabungan
data = movies.merge(credits, on='id')
data = data.merge(keywords, on='id')
data = data[data['id'].isin(links)]
data.shape

"""#Sistem Rekomendasi dengan Content Based Filtering

##Data Preprocessing
"""

import numpy as np
from ast import literal_eval
from nltk.stem import SnowballStemmer

data_prep = data.copy()

data_prep.head(1)

data_prep.columns

"""### Kolom crew

hanya mengambil nama sutradara
"""

print(data_prep['crew'].iloc[0])

data_prep['crew'] = data_prep['crew'].apply(literal_eval)

# fungsi untuk mengambil nama sutradara
def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

data_prep['director'] = data_prep['crew'].apply(get_director)

data_prep['director'].head(2)

"""menghilangkan spasi dan membuat nama sutradara 3 kali agar memiliki bobot yang sama dengan kolom cast"""

data_prep['director'] = data_prep['director'].astype('str').apply(lambda x: str.lower(x.replace(" ", "")))

data_prep['director'] = data_prep['director'].apply(lambda x: [x,x, x])

data_prep['director'].head(2)

"""###Kolom cast

mengambil maksimal 3 orang dari daftar pemeran
"""

print(data_prep['cast'].iloc[0])

data_prep['cast'] = data_prep['cast'].apply(literal_eval)

# jka terdapat data mengambil 3 pemeran film, jika tidak []
data_prep['cast'] = data_prep['cast'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
data_prep['cast'] = data_prep['cast'].apply(lambda x: x[:3] if len(x) >=3 else x)

data_prep['cast'].head(2)

data_prep['cast'] = data_prep['cast'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])

data_prep['cast'].head(2)

"""### Kolom keywords"""

print(data_prep['keywords'].iloc[0])

data_prep['keywords'] = data_prep['keywords'].apply(literal_eval)

# jika ada data tampilkan, jika tidak []
data_prep['keywords'] = data_prep['keywords'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

#membuat objek baru berisikan daftar keywords
sample = data_prep.apply(lambda x: pd.Series(x['keywords']),axis=1).stack().reset_index(level=1, drop=True)
sample.name = 'keyword'

print(sample)

# menghitung keywords yang sering muncul
sample = sample.value_counts()
sample[:10]

# menghapus kyewords yang hanya muncul sekali
sample = sample[sample > 1]

# fungsi menyaring keywords sesuai keyword sample
def filter_keywords(x):
    words = []
    for i in x:
        if i in sample:
            words.append(i)
    return words

data_prep['keywords'] = data_prep['keywords'].apply(filter_keywords)

# mengubah keyword menjadi asal kata, jumping -> jump
stemmer = SnowballStemmer('english')
data_prep['keywords'] = data_prep['keywords'].apply(lambda x: [stemmer.stem(i) for i in x])

# menghilangkan spasi dan rata huruf kecil
data_prep['keywords'] = data_prep['keywords'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])

"""### Kolom genres"""

#mengisi nilai null dengan[]
data_prep['genres'] = data_prep['genres'].fillna('[]')

data_prep['genres'] = data_prep['genres'].apply(literal_eval)

#menganbil nilai genres, jika tidak []
data_prep['genres'] = data_prep['genres'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

"""### Kolom baru

menambah kolom baru dari data keyword, cast, director dan genres
"""

data_prep['info'] = data_prep['keywords'] + data_prep['cast'] + data_prep['director'] + data_prep['genres']
data_prep['info'] = data_prep['info'].apply(lambda x: ' '.join(x))

"""##TF-IDF Vectorizer"""

data_fix = data_prep.copy()

from sklearn.feature_extraction.text import TfidfVectorizer

# Inisialisasi TfidfVectorizer
tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')

# Melakukan perhitungan idf pada data info
tf.fit(data_fix['info'])

# Mapping array dari fitur index integer ke fitur nama
tf.get_feature_names_out()

# Melakukan fit lalu ditransformasikan ke bentuk matrix
tfidf_matrix = tf.fit_transform(data_fix['info'])

# Melihat ukuran matrix tfidf
tfidf_matrix.shape

# Mengubah vektor tf-idf dalam bentuk matriks dengan fungsi todense()
tfidf_matrix.todense()

"""##Cosine Similarity"""

from sklearn.metrics.pairwise import cosine_similarity

# Menghitung cosine similarity pada matrix tf-idf
cosine_sim = cosine_similarity(tfidf_matrix)
cosine_sim

# Membuat dataframe dari variabel cosine_sim dengan baris dan kolom berupa title
cosine_sim_df = pd.DataFrame(cosine_sim, index=data_fix['title'], columns=data_fix['title'])
print('Shape:', cosine_sim_df.shape)

# Melihat similarity matrix pada setiap film
cosine_sim_df.sample(5, axis=1).sample(10, axis=0)

"""##Mendapatkan Rekomendasi"""

def movie_recommendations(title, similarity_data=cosine_sim_df, items=data_fix[['title','genres']], k=10):

    index = similarity_data.loc[:,title].to_numpy().argpartition(
        range(-1, -k, -1))

    # Mengambil data dengan similarity terbesar dari index yang ada
    closest = similarity_data.columns[index[-1:-(k+2):-1]]

    # Drop nama_resto agar nama resto yang dicari tidak muncul dalam daftar rekomendasi
    closest = closest.drop(title, errors='ignore')

    return pd.DataFrame(closest).merge(items).head(k)

data_fix[data_fix.title.eq('Toy Story')]

# Mendapatkan rekomendasi film yang mirip dengan Toy Story
movie_recommendations('Toy Story')

"""#Rekomendasi berdasarkan Collaborative Filtering

## Data Understanding
"""

# Import library
from zipfile import ZipFile
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path
import matplotlib.pyplot as plt

df = pd.read_csv('/content/ratings_small.csv')

df

"""##Data Preparation"""

# Mengubah movieId menjadi list tanpa nilai yang sama
movie_ids = df['movieId'].unique().tolist()

# Melakukan encoding movieId
movie_to_movie_encoded = {x: i for i, x in enumerate(movie_ids)}

# Melakukan proses encoding angka ke ke movieId
movie_encoded_to_movie = {i: x for i, x in enumerate(movie_ids)}

# Mapping movieId ke dataframe movie
df['movie'] = df['movieId'].map(movie_to_movie_encoded)

# Mendapatkan jumlah user
num_users = len(df['userId'])
print(num_users)

# Mendapatkan jumlah resto
num_movies = len(movie_to_movie_encoded)
print(num_movies)

# Mengubah rating menjadi nilai float
df['rating'] = df['rating'].values.astype(np.float32)

# Nilai minimum rating
min_rating = min(df['rating'])

# Nilai maksimal rating
max_rating = max(df['rating'])

print('Number of User: {}, Number of movies: {}, Min Rating: {}, Max Rating: {}'.format(
    num_users, num_movies, min_rating, max_rating
))

"""##Membagi Data untuk Training dan Validasi"""

# Mengacak dataset
df = df.sample(frac=1, random_state=42)
df

# Membuat variabel x untuk mencocokkan data user dan movies menjadi satu value
x = df[['userId', 'movieId']].values

# Membuat variabel y untuk membuat rating dari hasil
y = df['rating'].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values

# Membagi menjadi 80% data train dan 20% data validasi
train_indices = int(0.8 * df.shape[0])
x_train, x_val, y_train, y_val = (
    x[:train_indices],
    x[train_indices:],
    y[:train_indices],
    y[train_indices:]
)

print(x, y)

"""##Proses Training"""

class RecommenderNet(tf.keras.Model):

  # Insialisasi fungsi
  def __init__(self, num_users, num_movies, embedding_size, **kwargs):
    super(RecommenderNet, self).__init__(**kwargs)
    self.num_users = num_users
    self.num_resto = num_movies
    self.embedding_size = embedding_size
    self.user_embedding = layers.Embedding( # layer embedding user
        num_users,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.user_bias = layers.Embedding(num_users, 1) # layer embedding user bias
    self.resto_embedding = layers.Embedding( # layer embeddings resto
        num_movies,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.movie_bias = layers.Embedding(num_movies, 1) # layer embedding resto bias

  def call(self, inputs):
    user_vector = self.user_embedding(inputs[:,0]) # memanggil layer embedding 1
    user_bias = self.user_bias(inputs[:, 0]) # memanggil layer embedding 2
    resto_vector = self.resto_embedding(inputs[:, 1]) # memanggil layer embedding 3
    movie_bias = self.movie_bias(inputs[:, 1]) # memanggil layer embedding 4

    dot_user_movie = tf.tensordot(user_vector, resto_vector, 2)

    x = dot_user_movie + user_bias + movie_bias

    return tf.nn.sigmoid(x) # activation sigmoid

model = RecommenderNet(num_users, num_movies, 50) # inisialisasi model

# model compile
model.compile(
    loss = tf.keras.losses.BinaryCrossentropy(),
    optimizer = keras.optimizers.Adam(learning_rate=0.001),
    metrics=[tf.keras.metrics.RootMeanSquaredError()]
)

# Memulai training

history = model.fit(
    x = x_train,
    y = y_train,
    batch_size = 8,
    epochs = 10,
    validation_data = (x_val, y_val)
)

"""##Visualisasi Metrik"""

plt.plot(history.history['root_mean_squared_error'])
plt.plot(history.history['val_root_mean_squared_error'])
plt.title('model_metrics')
plt.ylabel('root_mean_squared_error')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

"""##Mendapatkan Rekomendasi Movie"""

movie_df = data_fix
df = pd.read_csv('/content/ratings_small.csv')

# Mengambil sample user
user_id = df.userId.sample(1).iloc[0]
movie_watched_by_user = df[df.userId == user_id]

movie_not_watched = movie_df[~movie_df['id'].isin(movie_watched_by_user.movieId.values)]['id']
movie_not_watched = list(
    set(movie_not_watched)
    .intersection(set(movie_to_movie_encoded.keys()))
)

movie_not_watched = [[movie_to_movie_encoded.get(x)] for x in movie_not_watched]
user_encoder = df['userId'].get(user_id)
user_movie_array = np.hstack(
    ([[user_encoder]] * len(movie_not_watched), movie_not_watched)
)

ratings = model.predict(user_movie_array).flatten()

top_ratings_indices = ratings.argsort()[-10:][::-1]
recommended_movie_ids = [
    movie_encoded_to_movie.get(movie_not_watched[x][0]) for x in top_ratings_indices
]

print('Showing recommendations for users: {}'.format(user_id))
print('===' * 9)
print('Movie with high ratings from user')
print('----' * 8)

top_movie_user = (
    movie_watched_by_user.sort_values(
        by = 'rating',
        ascending=False
    )
    .head(5)
    .movieId.values
)

movie_df_rows = movie_df[movie_df['id'].isin(top_movie_user)]
for row in movie_df_rows.itertuples():
    print(row.title)

print('----' * 8)
print('Top 10 movie recommendation')
print('----' * 8)

recommended_movie = movie_df[movie_df['id'].isin(recommended_movie_ids)]
for row in recommended_movie.itertuples():
    print(row.title)