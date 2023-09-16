# Laporan Proyek Machine Learning - Muhammad Zaki

## Project Overview

Sistem rekomendasi film merupakan sistem yang membantu pengguna menemukan film berdasarkan minatnya. Dengan adanya sistem tersebut pengguna dapat dengan mudah melakukan pemilihan film, menghemat waktu dengan menonton film yang dia sukai dan meningkatkan kepuasan pengguna. Tidak hanya terbatas pada pengguna, sistem rekomendasi ini juga memeberikan manfaat kepada penyedia langganan. jika pengguna puas pada layanan yang diberikan platform _straming_ maka ia akan memperpanjang langganannya hal ini menjadi keuntungan bagi penyedia layanan dalam memepertahakan pengguna. Sistem ini menggunakan analisis data dan pembelajaran mesin untuk memberikan rekomendasi yang tepat kepada pengguna.

## Business Understanding

Untuk pelaku bisnis platform _streaming_, upaya dalam meningkatkan kepuasan pengguna sangat penting. jika _user experience_ bagus maka akan berdampak baikkepada platform _streaming_ tersebut. jika pengguna merasa puas dengan sistem rekomendasinya maka dia akan memiliki kemungkinan yang tinggi dalam memperpanjang langganannya dan memiliki kemunhkinan untuk merekomendasikan kepada kenalan mereka. hal ini berdampak keuntungan penyedia platform dalam mempertahankan dan menambah pengguna baru.
### Problem Statements
- metode apa saja yang digunakan untuk membuat sistem rekomendasi?
- bagaimana menentukan apakah sistem tersebut berjalan dengan baik?

### Goals

- membuat 2 model sistem rekomendasi berdasarkan konten film seperti nama sutradara, pemain dan genre film, tersebut dan juga berdasarkan preferensi pengguna yang memberikan penilaian.
- menggunakan matriks evaluasi pada saat melatih model untuk melihat peforma model

    ### Solution statements
    - untuk sistem rekomendasi berdasarkan konten digunakan model _content based filtering_ dan untuk sisten rekomendasi berdasarkan preferensi user digunakan model _collaborative filtering_
    - matriks yang digunakan untuk melihat pefroma model atau indeks kepuasan pelanggan yaitu RMSE atau root mean squared error. semakin kecil nilai mse maka semakin bagus model rekomendasinya

## Data Understanding
Data yang digunakan diambil dari kaggle [The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset). Dataset ini mengandung lebih dari 45000 film yang rilis sebelum juli 2017. Memiliki 7 file CSV:
- credits.csv. berisi orang yang terlibat dalam pembuatan film seperti sutardara dan kru lainnya

  pada file credits.csv terdapat 3 kolom:
    - kolom cast    : berisi data pemeran dalam film
    - kolom crew    : beisi data sutradara, ediotor dll
    - kolom id      : berisi nilai unik film
- keywords.csv. beisi kata kunci dari setiap film

  pada file keywords.csv terdapat 2 kolom:
  - kolom id        : berisi nilai unik film
  - kolom keywords  : berisi kata kunci dari setiap film
- links.csv /links_small.csv. berisi fitur id IMDB dan TMDB dari film, dan file kecil yang digunakan karena terbatasnya sumber daya.

  pada file links.csv /links_small.csv terdapat 4 kolom:
  - kolom movieId    : berisi nilai unik movieId
  - kolom imdbId     : berisi nilai unik film sesuai imdb
  - kolom tmdbId     : berisi nilai unik film 
- movies_metadata.csv. berisikan informasi film dari budget film, bahasa yang digunakan, deskripsi film dan lainnya

  pada file movies_metadata.csv terdiri dari 24 kolom
  - kolom adult                 : berisi nilai boolean true berarti film dengan kategori D
  - kolom belongs_to_collection : total pendapatan film
  - kolom budget                : total dana pembuatan film
  - kolom genres                : genre dari film
  - kolom homepage              : website film
  - kolom id                    : merupakan nilai unik film
  - kolom imdb_id               : merupakan nilai unik film sesuai imdb
  - kolom original_language     : bahasa pembuatan film
  - kolom originak_title        : judul asli film sebelum adaptasi
  - kolom overview              : deskripsi singkat film
  - kolom popularity            : total kepopuleran film dari data tmdb
  - kolom poster_path           : berisi gambar poster film
  - kolom production_companies  : berisi data rumah produksi
  - kolom production_countries  : berisi data negara rumah produksi
  - kolom release_date          : tahun rilis film
  - kolom revenue               : total pendapatan film
  - kolom runtume               : durasi film dalam menit
  - kolom spoken_language       : bahasa yang digunakan pada film
  - kolom status                : status film, rilis akandi rilis
  - kolom tagline               : tagline dari film
  - kolom title                 : judul film
  - kolom video                 : cuplikan film
  - kolom vote_average          : rata-rata voting film
  - kolom vote_count            : jumlah voting
    
