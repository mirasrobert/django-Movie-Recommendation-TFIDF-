from django.http import Http404
from django.shortcuts import render
import pickle
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer  # pip install scikit-learn
from sklearn.metrics.pairwise import cosine_similarity

# Create your views here.


def index(request):
    if request.method == 'GET':
        # Load the data
        with open(r'D:\(E)\Programming Tuts\Projects Tutorials\Python\Django - Movie\dataset\movies.pkl', 'rb') as f:
            movies = pickle.load(f)

            # Create a dataframe
            df = pd.DataFrame(movies)
            movies_info = df[['title', 'overview']][:10].to_dict('records')
            return render(request, 'movies/index.html', {'movies_info': movies_info})


def recommend(request):
    # Load the data
    if request.method == 'POST':
        with open(r'D:\(E)\Programming Tuts\Projects Tutorials\Python\Django - Movie\dataset\similarity.pkl', 'rb') as s:
            similarity = pickle.load(s)

            movies_data = pd.read_csv(
                r'D:\(E)\Programming Tuts\Projects Tutorials\Python\Django - Movie\dataset\movies.csv')

            movie_name = request.POST['movie_name']

            list_of_all_titles = movies_data['title'].tolist()

            find_close_match = difflib.get_close_matches(
                movie_name, list_of_all_titles)

            close_match = find_close_match[0]

            index_of_the_movie = movies_data[movies_data.title ==
                                             close_match]['index'].values[0]

            similarity_score = list(enumerate(similarity[index_of_the_movie]))

            sorted_similar_movies = sorted(
                similarity_score, key=lambda x: x[1], reverse=True)

            number_of_suggested_movies = 30

            i = 1

            title_of_movies = []

            for movie in sorted_similar_movies:
                index = movie[0]
                title_from_index = movies_data[movies_data.index ==
                                               index]['title'].values[0]
                if (i < number_of_suggested_movies):
                    title_of_movies.append(title_from_index)
                    i += 1

            # Return the data to the template
            return render(request, 'movies/recommend.html', {'title_of_movies': title_of_movies})
