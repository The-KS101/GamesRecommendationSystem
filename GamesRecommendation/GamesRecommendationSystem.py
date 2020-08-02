# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 10:38:09 2020

@author: Josephine
"""

import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


dataset = pd.read_csv('MetaCritic_xboxone_Game_Rating.csv')
data = pd.read_csv('MetaCritic_ps4_Game_Rating.csv')


def weightedRating(a):
    meta = a['meta_scores'] / 10
    try:
        users = float(a['user_scores'])
    except ValueError:
        users = 5.0
    weighed = (meta + users)/2
    return weighed


def cleanGenre(a):
    genres = a['gameGenres']
    dump = re.sub(',', '', genres)
    return dump


def joinContent(a):
    genre = cleanGenre(a)
    comb = (genre + ' ' + a['gameDevs'] + ' ' + a['game_descriptions'] + ' '
            + a['gameDevs'] + ' ' + genre + ' ' + genre)
    return comb


def LCS(a, names):
    lcsVal = []
    for i in names:
        grid = np.zeros((len(i), len(a)))
        for j in range(len(i)):
            for k in range(len(a)):
                if i[j] == a[k]:
                    grid[j][k] = 1 + grid[j-1][k-1]
                else:
                    grid[j][k] = 0
        maxVal = 0
        for i in grid:
            if max(i) > maxVal:
                maxVal = max(i)
        lcsVal.append(maxVal)
    return lcsVal.index(max(lcsVal))


def getRecommend(title):
    names = [i.lower() for i in dataset['names']]
    try:
        idx = names.index(title.lower())
        print('Similar Games gotten for {}'.format(dataset['names'][idx]))
    except ValueError:
        idx = LCS(title.lower(), names)
        print('Given Name not found, displaying most similar name, {}'
              .format(dataset['names'][idx]))

    sims = cosine_sim[idx]
    mostSimIndex = np.argsort(sims)
    mostSim = mostSimIndex[:: -1][1:16]
    similarGames = []
    simSort = {}
    for i in mostSim:
        simSort.update({dataset['names'][i]: dataset['weighed_score'][i]})
    simSorted = sorted(simSort.items(), key=lambda x: x[1], reverse=True)
    for key in simSorted:
        similarGames.append(key[0])
    return similarGames


dataset['gameDevs'][dataset['gameDevs'].isnull()]
dataset['gameDevs'] = dataset['gameDevs'].replace(np.nan, '-', regex=True)
dataset['gameGenres'][dataset['gameGenres'].isnull()]
dataset['gameGenres'] = dataset['gameGenres'].replace(np.nan, '-', regex=True)
dataset['game_descriptions'] = (dataset['game_descriptions']
                                .replace(np.nan, '-', regex=True))

dataset['weighed_score'] = dataset.apply(weightedRating, axis=1)

dataFrame = dataset.apply(joinContent, axis=1)

cv = CountVectorizer(stop_words='english')
vec_matrix = cv.fit_transform(dataFrame)

cosine_sim = cosine_similarity(vec_matrix, vec_matrix)

simGames = getRecommend('Apex')
