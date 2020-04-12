import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

df = pd.read_csv('data\\anime_part.csv')

genre_dict = {}
for index, row in df.iterrows():
    for genre in row['genre'].split(','):
        if genre not in genre_dict:
            genre_dict[genre] = []
        genre_dict[genre].append(row['name'])

#print(genre_dict)

G=nx.Graph()

for genre, anime_name in genre_dict.items():
    G.add_node(genre, attr = genre)
    #G.add_nodes_from(anime_name, attr = anime_name)
    #for v in anime_name:
        #G.add_edge(genre, v)

plt.figure(figsize = (8, 8))
nx.draw(G, with_labels = True)
plt.savefig("test.png", dpi = 75)

G2 = nx.Graph()

for index, row in df.iterrows():
    anime_genre = row['genre'].split(',')
    i = 0
    for genre in anime_genre:
        G2.add_node(genre)
        if i > 0:
            G2.add_edge(genre, anime_genre[i-1])
            print(genre + " : " + anime_genre[i-1] + " : " + str(i))
        i+=1


plt.figure(figsize = (8, 8))
nx.draw(G2, with_labels = True)
plt.savefig("test2.png", dpi = 75)
