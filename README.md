# GamesRecommendationSystem
I created a Games Recommendation System which recommends games to people Based on Ratings, Genres, Production Studios and more.

After Seeing a lot of projects using the TMDB dataset, I decided to create a recommendation Engine for Games.

## Libraries Used
1.) Beautiful Soup
2.) Sci-kit Learn
3.) re
4.) Pandas
5.) Numpy
6.) Requests
7.) LXML

## Input
The input dataset was created using BS4 to scrape the Metacritic website. The dataset contained Columns for Name, Platform, Release Date, Metacritic ratings, User Score, Description, Genres, Age Ratings and Developer.

## Output
The Result was a recommendation function whereby after a Game Name is written in the input, the top 10 most similar games are giving out as an output list. This output was calculated by using the Game Dev, Genre and Description whereby the Game Dev and Genres where upscaled to have more weights in the prediction. Also, the output function was also made to choose the closest name to an input name in the case of a typo or incorrect Game Name input.

## Improvements
The data scraped was not used on multiple platforms because cross platform games where inputted various times for various platforms on the metacritic website, Some games lacked specific information like Developers and Age Ratings so they had to be filled in with the most generalized data. A better recommendation process involving the usage of more Game Data could have been used to improve recommendations.
