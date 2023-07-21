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
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    valid = False
    while not valid:
        city = input('Please enter a city (chicago, new york city, or washington): ').lower()
        if city == 'chicago' or city == 'new york city' or city == 'washington':
            valid = True
        else:
            print('Whoops! Try again! (Make sure you the match case of the examples!)\n')



    # get user input for month (all, january, february, ... , june)

    valid = False

    while not valid:
        month = input('Please enter a month (all, january, february...june): ').lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            valid = True
        else:
            print('Whoops! Try again!\n')


    #   get user input for day of week (all, monday, tuesday, ... sunday)

    valid = False

    while not valid:
        day = input('Please enter a day (all, monday, tuesday...sunday): ').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            valid = True
        else:
            print('Whoops! Try again!\n')


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
        test = '_'.join(city.split(' '))
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

    #   display the most common month

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
            print('• The most common hour for biking is ' + str(hour_popular) + ' PM!\n')
        else:
            print('• The most common hour for biking is ' + str(hour_popular) + ' AM!\n')

    # ask the user if they want to display raw data using separate fx
    display_raw_data(df, ['Start Time', 'day_of_week', 'month'])




    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #combine start and end stations
    df['Start End Combined'] = df['Start Station'] + ' => ' + df['End Station']
    trip_popular = df['Start End Combined'].value_counts().idxmax()

    #   display most commonly used start station
    start_popular = df['Start Station'].value_counts().idxmax()
    print("• The most popular station to start from is " + start_popular)
    # print(df['Start End Combined'].value_counts().idxmax())


    #   display most commonly used end station
    end_popular = df['End Station'].value_counts().idxmax()
    print("• The most popular station to end at is " + end_popular)

    #   display most frequent combination of start station and end station trip
    print("• The most popular total trip is to start at " + trip_popular.split(' => ')[0] + ' and to end at ' + trip_popular.split(' => ')[1] + '\n')

    # ask the user if they want to display raw data using separate fx
    display_raw_data(df, ['Start Station', 'End Station', 'Start End Combined'])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #   display total travel time
    df['Total Travel Time'] = df['End Time'] - df['Start Time']

    print("• Wow! These bikers traveled a long time! " + str(int(df['Total Travel Time'].sum().total_seconds() // 3600)) + ' hours to be exact!')


    #   display mean travel time
    print("• The mean travel time was about " + str(round(df['Total Travel Time'].sum().total_seconds() // 3600 / len(df['Total Travel Time']) * 60, 2)) + ' minutes.\n')

    #ask the user if they want to display raw data using separate fx
    display_raw_data(df, ['Start Time', 'End Time', 'Total Travel Time'])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #   Display counts of user types
    print("• There are two types of users for our bikes (subscriber and customer). Here's the breakdown for your parameters: ")
    print("----- Subscriber: " + str(df['User Type'].value_counts()['Subscriber']))
    print("----- Customer: " + str(df['User Type'].value_counts()['Customer']))


    #   Display counts of gender

    if city != 'washington':

        print("• Out of the users that provided their gender, " + str(round(df['Gender'].value_counts()['Male'] / (df['Gender'].value_counts()['Male'] + df['Gender'].value_counts()['Female']) * 100, 2)) + '% were male and ' + str(round(100.0 - round(df['Gender'].value_counts()['Male'] / (df['Gender'].value_counts()['Male'] + df['Gender'].value_counts()['Female']) * 100, 2), 2)) + '% were female.')
        print("• " + str(df['Gender'].isna().sum()) + ' riders declined to provide their gender.\n')


        #   Display earliest, most recent, and most common year of birth

        early_year = int(df['Birth Year'].min())
        late_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])

        print("• The oldest user in this search is now " + str(2023 - early_year) + ' years old! (Born in ' + str(early_year) + ')')
        if 2023 - early_year > 100:
            print('----- Looks like we might have a jokester that put in a fake birth year! Unless it was a very fit ' + str(2023 - early_year) + ' year old!')
        print("• The youngest user in this search is now " + str(2023 - late_year) + ' years old! (Born in ' + str(late_year) + ')\n')
        print("• The most common birth year in this search is " + str(common_year))
    else:
        print("Unfortunately, we dont have user's gender data in Washington.\n")

    #conditional display of raw data due to the lack of gender and birth year columns in washington.csv
    if city != 'washington':
        display_raw_data(df, ['User Type', 'Birth Year', 'Gender'])
    else:
        display_raw_data(df, ['User Type'])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df, columns):
    """Prompts the user whether or not they would like to see the raw data (in 5 row groups). Customized by column arg for each statistic group."""

    res = input('Want to see the raw data? (y or n): ')
    i = 0

    while res != 'n':
        print(df[columns][i: i + 5])
        res = input('Want to see more data? (y or n): ')
        i += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        stats = input('Do you want to see descriptive stats for this search? (y or n): ').lower()
        if stats == 'y':
            print(df.describe())

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
