# Get-movies

The Get-movies is a console utility for print list of movies according to the specified filters 

## Requirements
python 

## Usage

The following filters are available:

**The number of top rated films for each genre. Optional**  
-N <int>

**Filter by genre. Can be plural. Optional**  
-genres <genre_1&genre_2>

**Filter for release years of movies. Yert to. Optional** (default 2030)  
-year_to <int>

**Filter for release years of movies. Yert from. Optional** (default 1895)  
-year_from <int>

**Filter by title or part of the title of the movie. Optional**  
-year_from <String>

**Example**
> 
> *Example 1*  
> get-movies.py -N 3 -genres "Comedy|Adventure"  -year_from 1995 -year_to 2015 -year_from Love
>
> *Example 2*  
> get-movies.py 
>
> *Example 3*  
> get-movies.py  genres "Comedy" -year_from 2010
>

## Recommendation
If you want to change the original files, place them in the Data-files folder and name them movies.csv and rating.csv.
Then recreate the database by running admin.py

## For help  
-help -h