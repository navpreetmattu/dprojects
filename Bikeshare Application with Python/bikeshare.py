import pandas as pd
import time
import calendar
from datetime import datetime, timedelta

# Filenames (Files are in same folder as the python script)
chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'


def get_city():
    '''Asks the user for a city and returns the filename for that city's bike share data.

    Args:
        None.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''
    city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                 'Would you like to see data for Chicago, New York, or Washington?\n')
    city = city.lower()
    if city == 'chicago':
        return pd.read_csv(chicago)
    elif city == 'new york':
        return pd.read_csv(new_york_city)
    elif city == 'washington':
        return pd.read_csv(washington)
    else:
        print('Please choose a value from options')
        return get_city()


def get_time_period():
    '''Asks the user for a time period and returns the specified filter.

    Args:
        None.
    Returns:
        (str) Time period to filter data by.
    '''
    time_period = input('\nWould you like to filter the data by "month", "day", "both" or not at'
                        ' all? Type "none" for no time filter.\n')
    time_period = time_period.lower()
    if time_period == 'month' or time_period == 'day' or time_period == 'both' or time_period == 'none':
        return time_period
    else:
        print('Please choose a value from options')
        return get_time_period()


def get_month():
    '''Asks the user for a month and returns the specified month.

    Args:
        None.
    Returns:
        (str) Specified month value selected by user
    '''
    month_ = input(
        '\nWhich month? January, February, March, April, May, or June?\n')
    if month_.lower() in months_list:
        return month_.lower()
    else:
        print('Please choose a value from options')
        return get_month()


def get_day(month):
    '''Asks the user for a day and returns the specified day.

    Args:
        (str) Month
    Returns:
        (str) Specified day value selected by user
    '''
    year = 2017
    day = input('\nWhich day? Please type your response as an integer.\n')
    try:
        int_day = int(day)
        if int_day > 0 and int_day <= calendar.monthrange(year, month)[1]:
            return int_day
        else:
            print('Please choose a valid day value for the specified month')
            return get_day(month)
    except:
        print('Please enter an integer day value')
        return get_day(month)


def get_weekday():
    '''Asks the user for a weekday(Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday) 
        and returns the specified day.

    Args:
        None
    Returns:
        (str) Specified weekday value selected by user
    '''
    week_day = input(
        '\nWhich weekday? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday?\n')

    if week_day.lower() in day_list:
        return day_list.index(week_day)
    else:
        print('Please choose a valid weekday from the values specified above')
        return get_weekday()


def popular_month(city_file):
    '''Asks the user for a day and returns the specified day.

    Args:
        city_file
    Returns:
        (str) The most popular month for start time
    '''
    each_month_start_date_count = city_file['Start Time'].dt.month.value_counts(
    )
    return months_list[each_month_start_date_count.index[0]-1]


def popular_day(city_file):
    '''This method finds the most popular day of the week for start time

    Args:
        city_file
    Returns:
        (str) The most popular day of week for start time
    '''
    popular_start_day_count = city_file['Start Time'].dt.weekday.value_counts()
    popular_start_day = day_list[popular_start_day_count.index[0]]
    return popular_start_day


def popular_hour(city_file):
    '''This method finds the most popular hour of the day for the start time

    Args:
        city_file
    Returns:
        (str) The most popular hour of day for start time
    '''
    return city_file['Start Time'].dt.hour.value_counts().index[0]


def trip_duration(city_file):
    '''This method calculate the total trip duration and mean trip duration

    Args:
        city_file
    Returns:
        None
    '''
    total_trip_duration = datetime(
        1, 1, 1) + timedelta(seconds=int(city_file['Trip Duration'].sum()))
    mean_trip_duration = city_file['Trip Duration'].mean()

    print("Total trip duration is : %d years" %
          (total_trip_duration.year-1), end=',')
    print(" %d months" % (total_trip_duration.month-1), end=',')
    print(" %d days" % (total_trip_duration.day-1), end=',')
    print(" %d hours" % (total_trip_duration.hour), end=',')
    print(" %d minutes" % (total_trip_duration.minute), end=',')
    print(" %d seconds" % (total_trip_duration.second), end='\n\n')

    print("Mean trip duration is : %.4f seconds" %
          (mean_trip_duration))


def popular_stations(city_file):
    '''This method finds out the most popular start and end stations

    Args:
        city_file
    Returns:
        (tuple) The most popular start station and most popular end station
    '''
    frequent_start_station = city_file['Start Station'].value_counts(
    ).index[0]
    frequent_end_station = city_file['End Station'].value_counts().index[0]
    return frequent_start_station, frequent_end_station


def popular_trip(city_file):
    '''This method prints out the most popular trip for start and end station

    Args:
        city_file
    Returns:
        None
    '''
    trip = city_file.groupby(['Start Station', 'End Station'], as_index=False)[
        'Trip Duration'].count().nlargest(1, 'Trip Duration')
    print("The most popular trip is from '{}' to '{}'".format(
        trip.iloc[0, 0], trip.iloc[0, 1]))


def users(city_file):
    '''This method print out the counts of each user type

    Args:
        city_file
    Returns:
        None
    '''
    user_type_count_df = city_file['User Type'].value_counts()
    print('The counts of each user type are given below:')
    for index, row in user_type_count_df.iteritems():
        print('{} : {}'.format(index, row))


def gender(city_file):
    '''This method prints the total counts of different gender

    Args:
        city_file
    Returns:
        None
    '''
    if 'Gender' in city_file.columns:
        gender_count_df = city_file['Gender'].value_counts()
        print('The count of each gender is given below:')
        for index, row in gender_count_df.iteritems():
            print('{} : {}'.format(index, row))
    else:
        print('This file doesn\'t contains gender data')


def birth_years(city_file):
    '''This function prints the earliest (i.e. oldest user), most recent (i.e. youngest user),
    and most popular birth years.

    Args:
        city_file
    Returns:
        None
    '''
    if 'Birth Year' in city_file.columns:
        birth_year = city_file.sort_values('Birth Year', ascending=True)[
            'Birth Year'].dropna()
        oldest_year = birth_year.iloc[0]
        youngest_year = birth_year.iloc[-1]
        popular_birth_year = birth_year.value_counts().index[0]
        print("The most oldest birth year is %d, the most youngest birth year is %d and the popular birth year is %d" % (
            oldest_year, youngest_year, popular_birth_year))
    else:
        print('This file doesn\'t contains birth year data')


def display_data(city_file):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.

    Args:
        city_file
    Returns:
        None
    '''
    display = input('\nWould you like to view individual trip data?'
                    'Type \'yes\' or \'no\'.\n')
    if display.lower() == 'yes':
        index = 0
        while index+5 <= len(city_file):
            print(city_file[index: index+5])
            index += 5
            choice = input(
                '\nWould you like to see 5 more rows?\nType \'no\' to stop.\n')
            if choice.lower() == 'no':
                break


