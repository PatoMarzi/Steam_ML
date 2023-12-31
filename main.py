import pandas as pd
import uvicorn
from fastapi import FastAPI

app = FastAPI()

# The app.get decorator is used to associate the function with an HTTP GET request.
# '/PlayTimeGenre/{genre}/' is the path for the endpoint, the {genre} is the parameter.
@app.get('/PlayTimeGenre/{genre}/')
def PlayTimeGenre(genre: str):
    '''
    Find the genre with the most playtime hours.

    Parameters
    ----------
    genre : str
        Desired genre to look for.

    Returns
    -------
    int
        Year when the highest number of hours played was recorded for that genre.

    Examples
    -------
    >>> PlayTimeGenre('Action')
    2012
    >>> PlayTimeGenre('Indie')
    2006

    '''
    f1 = pd.read_parquet('./data/f1.parquet')
    f1['genres'] = f1['genres'].str.lower()
    # We look in our DataSet if there is any match with the genre entered.
    genres = f1[f1['genres'] == genre.lower()]
    if genres.empty:
        return f'The genre {genre} does not exist.'

    # We calculate the total playtime for each year in the dataset.
    results = genres.groupby('year')['playtime_forever'].sum()

    # Locate the index where the maximum value is. In this case the most played genre.
    idResut = results.idxmax()

    return f'Year with the most playtime hours for {genre}: {idResut}'

if __name__ == "__main__":
    uvicorn.run("main:app",port=10000,reload=True)

@app.get('/UserForGenre/{genre}/')
def UserForGenre(genre: str):
    '''
    Find the user with the most hours played by genre, as well as hours played for each year.

    Parameters
    ----------
    genre : str
        Desired genre to look for.

    Returns
    -------
    list
        The user name and the amount of hours played by year for that particular genre.

    Examples
    -------
    >>> UserForGenre('Simulation')
    UserName is the user with the most playtime for the genre "Action" with 23721 hours played.

    Year            2003    2006    2009    2010    2011    2012    2013    2014    2015    2016    
    Hours Played      0      0      2037    4102    1968     223     323    342     1224     112   
    '''

    f2 = pd.read_parquet('./data/f2.parquet')

    f2['genres'] = f2['genres'].str.lower()
    # Look in the DataSet if there is any match with the genre entered.
    genres = f2[f2['genres'] == genre.lower()]

    if genres.empty:
        return f'The genre {genre} does not exist.'

    # Locate the index for the player.
    player = genres.loc[genres['playtime_forever'].idxmax()]['user_id']

    # Filter the DataSet with only the player id
    filteredDFWithPlayerID = (genres[genres['user_id'] == player])

    # Create a new DF with just the year and playtime_forever columns
    hoursPlayedByYear = filteredDFWithPlayerID.groupby(
        'year')['playtime_forever'].sum()

    hoursList = [{'Year': year, 'hours': hours}
                 for year, hours in hoursPlayedByYear.items()]
    result = {f'{player} is the user with the most playtime for the genre {genre.capitalize()} Hours Played: {hoursList}'
              }
    return result

if __name__ == "__main__":
    uvicorn.run("main:app",port=10000,reload=True)

@app.get('/UsersRecommend/{year}/')
def UsersRecommend(year: int):
    '''
    Get the three most recommended games  

    Parameters
    ----------
    year : str
        Year in which the top three recommended games are.

    Returns
    -------
    list
        Name of the three recommended games.

    Examples
    -------
    >>> UsersRecommend(2018):
    Counter-Strike: Global Offense, Garry's Mode, Fall Guys
    >>> UsersRecommend(2021)
    Empire: Total War, Left 4 Dead 2, The Stanley Parable
    '''
    f3 = pd.read_parquet('./data/f3.parquet')
    # Create a DataSet with rows that match the year.
    givenYear = f3[f3['year'] == year]

    if givenYear.empty:
        return f'There are no records for the year {year}.'

    # Group the top three games
    topThree = (givenYear['title'].value_counts().head(3).reset_index()
                .rename(columns={'title': 'Game', 'count': 'Positive Reviews'}))

    return [{f'Top {i+1}: "{game}" with {reviews} positive reviews'} for i, (game, reviews) in topThree.iterrows()]

if __name__ == "__main__":
    uvicorn.run("main:app",port=10000,reload=True)


@app.get('/UsersNotRecommend/{year}/')
def UsersNotRecommend(year: int):
    '''
    Get the three least recommended games.

    Parameters
    ----------
    year : str
        Year in which the three least recommended games are.

    Returns
    -------
    list
        Name of the three recommended games.

    Examples
    -------
    >>> UsersNotRecommend(2008):
    Portal 2, Garry's Mode, Fall Guys
    >>> UsersNotRecommend(2011)
    Carmageddon Max Pack, Left 4 Dead 2, The Stanley Parable
    '''
    f4 = pd.read_parquet('./data/f4.parquet')
    givenYear = f4[f4['year'] == year]

    if givenYear.empty:
        return f'There are no records for the year {year}.'

    # Group the games that are from the desired year and had negative reviews.
    leastRecommendedGames = f4[(f4['year'] == year) & (
        f4['recommend'] == False)]

    # Create a list that has the 3 least recommended games for that year.
    leastThree = (
        leastRecommendedGames['title']
        .value_counts()
        .head(3)
        .reset_index()
        .rename(columns={'count': 'Negative Reviews', 'title': 'Game'})
    )

    leastThree = [{f'Top {i+1}: "{game}" with {reviews} negative reviews'}
                  for i, (game, reviews) in leastThree.iterrows()]

    return leastThree


if __name__ == "__main__":
    uvicorn.run("main:app",port=10000,reload=True)

@app.get('/sentiment_analysis/{year}/')
def sentiment_analysis(year: int):
    '''
    Get the category reviews from all users in a year.

    Parameters
    ----------
    year : str
        Desired year to see how the reviews were.

    Returns
    -------
    list
        Amount of all the different review categories for that year.

    Examples
    -------
    >>> sentiment_analysis(2018)
    {Negative = 101, Neutral = 142, Positive = 221}
    >>>sentiment_analysis(2019)
    {Negative = 140, Neutral = 47, Positive = 115}
    '''
    f5 = pd.read_parquet('./data/f5.parquet')
    givenYear = f5[f5['year'] == year]

    if givenYear.empty:
        return f'There are no records for the year {year}.'

    sentiment = f5.groupby(
        'year')['sentiment_analysis'].value_counts().unstack(fill_value=0)

    sentiment = sentiment.loc[year].to_dict()

    return {"Negative": sentiment.get(0, 0),
            "Neutral": sentiment.get(1, 0),
            "Positive": sentiment.get(2, 0)}


# Start the server

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000, reload=True, access_log=False)
