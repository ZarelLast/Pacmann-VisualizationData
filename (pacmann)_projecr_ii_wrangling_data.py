# -*- coding: utf-8 -*-
"""(Pacmann) Projecr II - Wrangling Data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1da1UWF7mLCI4gvOCohzykjswP4pFBvOj

# Latar Belakang

Sebuah badan riset kerja membutuhkan data tentang  pekerjaan yang dibutuhkan oleh perusahaan dibidang data.Kemudian tim analis data melakukan penelitian menyeluruh terkait sejumlah variabel, termasuk struktur gaji, lingkungan kerja, skala perusahaan, jenis pekerjaan, tingkat pengalaman, lokasi tempat tinggal karyawan, dan kategori pekerjaan.

1.   Mengidentifikasi jenis pekerjaan yang paling diminati dalam industri data.
2.   Menganalisis tren struktur gaji dalam industri data berdasaskan standar kompensasi(median).
3.   Memperoleh pemahaman tentang tingkat pengalaman yang umumnya dibutuhkan dalam bidang yg paling diminati.
4.   Mengevaluasi lokasi tempat tinggal karyawan yang paling sesuai dengan kebutuhan operasional.
5.   Menganalisis tentang skala perusahaan berdasarkan kategori pekerjaan.

# Goal

Tujuan utamanya yaitu untuk memberikan rekomendasi kepada manajemen perusahaan dalam yang ingin merekrut ataupun membuat divisi yang berfokus pada data, dengan mempertimbangkan berbagai aspek pasar kerja dan kebutuhan organisasi.

# Dataset
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from google.colab import userdata
import os

os.environ["KAGGLE_KEY"] = userdata.get('KAGGLE_KEY')
os.environ["KAGGLE_USERNAME"] = userdata.get('KAGGLE_USERNAME')

!kaggle datasets download -d murilozangari/jobs-and-salaries-in-data-field-2024

! unzip "jobs-and-salaries-in-data-field-2024.zip"

filepath = "jobs_in_data_2024.csv"
df = pd.read_csv(filepath)
df

df.info()

"""## Sorting Data
<!-- by work_year & salary -->
"""

# by work_year & salary
df_sorted = df.sort_values(by=['work_year', 'salary']).reset_index(drop=True)
df_sorted.head(5)

"""## Filter Data"""

# tanpa salary & salary_currency
df_filtered = df_sorted.drop(['salary', 'salary_currency', 'company_location'], axis=1)
df_filtered.head(5)

"""## Handling Missing Value"""

# Cek missing value
df_filtered.isna().sum()

"""## Handling Duplicated"""

# Hitung jumlah duplikat
df_filtered.duplicated().sum()

df_filtered.duplicated().sum() / len(df_filtered) * 100

# Menampilkan contoh duplikat
df_filtered[df_filtered.duplicated(keep=False)]\
  .sort_values(by=['work_year', 'salary_in_usd'])\
  .head(6)

# Remove duplikat
df_no_duplicated = df_filtered.drop_duplicates(keep='first')\
                            .reset_index(drop=True)
df_no_duplicated.head(5)

df_no_duplicated.duplicated().sum()

df_no_duplicated.duplicated().sum() / len(df_no_duplicated) * 100

"""## Handling Inkonsisten

### Identifikasi Inkonsistensi
"""

df_no_duplicated.columns

df_no_duplicated['work_year'].unique()

df_no_duplicated['work_year'].dtype

df_no_duplicated['experience_level'].unique()

df_no_duplicated['employment_type'].unique()

df_no_duplicated['job_title'].sort_values().unique()

df_no_duplicated['salary_in_usd'].dtype

df_no_duplicated['employee_residence'].sort_values().unique()

df_no_duplicated['work_setting'].unique()

df_no_duplicated['company_size'].unique()

df_no_duplicated['job_category'].sort_values().unique()

"""### Handling inkonsisten"""

# df_no_duplicated['work_year'] = df_no_duplicated['work_year'].astype(str)

map_company = {
    'S': 'Small',
    'M': 'Medium',
    'L': 'Large'
}
df_no_duplicated['company_size'] = df_no_duplicated['company_size'].map(map_company)

"""## Handling Outlier

### Outlier Numerik
"""

df_no_duplicated.describe()

# Cek outlier salary_in_usd
sns.histplot(data=df_no_duplicated, x="salary_in_usd")

# Membuat boxplot salary_in_usd
sns.boxplot(data=df_no_duplicated, x='salary_in_usd')

def detect_outliers(data):
  outliers = []
  Q1 = data.quantile(0.25)
  Q3 = data.quantile(0.75)
  IQR = Q3 - Q1
  lower_bound = Q1 - (1.5 * IQR)
  upper_bound = Q3 + (1.5 * IQR)
  print("lower:",lower_bound, "upper:", upper_bound)
  for x in data:
    if (x<lower_bound or x>upper_bound):
      outliers.append(x)
  return outliers

# Deteksi outlier pada dataframe
outliers_df = detect_outliers(df_no_duplicated['salary_in_usd'])
sns.boxplot(data=outliers_df, orient='h')
plt.title('salary in usd')

df_no_duplicated[df_no_duplicated['salary_in_usd'] == df_no_duplicated['salary_in_usd'].min()]

df_no_duplicated[df_no_duplicated['salary_in_usd'] == df_no_duplicated['salary_in_usd'].max()]

"""### Outlier Kategorik"""

list_columns = df_no_duplicated.columns
list_columns_kategorical = list_columns.drop('salary_in_usd')
list_columns_kategorical

list_columns_kategorical[0]

fig, ax = plt.subplots(4, 2, figsize=(12,9))
counter = 0

for x in range(4):
  for y in range(2):
    sns.boxplot(data=df_no_duplicated[list_columns_kategorical[counter]].value_counts(), ax=ax[x, y], orient="h")
    counter+=1

# make sure layout is not overlapping
fig.tight_layout()
# show the graphs
fig.show()

for kolom in list_columns_kategorical:
  modus = df_no_duplicated[kolom].mode()[0]
  print(f'Modus {kolom}: {modus}')

"""## Save CSV"""

df_no_duplicated.to_csv('file.csv')

"""## Korelasi"""

# ordinal
map_company_size = {
    'Small': 1,
    'Medium': 2,
    'Large': 3
}

# ordinal
map_jobs_level = {
    'Entry-level': 1,
    'Mid-level': 2,
    'Senior': 3,
    'Executive': 4
}

# ordinal
map_emp_type = {
    'Contract': 1,
    'Freelance': 2,
    'Part-time': 3,
    'Full-time': 4
}

map_work_set = {
    'Hybrid': 1,
    'In-person': 2,
    'Remote': 3}

ordinal_list = [map_company_size, map_jobs_level, map_emp_type, map_work_set]
map_ordinal = ['company_size', 'experience_level', 'employment_type', 'work_setting']
# one hot encoding
# df_encoded = pd.get_dummies(df_no_duplicated, columns=['work_setting'])
import copy
df_encoded = copy.deepcopy(df_no_duplicated)

df_encoded['work_year'] = df_encoded['work_year'].astype(int)

for kolom, res in zip(map_ordinal, ordinal_list):
  df_encoded[kolom] = df_encoded[kolom].map(res)

df_encoded.head()

sns.heatmap(df_encoded.corr(method='spearman'), annot=True, cmap='coolwarm', fmt=".2f")