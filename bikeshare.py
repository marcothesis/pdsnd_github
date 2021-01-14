#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import datetime
import pandas as pd
import numpy as np


# In[ ]:


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}


# In[ ]:


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    cities = ['chicago', 'new york city', 'washington']
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

    print('\nWelcome! Let\'s explore some bikeshare data in the United States!')

    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nWould you like to see data for Chicago, New York City or Washington?\n').lower()
        if city not in cities:
            print('\nIncorrect input. Please type in a city from the given options.\n')
            continue
        else:
            print('\nYou have chosen {}. If this is not the case, restart the program now!\n'.format(city.title()))
            break

    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        filter_input = input('Would you like to filter the data by month or day? Type "none" for no time filter.\n').lower()

        if filter_input == 'month':
            print('\nAlright. We will filter by month.\n')
            while True:
                month = input('Which month? January, February, March, April, May, June or all? Please type out the full month name.\n').lower()
                if month not in months:
                    print('Sorry, please enter an available month from the options or type "all".')
                    continue
                else:
                    print('\nOk, you have selected {}. Just a moment...\n'.format(month.title()))
                    day = 'all'
                    break
            break

        elif filter_input == 'day':
            print('\nAlright. We will filter by day.\n')
            while True:
                day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all? Please type out the full day name.\n').lower()
                if day not in days:
                    print('Sorry, please enter the correct day or type "all".')
                    continue
                else:
                    print('\nOk, you have selected {}. Just a moment...\n'.format(day.title()))
                    month = 'all'
                    break
            break

        elif filter_input == 'none':
            print('\nAlright. We will not filter the data.\n')
            month = 'all'
            day = 'all'
            break

        else:
            print('\nUnrecognized input. Please type "month", "day" or "none".\n')

    print('-'*40)
    return city, month, day


# In[ ]:


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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        dow_dict = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3, 'Friday':4, 'Saturday':5, 'Sunday':6}
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == dow_dict[day.title()]]

    return df


# In[ ]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating the Most Popular Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_names = ['January', 'February', 'March', 'April', 'May', 'June']
    top_month = df['month'].mode()[0]
    print('Most common month: {}'.format(month_names[top_month-1]))

    # display the most common day of week
    dow_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    top_dow = df['day_of_week'].mode()[0]
    print('Most common day: {}'.format(dow_names[top_dow]))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    top_hour = df['hour'].mode()[0]
    print('Most common hour: {} (24-hr)'.format(top_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[ ]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    top_start_station = df['Start Station'].mode()[0]
    print('Most commonly used Start Station: {}'.format(top_start_station))

    # display most commonly used end station
    top_end_station = df['End Station'].mode()[0]
    print('Most commonly used End station: {}'.format(top_end_station))

    # display most frequent combination of start station and end station trip
    df['Combined Stations'] = df['Start Station'] + ' and ' + df['End Station']
    top_combined_station = df['Combined Stations'].mode()[0]
    print('Most frequent combination of Start & End Station: {}'.format(top_combined_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[ ]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    def ydhms(seconds):
        min, sec = divmod(seconds, 60)
        hour, min = divmod(min, 60)
        day, hour = divmod(hour, 24)
        year, day = divmod(day, 365)
        return '{} years, {} days, {} hours, {} mins, {} secs'.format(year, day, hour, min, sec)

    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', ydhms(total_travel_time))

    # display mean travel time
    def readable_time(time):
        return str(datetime.timedelta(seconds = time))

    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time: {}'.format(readable_time(mean_travel_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[ ]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type = df['User Type'].value_counts()
    print('User Type:\n{}\n'.format(count_user_type))

    # Display counts of gender
    if 'Gender' in df.columns:
        count_gender = df['Gender'].value_counts()
        print('Gender:\n{}\n'.format(count_gender))
    else:
        print('There is no information on gender for this city.\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth = int(df['Birth Year'].min())
        print('Earliest year of birth: {}'.format(earliest_birth))

        most_recent_birth = int(df['Birth Year'].max())
        print('Most recent year of birth: {}'.format(most_recent_birth))

        most_common_birth = int(df['Birth Year'].mode()[0])
        print('Most common year of birth: {}'.format(most_common_birth))
    else:
        print('There is no information on year of birth for this city.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[ ]:


def display_raw_data(df):
    """Displays raw data based on user option."""
    
    see_more = input('\nDo you want to see some raw data? Enter yes or no.\n')
    show_rows = 0

    while True:
        if see_more.lower() == 'yes':
            print()
            print(df.iloc[show_rows:show_rows + 5])
            show_rows += 5
            see_more = input('\nDo you want to see more raw data? Enter yes or no.\n')
        elif see_more.lower() == 'no':
            break
        else:
            see_more = input('\nUnrecognized input. Please enter either yes or no.\n')


# In[ ]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


# In[ ]:


if __name__ == "__main__":
	main()
