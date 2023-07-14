import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    valid = False
    while not valid:
        city = input('Please enter a city (chicago, new york city, or washington): ')
        if city == 'chicago' or city == 'new york' or city == 'washington':
            valid = True
        else:
            print('Whoops! Try again! \n')



    # TO DO: get user input for month (all, january, february, ... , june)

    valid = False

    while not valid:
        month = input('Please enter a month (all, january, february...june): ')
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            valid = True
        else:
            print('Whoops! Try again! \n')


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    valid = False

    while not valid:
        day = input('Please enter a day (all, monday, tuesday...sunday): ')
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            valid = True
        else:
            print('Whoops! Try again! Make sure to match case with the example...\n')


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
    if city == 'new york city':
        test = city.split(' ').join('_')
        df = pd.read_csv(test + '.csv')
    else:
        df = pd.read_csv(city + '.csv')

    #ADD USEFUL COLUMNS
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    #return immediately if no filters selected
    if month == 'all' and day == 'all':
        return df

    #MONTH FILTERING
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months.index(month) + 1
        df = df[df['month'] == month_index]

    #DAY FILTERING
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month_popular = months[df['month'].value_counts().idxmax() - 1].title()
    day_popular = df['day_of_week'].value_counts().idxmax().title()
    hour_popular = df['Start Time'].dt.hour.value_counts().idxmax()
    pm = False

    if hour_popular > 12:
        hour_popular -= 12
        pm = True

    #CASE 1: ALL MONTHS, SPECIFIC DAY
    if len(df['month'].unique()) > 1 and len(df['day_of_week'].unique()) == 1:

        print('• The most popular month for biking for our data filtered by day (' + day_popular + ') is ' + months[df['month'].value_counts().idxmax() - 1].title())
        print('----- There were ' + str(df['month'].value_counts().max()) + ' bikers during this month!\n')
        if pm:
            print('• The most common hour for biking during this time is ' + str(hour_popular) + ' PM!')
        else:
            print('• The most common hour for biking during this time is ' + str(hour_popular) + ' AM!')

    #CASE 2: SPECIFIC MONTH, ALL DAYS
    if len(df['month'].unique()) == 1 and len(df['day_of_week'].unique()) > 1:

        print('• The most popular day of the week for biking in ' + month_popular + ' is ' + day_popular)
        if pm:
            print('• The most common hour for biking during this time is ' + str(hour_popular) + ' PM!')
        else:
            print('• The most common hour for biking during this time is ' + str(hour_popular) + ' AM!')

    #CASE 3: SPECIFIC MONTH AND DAY
    if len(df['month'].unique()) == 1 and len(df['day_of_week'].unique()) == 1:

        if pm:
            print('• The most common hour for biking during ' + month_popular + ' on ' + day_popular + 's is ' + str(hour_popular) + ' PM!')
        else:
            print('• The most common hour for biking during ' + month_popular + ' on ' + day_popular + 's is ' + str(hour_popular) + ' AM!')


    #CASE 4: NO FILTERS 🤬
    if len(df['month'].unique()) > 1 and len(df['day_of_week'].unique()) > 1:
        print('• The most popular month for biking is ' + month_popular)
        print('• The most popular day of the week for biking is ' + day_popular)

        if pm:
            print('• The most common hour for biking is ' + str(hour_popular) + ' PM!')
        else:
            print('• The most common hour for biking is ' + str(hour_popular) + ' AM!')




    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #combine start and end stations
    df['Start End Combined'] = df['Start Station'] + ' => ' + df['End Station']
    trip_popular = df['Start End Combined'].value_counts().idxmax()

    # TO DO: display most commonly used start station
    start_popular = df['Start Station'].value_counts().idxmax()
    print("• The most popular station to start from is " + start_popular)
    # print(df['Start End Combined'].value_counts().idxmax())


    # TO DO: display most commonly used end station
    end_popular = df['End Station'].value_counts().idxmax()
    print("• The most popular station to start from is " + end_popular)

    # TO DO: display most frequent combination of start station and end station trip
    print("• The most popular total trip is to start at " + trip_popular.split(' => ')[0] + ' and to end at ' + trip_popular.split(' => ')[1])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['Total Travel Time'] = df['End Time'] - df['Start Time']
    print(df['Total Travel Time'].sum().total_seconds() * 3600 / 24 / 31)


    # TO DO: display mean travel time


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types


    # TO DO: Display counts of gender


    # TO DO: Display earliest, most recent, and most common year of birth


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        # city, month, day = get_filters()
        # df = load_data(city, month, day)
        df = load_data('chicago', 'all', 'all')

        # print(df.head(50))
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        # user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
