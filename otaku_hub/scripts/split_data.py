import pandas as pd

df = pd.read_csv('..\\data\\anime.csv', na_values={'episodes' : ['Unknown']})
values = {'rating': 0, 'genre': 'Others', 'episodes': 0}
df = df.fillna(value = values)


none_df = pd.DataFrame(columns=df.columns)
movie_df = pd.DataFrame(columns=df.columns)
music_df = pd.DataFrame(columns=df.columns)
ona_df = pd.DataFrame(columns=df.columns)
ova_df = pd.DataFrame(columns=df.columns)
spl_df = pd.DataFrame(columns=df.columns)
tv_df = pd.DataFrame(columns=df.columns)


movie_count = 0
music_count = 0
none_count = 0
ona_count = 0
ova_count = 0
spl_count = 0
tv_count = 0
for index, row in df.iterrows():
    if row['type'] == 'Movie':
        movie_df.loc[movie_count] = row
        movie_count+=1
    elif row['type'] == 'Music':
        music_df.loc[music_count] = row
        music_count+=1
    elif row['type'] == 'ONA':
        ona_df.loc[ona_count] = row
        ona_count+=1
    elif row['type'] == 'OVA':
        ova_df.loc[ova_count] = row
        ova_count+=1
    elif row['type'] == 'Special':
        spl_df.loc[spl_count] = row
        spl_count+=1
    elif row['type'] == 'TV':
        tv_df.loc[tv_count] = row
        tv_count+=1
    else:
        none_df.loc[none_count] = row
        none_count+=1

none_df.to_csv('../data/none_type_anime.csv', index=False)
music_df.to_csv('../data/music_type_anime.csv', index=False)
movie_df.to_csv('../data/movie_type_anime.csv', index=False)
ona_df.to_csv('../data/ona_type_anime.csv', index=False)
ova_df.to_csv('../data/ova_type_anime.csv', index=False)
spl_df.to_csv('../data/spl_type_anime.csv', index=False)
tv_df.to_csv('../data/tv_type_anime.csv', index=False)
