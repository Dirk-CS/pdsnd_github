import time
import pandas as pd
import numpy as np
import datetime
pd.set_option("display.max_columns", 200)


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#name filter options
filter_options = {
    'city': ['chicago', 'new york city', 'washington'], 
    'month': ['all', 'january', 'february', 'march', 'april', 'may', 'june'],
    'day':  ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    #store choices in a list
    filters_chosen = []
    
    print('Hello! Let\'s explore some US bikeshare data!')  
    #loop through the filter options, get user input.
    print('\nPlease choose a city, a month and a day you want to analyze.')
    i = 0
    while i < len(filter_options):
        for key, filters in filter_options.items():
            print(f'Here are your choices for the {key}: ')
            for filter in filters:
                if filter == 'all':
                    print(f'\t- {filter.lower()}')
                else:
                    print(f'\t- {filter.title()}')
            while True:
                #prompt for input from user
                print(f'Which {key} do you want to analyze? ')
                filter = input()
                if filter.lower() in filter_options[key]:
                    filters_chosen.append(filter.lower())
                    if filter == 'all':
                        print(f'\nYou chose {filter}.\n')
                    else:
                        print(f'\nYou chose {filter.title()}.\n')
                    break
                else:
                    #stay in the loop to get valid input
                    print(f'\nPlease name one of the options given.')
            # go to next key        
            i += 1
            
    print('Thank you for making your choices.')
    #assign values from filters chosen
    city, month, day = filters_chosen
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
    df_city= pd.read_csv(CITY_DATA[city])
    #change dtype of Start and End Time to datetime objects
    df_city['Start Time'] = pd.to_datetime(df_city['Start Time'])
    df_city['End Time'] = pd.to_datetime(df_city['End Time'])
    #add filter columns
    df_city['Day of Week'] = df_city['Start Time'].dt.day_name()
    df_city['Month'] = df_city['Start Time'].dt.month_name()
    #build dataframe according to filters
    if month == 'all' and day == 'all':
        df = df_city
    elif month == 'all' and day != 'all':
        df = df_city.loc[df_city['Day of Week'] == day.title()]
    elif month != 'all' and day == 'all':
        df = df_city.loc[df_city['Month'] == month.title()]
    else:
        df = df_city.loc[(df_city['Month'] == month.title()) & (df_city['Day of Week'] == day.title())]
    return df

def display_raw_data(df):
    """Displays raw data for selected filters upon user request."""
    
    i = 0
    j = 5
    raw_data_prompt = "Do you want to see the raw data (yes/no)?"
    print(raw_data_prompt)
    while True:
        answer = input()
        if answer.lower() == 'no':
            break
        elif answer.lower() == 'yes':
            if i + j >= len(df):
                print('This is the last batch.') 
                print(df.iloc[i:len(df)+1])
                break
            else:
                print('Here is the data: \n', df.iloc[i:i+j])
            i += j
            print('\nDo you want to see 5 more rows?')
        else:
            print('\nPlease answer \'yes\' or \'no\'.') 

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # display the most common month (only possible if all months were chosen)
    if (df['Month'].nunique()) == 1:
        print('\n- Month: The month is fixed, please choose "all" in the next round to find the most common one.')
    elif df['Month'].nunique() > 1:
        popular_hour = df['Month'].mode()[0]
        print(f'\n- Month: The most popular month for your combination is {popular_hour.title()}.')
    # display the most common day of week
    if (df['Day of Week'].nunique()) == 1:
        print('\n- Day: The day is fixed, please choose "all" in the next round finde the most common one.')
    elif df['Day of Week'].nunique() > 1:
        popular_day = df['Day of Week'].mode()[0]
        print(f'\n- Day: The most popular day for your combindation is {popular_day.title()}.')  
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour

    popular_hour = (df['hour'].mode()[0])
    print(f'\n- Hour: The most popular hour for your combindation is from {popular_hour} to {popular_hour + 1} o\'clock.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # display most commonly used start station
    top_station_start = df['Start Station'].mode()[0]
    print('The top station for starting a trip: ', top_station_start, '.')
    
    # display most commonly used end station
    top_station_end = df['End Station'].mode()[0]
    print('Most commonly used for ending a trip: ', top_station_end, '.')    

    # display most frequent combination of start station and end station trip
    top = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending = False)
    start, end = top.index[0]
    print('The most popular combination: from', start, 'to', end, '.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total_travel = int(df['Trip Duration'].sum())
    travel_in_days = datetime.timedelta(seconds = total_travel)
    print('\nTotal travel time is: ', total_travel, 'seconds.')
    print('That is: ', travel_in_days, '(hours, minutes, seconds).')
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('On average, a trip took ', '%.2f' %mean_travel_time, 'seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # Check for null values and drop rows with null values
    if df['User Type'].isnull().any():
        usertype = df['User Type'].fillna('no Info')
    else:
        usertype = df['User Type']
    print('\nThese are the numbers for the user type: \n', usertype.value_counts())
    
    # Display counts of gender
    try:
        if df['Gender'].isnull().sum() != 0:
            gendertype = df['Gender'].fillna('no Info')
        else:
            gendertype = df['Gender']
        print('\nThe users according to gender: \n', gendertype.value_counts())
    except KeyError:
            print('\nNo data on gender available.')
            
    # Display earliest, most recent, and most common year of birth
    # Drop NaN values and convert values to int
    try:
        df_birth_years = df.dropna(subset=['Birth Year'])
        df_birth_years = df_birth_years.astype({'Birth Year':'int'})
        print('\n-Earliest birth year: ', df_birth_years['Birth Year'].min())
        print('-Most recent birth year : ', df_birth_years['Birth Year'].max())
        print('-Most common birth year: ', df_birth_years['Birth Year'].mode()[0])
    except KeyError:
        print('\nNo data on birth year available.')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()