import datetime
import numpy as np
import pandas as pd
import calendar


def retrieve_city():
    '''Asks the user for the name of a city and returns the filename for the corresponding city\'s data.
    Arguments: NA
    Returns:
        File name for a city\'s data in string format.
    '''
    city = input('\nHello! I am Awesome-O 2000! Let\'s explore some US bikeshare data!\n'
                 'There is data available for Chicago, New York City, or Washington DC?\n').title()
    if city == 'Chicago' or city == 'chicago':
        return 'chicago.csv'
    elif city == 'New York' or city == "new york" or city == 'New York City' or city == 'new york city':
        return 'new_york_city.csv'
    elif city == 'Washington' or city == 'washington':
        return 'washington.csv'
    else:
        print("\nOops! You entered an invalid city! Please try again.")
        return retrieve_city()


def retrieve_time():
    '''Asks user to choose if they want month, day or none and returns the filter.
    Arguments: NA
    Returns:
        Two things as strings:
        1: the kind of period (e.g. month, day or none)
        2: the specified kind of period if given (e.g., Saturday, January)
    '''
    time = input('\nWould you like to retrieve data by month, day or no preference (type none)?.\n').lower()
    if time == 'month' or time == 'Month':
        return ['month', retrieve_month()]
    elif time == 'day' or time == 'Day':
        return ['day', retrieve_day()]
    elif time == 'none' or time == 'None':
        return ['none', 'no filter']
    else:
        print("\nIt is unclear what you mean. Please try again.")
        return retrieve_time()


def retrieve_month():
    '''Requests a month from the user and returns it.
    Arguments: NA
    Returns:
        Month as a number, e.g. for March it returns '03'; represented in string format
    '''
    month = input('\nWould you like data for January, February, March, April, May, or June?\n').title()
    if month == 'January':
        return '01'
    elif month == 'February':
        return '02'
    elif month == 'March':
        return '03'
    elif month == 'April':
        return '04'
    elif month == 'May':
        return '05'
    elif month == 'June':
        return '06'
    else:
        print("\nIt is not clear what you mean. Please try again.")
        return retrieve_month()

def retrieve_day():
    '''Requests a day from the user and returns the data for user inputs.
    Arguments: NA
    Returns:
        Day of the week represented as an integer; for example for Thursday it returns 4
    '''
    day_of_week = input('\nWould you like data for Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').title()
    if day_of_week == 'Monday':
        return 1
    elif day_of_week == 'Tuesday':
        return 2
    elif day_of_week == 'Wednesday':
        return 3
    elif day_of_week == 'Thursday':
        return 4
    elif day_of_week == 'Friday':
        return 5
    elif day_of_week == 'Saturday':
        return 6
    elif day_of_week == 'Sunday':
        return 7
    else:
        print("\nIt is not clear what you mean. Please try again.")
        return retrieve_day()

def month_most(df):
    '''Returns the most common month - that is, the month with the most trips.
    Arguments:
        df: dataframe of city\'s data
    Returns:
        Most common month in string format
    '''
    #Determines how many rows with a given month.
    monthly = df.groupby('Month')['Start Time'].count()
    return "Most popular start time by month: " + calendar.month_name[int(monthly.sort_values(ascending=False).index[0])]


def day_most(df):
    '''Returns the most common day - that is, the name of the day of the week with the most trips.
    Arguments:
        df: dataframe of city\'s data
    Returns:
        Most common name of day of the week in string format
    '''
    daily = df.groupby('Day of Week')['Start Time'].count()
    return "Most popular start time by day of week: " + calendar.day_name[int(daily.sort_values(ascending=False).index[0])]


def hour_most(df):
    '''Returns the most common hour of day - that is, the hour of day with the most trips.
    Arguments:
        df: dataframe of city\'s data
    Returns:
        Most common hour of the day in string format
    '''
    hourly = df.groupby('Hour of Day')['Start Time'].count()
    #Sort the results highest to lowest and then return the hour of the day that was highest (first in sorted list)
    most_hour = hourly.sort_values(ascending=False).index[0]
    h = datetime.datetime.strptime(most_hour, "%H")
    return "Most popular start time by hour of day: " + h.strftime("%I %p")

