import datetime as dt
import numpy as np
import pandas as pd


'''
The following section sets up four dictionaries
'''

#data_dict matches the city with its respective dataset
data_dict = {
'New York City': 'new_york_city.csv',
'Chicago': 'chicago.csv',
'Washington':'washington.csv'}
#city_dict matches input to a city while allowing for spelling errors and tyos
city_dict = {
'New York City':['new york city','newyork city','newyorkcity','nyc'],
'Chicago':['chicago','chigago','chicaco','chi'],
'Washington': ['washington', 'washingtin', 'washingten','wash','was']}
#month_dict matches input to a month while allowing for spelling errors and typos
month_dict = {
'January': ['jan', 'january'],
'February': ['feb','february','febuary'],
'March': ['mar','march'],
'April': ['apr','arpil','april'],
'May': ['may'],
'June': ['jun','june'],
'All':['all','al','alll','aall','aal']}
#day_dict matches input to a day while allowing for spelling errors and typos
day_dict = {
'Monday': ['mon', 'monday'],
'Tuesday': ['tue','tues','tuesday'],
'Wednesday': ['wed','wednesday', 'wensday'],
'Thursday': ['thu','thur','thurs','thursday','thirsty'],
'Friday': ['fri','firday','friday'],
'Saturday': ['sat','saturday','satirday'],
'Sunday': ['sun','sunday'],
'All': ['all','al','alll','aall','aal']}

### functions begin here ###

def getkeys(dict, item):
	'''
		Purpose:
			getkeys allows you to iterate through a dictionary and find
			a key associated with a value
		Args:
			None
		Returns:
	 		list of str (key) associated with a specific value
	'''
	listofkeys = list()
	for key, value in iter(dict.items()):
		if item in value:
			listofkeys.append(key)
	return listofkeys

def getvals(dict):
	'''
		Purpose:
			getvals creates a list of all the values in a dictionary
		Args:
			None
		Returns:
		 	list of all values in a dictionary
	'''
	listofvals = list()
	dict_vallength = len(dict.values())
	for sublist in range(dict_vallength):
		for value in list(dict.values())[sublist]:
			listofvals.append(value)
	return listofvals

def get_user_city():
    '''
        Purose:
            get_user_city seeks input from the user for the city they are interested in
        Args:
            None
        Returns:
            str (city) after matching input with values in city_dict
    '''
    print("Welcome, let\'s explore bikesharing data.")
    city = ''
    while city not in getvals(city_dict):
        city = input("Please type which of the following cities you want to look at:\nNew York City\nChicago\nWashington\n").lower()
        if city in getvals(city_dict):
            print("\nYou have chosen {} as your city.\n".format(list(getkeys(city_dict, city))[0]))
        else:
            print("\nI'm sorry, I do not recognise that city, please try again.\n")
            city = input("Please type which of the following cities you want to look at:\nNew York City\nChicago\nWashington\n").lower()
    city = list(getkeys(city_dict, city))[0]
    return city

def get_user_month():
	'''
		Purose:
			get_user_month seeks input from the user for the month they are interested in
		Args:
			None
		Returns:
			str (month) after matching input with values in month_dict
	'''
	month = ''
	while month not in getvals(month_dict):
		try:
			month = input("Which of the following months do you want to look at: January, February, March, \nApril, May, June, or All? \n").lower()
			if month in getvals(month_dict):
				monthval = list(getkeys(month_dict, month))[0]
				if monthval == 'All':
					print("\nYou have chosen to investigate all months\n")
				else:
					print("\nYou have chosen {} as your month.\n".format(monthval))
			else:
				print("\nI'm sorry, I do not recognise that month, please try again.\n")
		except ValueError:
			break
	month = monthval
	return month