- ratings.csv/ratings_small.csv. berisi informasi pengguna dan rating yang mereka berikan ke sebuah film. data kecil yang digunakan yaitu berisi 100 000 rating dari 700 pengguna terhadap 9000 film.
  ratings.csv/ratings_small.csv terdiri dari 4 kolom
  - kolom userId    : nilai unik pengguna
  - kolom movieId   : nilai unik film
  - kolom rating    : raing yang diberikan user (skala 0-5)
  - kolom timestamp : nilai timestamp

Data ini dipilih karena mencakup secara umum dan memiliki data pengguna yang beragam sehingga diharapkan analisis dan pembuatan sistem rekomandasi bisa digunakan secara umum juga.

Banyaknya kolom pada setiap data membuat dataset ini sangat besar dan membutuihkan komputasi yang besar juga, sehingga tidak semua kolom yang akan dijadikan fitur untuk membuat model dari sistem rekomendasi ini. Variabel-variabel yang digunakan adalah sebagai berikut:
- title : merupakan judul film.
- cast : nama pemeran utama dan pemeran support
- crew: nama sutradata, editor, komposer, penulis dl
- genres: genre dari film
- id: kode unik setiap film
- keywords: kata kunci yang berkaitan dengan film

## Data Preparation
- _Null handling_
  Terdapat 2 cara dalam mengatasi data kosong:
  - pertama dengan menghapus data tersebut. pada data movie kolom 'title' terdapat data kosong yang eror, maka dilakukan drop untuk menghindari masalah lainnya
  - kedua dengan cara mengganti _null_ dengan data kosong atau [], hal ini bertujuan agar data tersebut tidak sia-sia dan masih bisa dimanfaatkan.