def duration(df):
    '''Returns average trip duration and total trip duration
    Arguments:
        df: dataframe of city\'s data
    Returns:
        Two things represented as strings: 1) Total trip duration in years, days, hours, minutes, and seconds; 2) Average trip duration in hours, minutes, and seconds
    '''
    total_duration = df['Trip Duration'].sum()
    average_duration = df['Trip Duration'].mean()
    m, s = divmod(total_duration, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    y, d = divmod(d, 365)
    total_duration = "\nTotal trip duration: %d years %02d days %02d hrs %02d min %02d sec" % (y, d, h, m, s)
    m, s = divmod(average_duration, 60)
    h, m = divmod(m, 60)
    average_duration = "Average trip duration: %d hrs %02d min %02d sec" % (h, m, s)
    return [total_duration, average_duration]

def station_pop(df):
    '''Returns the most popular start/stop stations
    Arguments:
        df: dataframe of city\'s data
    Returns:
        List with 2 values: 1) most popular start station, 2) most popular stop station
    '''
    start_counts = df.groupby('Start Station')['Start Station'].count()
    stop_counts = df.groupby('End Station')['End Station'].count()
    start_sort = start_counts.sort_values(ascending=False)
    stop_sort = stop_counts.sort_values(ascending=False)
    total_count = df['Start Station'].count()
    station_pop_start = "\nMost popular start station: " + start_sort.index[0] + " (" + str(start_sort[0]) + " trips, " + '{0:.2f}%'.format(((start_sort[0]/total_count) * 100)) + " of trips)"
    station_pop_stop = "Most popular end station: " + stop_sort.index[0] + " (" + str(stop_sort[0]) + " trips, " + '{0:.2f}%'.format(((stop_sort[0]/total_count) * 100)) + " of trips)"
    return [station_pop_start, station_pop_stop]


def trip_most(df):
    '''Returns the most popular trip route (start & stop station)
    Arguments
        df: dataframe of city\'s data
    Returns:
        Most popular combination of start and stop stations as a string
    '''
    trips = df.groupby(['Start Station', 'End Station'])['Start Time'].count()
    station_sorted = trips.sort_values(ascending=False)
    trips_total = df['Start Station'].count()
    return "Most common trip start and stop: " + "\n  Start station: " + str(station_sorted.index[0][0]) + "\n  Stop station: " + str(station_sorted.index[0][1]) + "\n  (" + str(station_sorted[0]) +  " trips, " + '{0:.2f}%'.format(((station_sorted[0]/trips_total) * 100)) + " of trips)"


def user_data(df):
    '''Returns the number of trips by user kind
    Arguments:
        df: dataframe of city\'s data
    Returns:
        A pandas series where index is the user type and value is the number of trips made by that user type
    '''
    user_type = df.groupby('User Type')['User Type'].count()
    return user_type


def user_gender(df):
    '''Returns the number of trips taken by each gender of user
    Arguments:
        df: dataframe of city\'s data
    Returns:
        A pandas series where index is the gender of the user and value is the number of trips made by that user type
    '''
    gender_count = df.groupby('Gender')['Gender'].count()
    return gender_count


def yearofbirth(df):
    '''Returns the earliest birth year, the most recent birth year, and the most common birth year
    Arguments:
        df: dataframe of city\'s data
    Returns:
        List of three values: 1) earliest birth year as a string, 2) most recent birth year as a string, 3) most common birth year as a string
    '''
    earliest_yearofbirth = "Earliest year of birth: " + str(int(df['Birth Year'].min()))
    mostrecent_yearofbirth = "Most recent year of birth: " + str(int(df['Birth Year'].max()))
    yearofbirth_count = df.groupby('Birth Year')['Birth Year'].count()
    yearofbirth_sort = yearofbirth_count.sort_values(ascending=False)
    trips_total = df['Birth Year'].count()
    common_yearofbirth = "Most common year of birth: " + str(int(yearofbirth_sort.index[0])) + " (" + str(yearofbirth_sort.iloc[0]) + " trips, " + '{0:.2f}%'.format(((yearofbirth_sort.iloc[0]/trips_total) * 100)) + " of trips)"
    return [earliest_yearofbirth, mostrecent_yearofbirth, common_yearofbirth]


def raw_data(df, line):
    '''Gives user five lines of raw data if they answer yes; will keep going by five lines if user answers yes.
    Arguments
        df: dataframe of city\'s data
    Returns:
        Returns the next five lines of raw data if the user says yes, then asks again and calls this function again
    '''
    answer = input('\nWould you like to view raw data?'
                    ' Type \'yes\' or \'no\'.\n')
    answer = answer.lower()
    if answer == 'yes':
        print(df.iloc[line:line+5])
        line += 5
        return raw_data(df, line)
    if answer == 'no':
        return
    else:
        print("\nI didn't understand that answer. Please try again.")
        return raw_data(df, line)


def statistics():
    '''Returns descriptive statistics about a city and filter period given by user
    Arguments: NA
    Returns: NA
    '''
    city = retrieve_city()
    city_df = pd.read_csv(city)

    def retrieve_day(str_date):
        '''Takes a date in the format yyyy-mm-dd and returns an integer
            represention of the day of the week, e.g. for Monday it returns 0
        Args:
            str_date: date in the format yyyy-mm-dd
        Returns:
            (int) Integer represention of the day of the week,
                e.g. for Monday it returns 0
        '''
    #parse string in format yyyy-mm-dd and create date object based on those values.
        date_obj = datetime.date(int(str_date[0:4]), int(str_date[5:7]), int(str_date[8:10]))
        return date_obj.weekday() #return the day of the week that that date was
    city_df['Day of Week'] = city_df['Start Time'].apply(retrieve_day)
    city_df['Month'] = city_df['Start Time'].str[5:7]
    city_df['Hour of Day'] = city_df['Start Time'].str[11:13]

    time_period = retrieve_time()
    filtered_time = time_period[0]
    filtered_time_value = time_period[1]
    filtered_time_name = 'No filter'

    if filtered_time == 'none':
        filtered_df = city_df
    elif filtered_time == 'month':
        filtered_df = city_df.loc[city_df['Month'] == filtered_time_value]
        filtered_time_name = calendar.month_name[int(filtered_time_value)]
    elif filtered_time == 'day':
        filtered_df = city_df.loc[city_df['Day of Week'] == filtered_time_value]
        filtered_time_name = calendar.day_name[int(filtered_time_value)]

    print('\n')
    print(city[:-4].upper().replace("_", " ") + ' -- ' + filtered_time_name.upper())

    print('Total trips: ' + "{:,}".format(filtered_df['Start Time'].count()))

    if filtered_time == 'none' or filtered_time == 'day':
        print(month_most(filtered_df))

    if filtered_time == 'none' or filtered_time == 'month':
        print(day_most(filtered_df))

    print(hour_most(filtered_df))

    stats_dur = duration(filtered_df)
    print(stats_dur[0])
    print(stats_dur[1])

    station_most = station_pop(filtered_df)
    print(station_most[0])
    print(station_most[1])

    # What is the most popular trip?
    print(trip_most(filtered_df))

    # What are the counts of each user type?
    print('')
    print(user_data(filtered_df))

    if city == 'chicago.csv' or city == 'new_york_city.csv':
        print('')
        print(user_gender(filtered_df))
        yearofbirth_data = yearofbirth(filtered_df)
        print('')
        print(yearofbirth_data[0])
        print(yearofbirth_data[1])
        print(yearofbirth_data[2])

    raw_data(filtered_df, 0)

    def rerun_ask():
        '''If the user says yes, the program restarts; if the user says no, the program exits.
        Arguments: NA
        Returns: NA
        '''
        rerun = input('\nDo you want to restart the program? Type \'yes\' or \'no\'.\n')
        if rerun.lower() == 'yes':
            statistics()
        elif rerun.lower() == 'no':
            return
        else:
            print("\nInput is invalid. Please try again!")
            return rerun_ask()

    rerun_ask()


if __name__ == "__main__":
    statistics()
