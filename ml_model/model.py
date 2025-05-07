import pandas as pd
from velik.settings import BASE_DIR

df = pd.read_csv(BASE_DIR /'ml_model/df.csv', index_col=0)

df['bike_characteristics_string'] = df['bike_characteristics_string'].str.replace(' ', ',')
df['bike_characteristics_string'] = df['bike_characteristics_string'].str.replace(',,', ',')
df['bike_characteristics_string'] = df['bike_characteristics_string'].str.replace(':', '')
df['bike_characteristics_string'] = df['bike_characteristics_string'].str.replace('_', '')
df['bike_characteristics_string'] = df['bike_characteristics_string'].str.replace('(', '')
df['bike_characteristics_string'] = df['bike_characteristics_string'].str.replace(')', '')
df['bike_characteristics_string'] = df['bike_characteristics_string'].apply(lambda x: x.lower())

from sklearn.feature_extraction.text import CountVectorizer

# создание вектора слов (токенов)
cv = CountVectorizer()
vectors = cv.fit_transform(df['bike_characteristics_string']).toarray()

from nltk.stem.porter import PorterStemmer

# приведение слов к стему (корневому слову)
ps = PorterStemmer()

def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)


df['bike_characteristics_string'] = df['bike_characteristics_string'].apply(stem)

from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vectors)

# возвращает id великов
def recommend(bike_id):
    bike_index = df[df['bike_id'] == bike_id].index[0]
    distances = similarity[bike_index]
    # получаем рекомендации
    bike_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[:4]

    result = []
    for i in bike_list:
        result.append(int(df.iloc[i[0]]['bike_id']))
    # исключаем переданный велик
    result.remove(bike_id)
    
    return result[:3]