- mengganti beberapa tipe data. untuk menggabungkan data diperlukan kolom yang memiliki nilai dan tipe data yang sama. misalkan untuk menggabungkan data 'movie' dengan data 'credit' diperlukan kolom id dengan tipe data yang sama. Kolom id dan tmdbId pada data merupakan float dab kolom id pada data credits bertipe integer, maka data float tersebuh diubah tipe datanya menjadi integer.
- menggabungkan data. data [The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) memiliki 6 file csv yang terpisah, kolom-kolom yang akan digunakan disatukan terlebih dahlu.
- _Preprocesimg_
  - ekstrak JSON. pada kolom 'cast', 'crew' dan 'genres' untuk mendapatkan variabel yang dibutuhkan.
    - pada kolom cast tedapat banyak aktor yang bekerja. untuk menghemat komputasi diambil 3 nama paling awal dan nama paling awal itu merupakan pemeran utama oleh sebeb itu akan diambil 3 nama. 
    - pada kolom crew hanya akan diambil nama sutradaranya. dikarenakan umumnya orang akan mengenal siapa sutradaranya
    - pada kolom genres akan diambil semua variabel yang ada.
  - membersihkan kolom 'keywords'. variable kolom tersebut juga berbetuk JSON, tetapi untuk prosesnya sangat berbeda seperti:
    - pertama dilakukan ekstraksi variabel
    - kemudian semua vaiabel yang berisi kata kunci disimpan pada sebuah objek untuk menghitung kata kunci yang sering muncul
    - menghapus kata kunci yang tidak berulang, itu berarti teg tersebut tidak terlalu diminati sehingga dilakukan eliminasi data
    - mengubah semua kata menjadi kata asal menggunakan [SnowballStemmer](https://www.nltk.org/_modules/nltk/stem/snowball.html).
## Modeling
terdapat 2 model yang digunakan pada sistem rekomendasi:
- Content Based Filtering.
  - cara kerja algoritma Content Based Filtering
    - membuat data fitur dan dibersihkan
    - kemudian melakukan perhitungan TF-IDF(Term Frequency Inverse Document Frequency of records) untuk mengukur seberapa sering kata muncul menghitung seberapa penting kata pada fitur
    - membuat perhitungan menggunakan cosine_similarity untuk menghitung kemiripan sebuah film
    - jika nama film dimasukkan maka sistem rekomendasi akan memilih film yang memiliki skor tinggi cosine_similarity dan menampilkannya
  - memiliki beberapa kelebihan dan kekurangan diantaranya 
    - kelebihan metode ini bisa memberikan rekomendasi yang lebih personal dan memiliki rekomendasi yang releven dengan pengguna
    - kekurangan metode ini yaitu konten yang menjadi kurang beragam dikarenakan rekomendasi ini berasal dari apa yang ditonton sebelumnya dan data akan terbatas dan sulit memberikan rekomendasi jika
      pengguna baru.
    - model tersebut dipilih karena tersedianya kolom atau konten yang cocok dan layak untuk dilakukan permodelan berdasarkan konten
    - parameter tuning yang diubah dari nilai default
      - ngram_range=(1, 2). bertujuan untuk mengambil kata tunggal dan pasangan kata
      - min_df=0. bertujuan agar semua data dimasukkan kedalam vektor.
      - stop_words='english'. untuk membuang kata yang tiak memiliki makna seperti (the, and, in, dll)
  - rekomendasi yang dihasilkan setelah memasukkan film 'Toy Story' sebagi film favorit
    - Luxo Jr.
    - Toy Story 2
    - Cars 2
    - Cars
    - A Bug's Life
    - Toy Story of Terror!
    - Toy Story 3
    - Hugo
    - The Lego Movie
    - Larry Crowne
  - peforma dari sistem rekomendasi tersebut bisa dilihat dari persamaan hasi film yang direkomendasikan. 8 dari 10 film memiliki tema yang sama yaitu sebuah benda atau hewan yang bisa berbicara dan
    berinteraksi seperti manusia. sehingga jika melihat dari komteks tersebut maka model ini memberikan peforma yang bangus.

- Collaborative Filtering.
  - algoritma Collaborative Filtering
    - menggunakan module RecommenderNet untuk membuat lapisan atau layer dengan mengimplementasikan jaringan saraf tiruan atau neural network
    - mengubah nilai userId dan id menjadi vaktor numerik menggunakan lapisan embedding
    - kemudian membuat fungsi call untuk menghitung prediksi peringkat rekomendasi dengan aktivasi sigmoid
  - memiliki beberapa kelebihan dan kekurangan diantaranya
    - kelebiham metode ini mudah memberikan rekomendasi pada pengguna baru dan tidak memerlukan detail film
    - kekurangan metode ini yaitu kurang efektif dalam menangani perubahan perefrensi dikarenana interaksi pengguna.
    - model ini dipilih karena pada dataset terdapat kolom-kolom yang sesuai dan cocok untuk membuat model pembelajaran mesin ini.
    - rekomendasi yang didapat dari salah satu pengguna.
 - menghasilkan prediksi seperti berikut


Showing recommendations for users: 175
=========================================
Movie with high ratings from user
-----------------------------------------
Terminator 3: Rise of the Machines
-----------------------------------------
Top 10 movie recommendation
-----------------------------------------
Nick of Time

L.A. Confidential

The Breakfast Club

Sister Act

Ghost Dog: The Way of the Samurai

Amélie

A Bridge Too Far

Hairspray

Michael Clayton

Southland Tales

## Evaluation
- Dalam pengukuran presisi dari rekomendasi Content Based Filtering digunakan rumus P = total rekomendasi relevan/total rekomendasi
- Dilihat dari data yang dimasukkan 'toy story' terdapat 10 rekomendasi dari sistem. 8 daru 10 rekomendasi film mempunyai kemiripan dimana sebuah benda atau hewan yang berbicara / memiliki perilaku
  seperti manusia. sehingga dapat ditarik kesimpulan bahwa presisi sistem rekomedasi berbasis Content Based Filtering memiliki presisi sebesar 80%
- parameter yang digunakan saat proses pelatihan model sistem rekomendasi Collaborative Filtering:
  - menggunakan batch_size 8. penggunaan batch size yang terhitung kecil dari total keseluruhan data dimaksudkan agar model bisa lebih baik dalam mempelajadi data latih
  - epoch 10. dengan besarnya data latih dan kecilnya batch siza maka jumlah epoch yang banyak menjadi tidak relevan lagi.
  - learning_rate 0.001 agar model bisa mempelajadi fitur data latih bukan meniru data latih
  - matriks evaluasi yang digunakan yaitu RMSE. RMSE bekrja dengan mengambil nilai rata-rata kuadrat hasil selisih prediksi dengan nilai sebenarnya.
  
  ![rmse](/img/rmse.png)
  
- bisa dilihat hasil latih dari model, skor RMSE yang didapat sebesar 0.1931 untuk latih dan 0.2051 untuk tes. sehingga bisa disimpulkan banwa model bekreja dengan baik dengan  nilai rata-rata kesalahan sebesar 0.2051.
- matriks RMSE mengukur sejauh mana perbedaan hasil prediksi dengan hasil sebenarnya.
- sehingga sistem rekomendasi dinilai sudah mampu memberikan rekomendasi yang baik dan sesuai dengan pereferensi pengguna

## Kesimpulan
- sistem rekomendasi film merupakan merupakan sistem yang bisa memberikan rekomendasi film kepada pengguna berdasarkan pereferensi pengguna.
- sisten rekomendasi film sama-sama memberikan keuntungan terhadap pengguna dan penyedia.
- sistem rekomendasi berdasarkan Content Based Filtering memiliki presisi sebesar 80%.
- sistem rekomendasi berdasarkan Collaborative Filtering memiliki skor RMSE sebesar 0.2051.
- kedua sistem rekomendasi tersebut bisa memberikan rekomendasi dengan baik sesuai pereferensi pengguna dan dinilai bisa meningkatkan _user expreience_ 
 
**---END---**