def statistics():
    '''Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.

    Args:
        None
    Returns:
        None
    '''
    # Filter by city (Chicago, New York, Washington)
    city_df = get_city()
    convert_datetime(city_df)

    # Filter by time period (month, day, none)
    time_period = get_time_period()

    #########################################################
    #                                                       #
    #   This logic will filter the data set on the basis    #
    #   of time period selected by the user i.e. 'month',   #
    #   'day' or 'both'. Filtering only required once now.  #
    #                                                       #
    #########################################################
    if time_period == 'month':
        m = get_month()
        selected_month = months_list.index(m) + 1
        city_df = city_df[city_df['Start Time'].dt.month == selected_month]
    elif time_period == 'day':
        week_day = get_weekday()
        city_df = city_df[city_df['Start Time'].dt.weekday == week_day]
    elif time_period == 'both':
        m = get_month()
        selected_month = months_list.index(m) + 1
        selected_day = get_day(selected_month)
        city_df = city_df[city_df['Start Time'].dt.month == selected_month]
        city_df = city_df[city_df['Start Time'].dt.day == selected_day]

    print('Calculating the first statistic...')

    # What is the most popular month for start time?
    if time_period == 'none':
        start_time = time.time()

        print("The most popular month for start time is {}.".format(
            popular_month(city_df)).title())
        print("That took %s seconds." % (time.time() - start_time))
        print("Calculating the next statistic...")

    # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
    if time_period == 'none' or time_period == 'month':
        start_time = time.time()

        print("The most popular day for start time is {}.".format(
            popular_day(city_df)).title())
        print("That took %s seconds." % (time.time() - start_time))
        print("Calculating the next statistic...")

    start_time = time.time()

    # What is the most popular hour of day for start time?
    print("The popular hour of the day for start time is {}th hour.".format(
        popular_hour(city_df)))
    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the total trip duration and average trip duration?
    trip_duration(city_df)
    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the most popular start station and most popular end station?
    freq_start_station, freq_end_station = popular_stations(
        city_df)
    print("The most popular start station is {} and the most popular end station is {}.".format(
        freq_start_station, freq_end_station))
    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the most popular trip?
    popular_trip(city_df)
    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What are the counts of each user type?
    users(city_df)
    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What are the counts of gender?
    gender(city_df)
    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What are the earliest (i.e. oldest user), most recent (i.e. youngest user), and
    # most popular birth years?
    birth_years(city_df)
    print("That took %s seconds." % (time.time() - start_time))

    # Display five lines of data at a time if user specifies that they would like to
    display_data(city_df)

    # Restart?
    restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
    if restart.lower() == 'yes':
        statistics()


def convert_datetime(city_file):
    ''' This method will convert the Start Time and End Time columns from string to datetime

    Args:
        city_file
    Return:
        None
    '''
    city_file['Start Time'] = pd.to_datetime(city_file['Start Time'])
    city_file['End Time'] = pd.to_datetime(city_file['End Time'])


if __name__ == "__main__":

    day_list = ['monday', 'tuesday', 'wednesday',
                'thursday', 'friday', 'saturday', 'sunday']
    months_list = ['january', 'february', 'march', 'april', 'may', 'june']
    statistics()