def get_user_day():
	'''
		Purpose:
			get_user_day seeks input from the user for the day they are interested in
		Args:
			None
		Returns:
			str (day) after matching input with values in day_dict
	'''
	day = ''
	while day not in getvals(day_dict):
		try:
			day = input("Which of the following days do you want to look at: Monday, Tuesday, \nWednesday, Thursday, Friday, Saturday, Sunday, or All? \n").lower()
			if day in getvals(day_dict):
				dayval = list(getkeys(day_dict, day))[0]
				if dayval == 'All':
					print("\nYou have chosen to investigate all days\n")
				else:
					print("\nYou have chosen {} as your day.\n".format(dayval))
			else:
				print("\nI'm sorry, I do not recognise that day, please try again.\n")
		except ValueError:
			break
	day = dayval
	return day

def summary_of_inputs(city, month, day):
	'''
		Purpose:
			summary_of_inputs is a small function to just summarise the information a user wants
		Args:
			str (city)
			str (month)
			str (day)
		Returns:
			It prints a statement with city, month, and day information as defined by user input.
			It's not meant to be anything fancy, just a short reminder what the user's params are.
	'''
	print("\nYou have chosen to investigate the bikesharing data of:\n{} for the following month(s): {} on the following day(s): {}\n".format(city, month, day))

def get_data(city, month, day):
	'''
		Purpose:
			To create the Pandas dataframe which will be used in this project
		Args:
			str (city)
			str (month)
			str (day)
			As defined by the input functions
		Returns:
			A Pandas dataframe object
	'''
	#Read csv file
	bikeshare_dataframe = pd.read_csv(data_dict[city])

	#Convert 'Start Time' column to datetime and
	#ceate columns for month, day, and hour
	bikeshare_dataframe['Start Time'] = pd.to_datetime(bikeshare_dataframe['Start Time'])
	bikeshare_dataframe['month'] = bikeshare_dataframe['Start Time'].dt.month
	bikeshare_dataframe['day_of_week'] = bikeshare_dataframe['Start Time'].dt.weekday_name
	bikeshare_dataframe['hour'] = bikeshare_dataframe['Start Time'].dt.hour

	#Handle the case when user selects all months

	if month.lower() != 'all':
		months = dict(zip([list(month_dict.keys())[x] for x in range(len(month_dict)-1)], list(range(1,len(month_dict)))))
		month = months.get(month)
		bikeshare_dataframe = bikeshare_dataframe[bikeshare_dataframe['month'] == month]

	#Handle the case when user selects all days

	if day.lower() != 'all':
		bikeshare_dataframe = bikeshare_dataframe[bikeshare_dataframe['day_of_week'] == day.title()]
	return bikeshare_dataframe

def stats_trips(dataframe, city, month, day):
	'''
		Purpose:
			To calculate stats for trip duration
		Args:
			dataframe: Pandas dataframe object
			str (city)
			str (month)
			str (day)
		Returns:
			Prints output of stats
	'''
	print("Let's look at some of the trip stats.")
	#Calculate the various stats. Use divmod() to create list of hrs and mins
	median_trip_duration = dataframe['Trip Duration'].median()
	median_trip_hrs = divmod(median_trip_duration, 60)
	mean_travel_duration = int(dataframe['Trip Duration'].mean())
	mean_trav_dur_hrs = divmod(mean_travel_duration, 60)
	total_travel_duration = dataframe['Trip Duration'].sum()
	total_travel_hrs = divmod(total_travel_duration, 60)
	total_nr_trips = dataframe['Trip Duration'].count()
	longest_trip = dataframe['Trip Duration'].max()
	shortest_trip = dataframe['Trip Duration'].min()

	#Print statements to display stats
	print(
	f"It looks like if you were to start your journey in {city} on a {day} in the",\
	f"month of {month},\nyou might expect your average travel time to be at least",\
	f"{mean_trav_dur_hrs[0]} hours and {mean_trav_dur_hrs[1]} minutes.",\
	f"\nThe shortest trip was {shortest_trip} minutes while the longest",\
	f"trip took {longest_trip} minutes. \nInterestingly,",\
	f"the total number of trips in {city} for",\
	f"for your date range\nwas {total_nr_trips} for a total of {total_travel_hrs[0]}",\
	f"hours {total_travel_hrs[1]} minutes.\nThe median",\
	f"duration of a trip was {median_trip_hrs[0]} hours",\
	f"{median_trip_hrs[1]} minutes.",\
	"\nHere are the raw values if you\'re interested:\n")

	print("Median trip duration: {:.2f} minutes.".format(median_trip_duration))
	print("Mean traval duration: {:.2f} minutes.".format(mean_travel_duration))
	print("Longest trip duration: {:.2f} minutes.".format(longest_trip))
	print("Shortest trip duration: {:.2f} minutes.".format(shortest_trip))
	print("Total travel duration: {:.2f} minutes.".format(total_travel_duration))
	print("Total number of trips: {} trips.".format(total_nr_trips))
	print("*"*100)

