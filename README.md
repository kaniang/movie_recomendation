# Laporan Proyek Machine Learning - Muhammad Zaki

## _Project Overview_

Sistem rekomendasi film merupakan sistem yang membantu pengguna menemukan film berdasarkan minatnya. Tujuannya untuk mempermudah pemilihan film, menghemat waktu dan meningkatkan kepuasan pengguna. Hal ini menjadi penting karena pertumbuhan konten digital dan kebutuhan oleh penyedia layanan streaming untuk mempertahankan pelanggan. Sistem ini menggunakan analisis data dan pembelajaran mesin untuk memberikan rekomendasi yang tepat kepada pengguna.

## _Business Understanding_

Untuk pelaku bisnis platform _streaming_, upaya dalam meningkatkan kepuasan pengguna sangat penting. jika _user experience_ bagus maka pengguna akan loyal sehingga platform _streaming_ tersebut bisa memaksimalkan pendapatannya.

### _Problem Statements_
- metode apa saja yang digunakan untuk membuat sistem rekomendasi?
- bagaimana menentukan apakah sistem tersebut berjalan dengan baik?

### _Goals_

- membuat 2 model sistem rekomendasi berdasarkan konten film seperti nama sutradara, pemain dan genre fil, tersebut dan juga berdasarkan preferensi pengguna yang memberikan penilaian.
- menggunakan matriks evaluasi pada saat melatih model untuk melihat peforma model

    ### Solution statements
    - untuk sistem rekomendasi berdasarkan konten digunakan model _content based filtering_ dan untuk sisten rekomendasi berdasarkan preferensi user digunakan model _collaborative filtering_
    - matriks yang digunakan untuk melihat pefroma model yaitu RMSE atau root mean squared error

## _Data Understanding_
Data yang digunakan diambil dari kaggle [The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset). Dataset ini mengandung lebih dari 45000 film yang rilis sebelum juli 2017.

Variabel-variabel pada The Movies Dataset dataset adalah sebagai berikut:
- title : merupakan judul film.
- cast : nama pemeran utama dan pemeran support
- crew: nama direktor, editor, komposer, penulis dl
- genres: genre dari film
- id: kode unik setiap film
- keywords: kata kunci yang berkaitan dengan film

## Data Preparation
- _Null handling_
  Terdapat 2 cara dalam mengatasi data kosong:
  - pertama dengan menghapus data tersebut. pada data movie kolom 'title' terdapat data kosong yang eror, maka dilakukan drop untuk menghindari masalah lainnya
  - kedua dengan cara mengganti nilai kosong dengan data kosong atau []
- mengganti beberapa tipe data. untuk menggabungkan data diperlukan kolom yang memiliki nilai dan tipe data yang sama. misalkan untuk menggabungkan data 'movie' dengan data 'credit' diperlukan kolom id dengan tipe data yang sama. jika salah satu berbeda maka haus disamakan dengan fungsi (.astype).
- menggabungkan data. data [The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) memiliki 6 file csv yang terpisah, kolom-kolom yang akan digunakan disatukan terlebih dahlu.
- _Preprocesimg_
  - ekstrak JSON. pada kolom 'cast', 'crew' dan 'genres' untuk mendapatkan variabel yang dibutuhkan.
    - pada kolom cast tedapat banyak aktor yang bekerja, oleh sebeb itu akan diammbil 3 nama.
    - pada kolom crew hanya akan diambil nama sutradaranya.
    - pada kolom genres akan diambil semua variabel yang ada.
  - membersihkan kolom 'keywords'. variable kolom tersebut juga berbetuk JSON, tetapi untuk prosesnya sangat berbeda seperti:
    - pertama dilakukan ekstraksi variabel
    - kemudian semua vaiabel yang berisi kata kunci disimpan pada sebuah objek untuk menghitung kata kunci yang sering muncuk
    - menghapus kata kunci yang tidak berulang
    - mengubah semua kata menjadi kata asal menggunakan [SnowballStemmer](https://www.nltk.org/_modules/nltk/stem/snowball.html).
## Modeling
terdapat 2 model yang digunakan pada sistem rekomendasi:
- Content Based Filtering.
  - memiliki beberapa kelebihan dan kekurangan diantaranya
    - kelebihan metode ini bisa memberikan rekomendasi yang lebih personal dan memiliki rekomendasi yang releven dengan pengguna
    - kekurangan metode ini yaitu konten yang menjadi kurang beragam dikarenakan rekomendasi ini berasal dari apa yang ditonton sebelumnya dan data akan terbatas dan sulit memberikan rekomendasi jika pengguna baru.
  - rekomendasi yang dihasilkan setelah memasukkan film 'Toy Story'  ![cbf](/img/rcmd_cbf.jpg)
- Collaborative Filtering.
  - memiliki beberapa kelebihan dan kekurangan diantaranya
    - kelebiham metode ini mudah memberikan rekomendasi pada pengguna baru dan tidak memerlukan detail film
    - kekurangan metode ini yaitu kurang efektif dalam menangani perubahan perefrensi dikarenana interaksi pengguna.
    - rekomendasi yang didapat dari salah satu pengguna ![cf](/img/rcmd_cf.jpg)

## Evaluation
parameter yang digunakan saat proses pelatihan model sistem rekomendasi Collaborative Filtering:
- menggunakan batch_size 8 dan epoch 10 dan learning_rate 0.001 dengan tujuan model mempelajadi data latih bukan meniru data latih
- matriks evaluasi yang digunakan yaitu RMSE.
  
  ![rmse](/img/rmse.png)
  
  bisa dilihat hasil latih dari model, skor RMSE yang didapat sebesar 0.1931 untuk latih dan 0.2051 untuk tes.
- matriks RMSE mengukur sejauh mana perbedaan hasil prediksi dengan hasil sebenarnya, dengan cara menganmbil rata-rata hasil kuadrat selisih kesalahan prediksi terhadap nilai sebenarnya. oleh sebab itu nilai 0.2051 pada data tes merupakan hasil yang bagus.
- sehingga sistem rekomendasi dinilai sudah mampu memberikan rekomendasi yang baik dan sesuai dengan pereferensi pengguna


**---END---**
