import time
import pandas as pd
import numpy as np
import datetime
import calendar

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

CITIES = ['chicago', 'new york', 'washington']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', \
        'thursday', 'friday', 'saturday' ]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ('chicago', 'new york', 'washington')
    while True:
        city = input('Which city do you want to explore? Chicago, New York or Washington? \n>').lower()
        if city in cities:
            break
        
        print('That is not a valid answer. Please try again.')


    # get user input for month (all, january, february, ... , june)
    months = {v.lower(): k for k, v in enumerate(calendar.month_name)}
    while True:
        month = input('There is data available from january to june. Please enter the month you want to look at (e.g. all, january, february,..., june.) \n>')
        if month in list(months)[1:7] or month == 'all':
            break
        
        print('That is not a valid answer. Please try again.')  

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = {v.lower(): k for k, v in enumerate(calendar.day_name)}    
    while True:
        day = input('Do you also want to look at a specific day of the week? (e.g. all, monday, tuesday,..., sunday.) \n> ')
        if day in days or day == 'all':
            break
        
        print('That is not a valid answer. Please try again.') 


    print('-'*40)
    return city, month, day 


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        month =  MONTHS.index(month) + 1
        df = df[ df['month'] == month ]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[ df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating the most frequent times of travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('The month with the highest use is %s.' % calendar.month_name[most_common_month])

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print('The day with the highest use is %s.' % most_common_day_of_week)

    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print('The hour with the highest use is hour %s.' % most_common_start_hour)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating the most popular stations and trip...\n')
    start_time = time.time()

    # display most commonly used start station
    df['popular_start_station'] = df['Start Station']
    popular_start_station = df['popular_start_station'].mode()[0]
    print('Most users start their journey at %s.' % popular_start_station)

    # display most commonly used end station
    df['popular_end_station'] = df['End Station']
    popular_end_station = df['popular_end_station'].mode()[0]
    print('Most users end their journey at %s.' % popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_combination = df['Start Station' ] + ', ' + df['End Station'] 
    print('The most common journey is from %s to%s.' \
          % (popular_combination.mode()[0].split(',')[0],popular_combination.mode()[0].split(',')[1]))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating trip duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = datetime.timedelta(seconds=int(df['Trip Duration'].sum()))
    print('The total travel time is %s hours.' % total_travel)

    # display mean travel time
    mean_travel = datetime.timedelta(seconds=int(df['Trip Duration'].mean()))
    print('The mean travel time is %s hours.' % mean_travel)    

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating user stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User types:')
    subs = len(df.loc[df['User Type'] == "Subscriber"])
    custs = len(df.loc[df['User Type'] == "Customer"])
    deps = len(df.loc[df['User Type'] == "Dependent"])
    print('{} users were listed as subscriber, {} as customer and {} as dependent.\n'.format(subs, custs, deps))
    
    if 'Gender' in df.columns:
        user_stats_gender(df)

    if 'Birth Year' in df.columns:
        user_stats_birth(df)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

    # Display counts of gender
def user_stats_gender(df):
    """Displays statistics of analysis based on the gender of bikeshare users."""

    # Display counts of gender
    print('Gender of users:')
    male = len(df.loc[df['Gender'] == "Male"])
    female = len(df.loc[df['Gender'] == "Female"])
    print('{} of users were male and {} were female.\n'.format(male, female))


    # Display earliest, most recent, and most common year of birth
def user_stats_birth(df):
    """Displays statistics of analysis based on the birth years of bikeshare users."""
    
    print('Age of users:')
    # Display earliest, most recent, and most common year of birth
    birth_year = df['Birth Year']
    # the most common birth year
    most_common_year = int(birth_year.mode()[0])
    print('Most users were born in %s.' % most_common_year)
    # the most recent birth year
    most_recent = int(birth_year.max())
    print('The youngest user was born in %s.' % most_recent)
    # the most earliest birth year
    earliest_year = int(birth_year.min())
    print('The oldest user was born in %s.' % earliest_year)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