def stats_users(dataframe, city, month, day):
	'''
		Purpose:
			Determine user types, genders, and ages
		Args:
			dataframe
			str (city)
			str (month)
			str (day)
		Returns:
			Prints stats relating to user type, gender, and age
	'''

	print("We\'ll now look at some more detailed user stats for {}.\n".format(city))
	#Count the number of different user types
	types = dataframe['User Type'].value_counts()
	#Test whether dataset has 'Gender' as a column
	gender_test = 'Gender' in dataframe
	#Test whether dataset has 'Birth Year' as a column
	birth_year_test = 'Birth Year' in dataframe
	gender = ''
	#If dataset contains Gender, determine number of M and F
	if gender_test == True:
		gender = dataframe['Gender'].value_counts()
		m_f_ratio = gender[0]/gender[1]
		print("The gender numbers is as follows:\n", gender.to_string())
		print(
		f"\nThere are {m_f_ratio:.2f} times as many men compared to women who",\
		f"used\nthe bikesharing program in {city} during the dates specified.\n")
	else:
		print("This dataset does not contain gender data for {}.\n".format(city))
	#If dataset contains Birth Year, determin oldest, youngest, and median
	if birth_year_test == True:
		current_year = dt.date.today().year
		min_year = int(dataframe['Birth Year'].min())
		max_year = int(dataframe['Birth Year'].max())
		mode_year = int(dataframe['Birth Year'].mode()[0])
		old_age = int(current_year-min_year)
		young_age = int(current_year-max_year)
		print(
		f"The oldest riders were born in {min_year} and are {old_age} years old.",\
		f"\nThe youngest riders were born in {max_year} and are {young_age} years old.",\
		f"\nThe most common birth year is {mode_year}.")
	else:
		print("This dataset does not contain age data for {}.".format(city))
	print("\nThese are the types of customers in {}:\n".format(city), types.to_string())
	print("*"*100)

def stats_station(dataframe, city, month, day):
	'''
		Purpose:
			Determine station usage stats
		Args:
			dataframe
			str (city)
			str (month)
			str (day)
		Returns:
			Prints station usage stats
	'''
	print("We\'ll now look at some more detailed station stats for {}.\n".format(city))

	#Determine most popular starting station
	most_pop_start = dataframe['Start Station'].mode()[0]
	print("The most popular starting station was:",most_pop_start)

	#Determine most popular destination station
	most_pop_end = dataframe['End Station'].mode()[0]
	print("The most popular ending station was:",most_pop_end)

	#Determine most popular start/destination station combination
	most_pop_combo = dataframe.groupby(['Start Station','End Station']).size(
	).sort_values(ascending=False).head(5).to_string()
	print("\nThe top 5 most popular starting and ending station combinations were:\n\n", most_pop_combo)
	print("*"*100)

