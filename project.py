import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = {'january':1,
         'february':2,
         'march':3,
         'april':4,
         'may':5,
         'june':6}
DAYS = {'monday':0,
        'tuesday':1,
        'wednesday':2,
        'thursday':3,
        'friday':4,
        'saturday':5,
        'sunday':6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (Chicago, New York city, Washington). HINT: Use a while loop to handle invalid inputs
    ValidInput = False
    while not ValidInput:
        city = input("Please select a city - Chicago, New York City or Washington: ").lower()
        if city in CITY_DATA.keys():
            ValidInput = True
        else:
            print('Invalid input. Please try again.')

    ValidInput2 = False
    ValidInput3 = False
    ValidInput4 = False
    while not ValidInput2:
        filteroption = input ("Would you like to filter by month or day of the week? Type month, day, both or none...").lower()
        if filteroption in ('none','both','month','day'):
            ValidInput2 = True
        else: 
            print('Invalid input. Please try again.')
    month = ''
    day = ''
    if (filteroption != 'none'):
        if ((filteroption == 'both') | (filteroption == 'month')):
            
            # Get user input for month (all, january, february, ... , june)
            while not ValidInput3:
                month = input ("Please select a month (only january to june data available): ").lower()    
                if month in MONTHS.keys():
                    ValidInput3 = True 
                else: 
                    print('Invalid input. Please try again.')
        if ((filteroption == 'both') | (filteroption == 'day')):
            while not ValidInput4:

                # Get user input for day of week (all, monday, tuesday, ... sunday)
                day = input("Please select a day:").lower()
                if day in DAYS.keys():
                    ValidInput4 = True
                else: 
                    print('Invalid input. Please try again.')
            
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
    df = pd.read_csv(CITY_DATA[city], parse_dates=['Start Time','End Time'])
        
    # Filter the DataFrame based on a specific month
    if ((month!='all') & (month!='')):
        filtered_df = df[(df['Start Time'].dt.month == MONTHS[month]) | (df['End Time'].dt.month == MONTHS[month])]
    else: 
        filtered_df = df

    # Filter DataFrame by day of the week
    if ((day!='all') & (day!='')):
        filtered_df2 = filtered_df[(filtered_df['Start Time'].dt.weekday == DAYS[day]) | (filtered_df['End Time'].dt.weekday == DAYS[day])]
    else: 
        filtered_df2 = filtered_df
    return filtered_df2

   
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Convert Start Time column to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day and hour from Start Time column
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # Display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month is:', list(MONTHS.keys())[list(MONTHS.values()).index(most_common_month)])

    # Display the most common day of week
    most_common_weekday = df['weekday'].mode()[0]
    print('The most common weekday is:', list(DAYS.keys())[list(DAYS.values()).index(most_common_weekday)])

    # Display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common hour is:', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40) 

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    df['Start Station'] = df['Start Station'].astype(str)
    df['End Station'] = df['End Station'].astype(str)

    # Display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts()
    print('The most common Start Station is:', most_common_start_station)

    # Display most commonly used end station
    most_common_end_station = df['End Station'].value_counts()
    print('The most common End Station is:', most_common_end_station)

    # Display most frequent combination of start station and end station trip
    start_end_station = df.groupby(['Start Station', 'End Station']).size().reset_index(name='count')
    most_frequent_combtrip = start_end_station.loc[start_end_station['count'].idxmax()]   
    print('The most frequent combination of Start Station and End Station trip is from',most_frequent_combtrip['Start Station'],' to ',most_frequent_combtrip['End Station'],' with ',most_frequent_combtrip['count'],' trips.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: ',total_travel_time, ' seconds')
  
    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average travel time: ',mean_travel_time, ' seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types

    df['User Type'] = df['User Type'].astype(str)
    print('Counts of user types: ', df.groupby(['User Type'])['User Type'].count())

    if city != 'washington':
        df['Gender'] = df['Gender'].astype(str)

        # Display counts of gender
        print('Counts of gender: ', df.groupby(['Gender'])['Gender'].count())
        df['Birth Year']=df['Birth Year'].fillna(0).astype(int)

        # Display earliest, most recent, and most common year of birth
        without_zeros= df.loc[df['Birth Year'] != 0]
        earliest_birth_year = without_zeros ['Birth Year'].min()
        print('Earliest birth year:', earliest_birth_year)
    
        most_recent_birth_year = df['Birth Year'].max()
        print('Most recent birth year:', most_recent_birth_year)

        most_common_birth_year = without_zeros ['Birth Year'].mode()[0]
        print('Most common birth year:', most_common_birth_year)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_data(df):
    """ Display statistics on the 5 rows of individual trip data only"""
    validInput = False
    printRows = False
    while not validInput == True:
        view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?").lower()
        start_loc = 0
        if view_data == 'yes':
            printRows= True
            validInput=True
        elif view_data == 'no':
            printRows= False
            validInput=True
        else:
            print('Invalid value. Please try again.')    
        
        view_display = 'initial'
        
        while (printRows):
            if (view_display in ('initial','yes')):
                print(df.iloc[start_loc:start_loc + 5])
            
            view_display = input("Do you wish to continue?: ").lower()
            if view_display == 'yes':
                start_loc += 5
            elif view_display == 'no':
                printRows= False
                print('-'*40)
            else:
                print('Invalid value. Please try again.')  



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        print(df)       
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        view_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        


if __name__ == "__main__":
	main()