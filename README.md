# sqlalchemy-challenge
## Main Objective
This project focuses on the analysis of the Hawaii database which contains the temperature and precipitation information from 2010 to 2017.
The datasbase contains two tables: measurements and stations. The project is divided in 2 parts.
## Description
### First Part
A precipitation and a station analyses are included in the jupyter notebook, which include the following information:
- Precipitation Analysis
 - Most recent date in the data set.
 - Using this date, retrieve the last 12 months of precipitation data by querying the 12 preceding months of data.
 - Select only the date and prcp values.
 - Load the query results into a Pandas DataFrame and set the index to the date column.
 - Sort the DataFrame values by date.
 - Plot the results using the DataFrame plot method.
- Station Analysis
 - Calculate the total number of stations in the dataset.
 - Find the most active stations.
 - Retrieve the last 12 months of temperature observation data (TOBS) and plot the results.
### Second Part
This part consists on designing an API based on the previous queries. Here's the list of routes and their functions:
* `/`

  * Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation`

  * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

  * Return the JSON representation of your dictionary.

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * Query the dates and temperature observations of the most active station for the last year of data.

  * Return a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