def stats_dates(dataframe, city, month, day):
	'''
		Purpose:
			To determine date-based stats
		Args:
			dataframe
			str (city)
			str (month)
			str (day)
		Returns:
			Prints data-based stats for bikesharing data
	'''
	print("We\'ll now look at some more detailed monthly, daily, or hourly stats for {}.\n".format(city))
	#If user selected ALL months, this allows them to determine which month
	#was the most popular. Can't determine most popular month if only
	#using one month
	if month == 'All':
		pop_month_index = dataframe['month'].mode()[0]
		pop_month = list(month_dict)[pop_month_index - 1]
		print("The most popular month is: {}".format(pop_month))
	else:
		print("Insufficient date range to determine the most popular month. Try \'All\' next time.")
	#If user selected ALL days, this allows them to determine which day
	#was the most popular. Can't determine most popular day if only
	#using one day
	if day == 'All':
		pop_day = dataframe['day_of_week'].mode()[0]
		print("The most popular day is: {}".format(pop_day))
	else:
		print("Insufficient date range to determine the most popular day. Try \'All\' next time.")
	#Determine the most popular hour and present in 12hr format.
	pop_hr = dataframe['hour'].mode()[0]
	if pop_hr < 12:
		print("The most popular hour is: {}a.m.".format(pop_hr))
	else:
		print("The most popular hour is: {}p.m.".format(pop_hr - 12))
	print("*"*100)

def stats_missing_data(dataframe, city, month, day):
	'''
		Purpose:
			Computes the number of missing values
		Args:
			dataframe
			str (city)
			str (month)
			str (day)
		Returns:
			Prints how many missing values there are
	'''
	#Count total NAN vals
	missing_values = np.count_nonzero(dataframe.isnull())
	print("The number of missing values in the {} dataset : {}".format(city, missing_values))

    #Counts the number of missing values in the User Type column
	missing_user_data = np.count_nonzero(dataframe['User Type'].isnull())
	print("The number of missing User Type values is: {}\n".format(missing_user_data))

	#Tests whether Birth Year and Gender are columns in dataframe
	birth_year_test = 'Birth Year' in dataframe
	gender_test = 'Gender' in dataframe

	#Prints nr of missing birth year values
	if birth_year_test == True:
		missing_birth_data = np.count_nonzero(dataframe['Birth Year'].isnull())
		print("The number of missing Birth Year values is: {}".format(missing_birth_data))
	else:
		print("The dataset for {} does not contain birth year information:\nMissing values cannot be computed.".format(city))
		missing_birth_data = 0
	#Prints nr of missing gender values
	if gender_test == True:
		missing_gender_data = np.count_nonzero(dataframe['Gender'].isnull())
		print("The number of missing Gender values is: {}".format(missing_gender_data))
	else:
		missing_gender_data = 0
		print("The dataset for {} does not contain gender information:\nMissing values cannot be computed.".format(city))

	#Tells user if all missing vals are accounted for and how many are unknown.
	data_test = (missing_values - missing_user_data - missing_birth_data - missing_gender_data)
	if data_test == 0:
		print("\nAll missing data accounted for. Total unaccounted values: {}".format(data_test))
	else:
		print("\nSome missing data unaccounted for. Total unaccounted values: {}".format(data_test))
	print("*"*100)

def raw_data_display(dataframe):
	'''
		Purpose:
			Display 5 rows of raw data pending user input
		Args:
			dataframe
		Returns:
			Prints 5 rows of data pending user input
	'''
	#Get total nr of rows in dataframe
	nr_rows = dataframe.shape[0]
	#Initialise counter
	display = 0
	#Get user input and display rows of data, beginning with column names
	for rows in range(0, nr_rows, 5):
		user_input = input("Would you like to view the data? Yes or No?\n")
		if user_input.lower() != 'yes':
			break
		print(dataframe.head(display))
		display += 5

def main():

    while True:

        [city, month, day] = [get_user_city(), get_user_month(), get_user_day()]
        bikeshare_dataframe = get_data(city, month, day)
        summary_of_inputs(city, month, day)

        stats_trips(bikeshare_dataframe, city, month, day)
        stats_users(bikeshare_dataframe, city, month, day)
        stats_station(bikeshare_dataframe, city, month, day)
        stats_dates(bikeshare_dataframe, city, month, day)
        stats_missing_data(bikeshare_dataframe, city, month, day)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() == 'yes':
            main()
        else:
            print("Good bye.")
            break

if __name__ == "__main__":
    main()
