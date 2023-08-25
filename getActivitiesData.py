# Python script to retrieve all the data sleep

import fitbit
import pandas as pd
from fitbit import gather_keys_oauth2 as Oauth2
import datetime
import os
import click

def get_authorization():
    # You will need to put in your own CLIENT_ID and CLIENT_SECRET as the ones below are fake
    global auth2_client
    CLIENT_ID = *******
    CLIENT_SECRET = *******

    server=Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
    server.browser_authorize()
    ACCESS_TOKEN=str(server.fitbit.client.session.token['access_token'])
    REFRESH_TOKEN=str(server.fitbit.client.session.token['refresh_token'])
    auth2_client=fitbit.Fitbit(CLIENT_ID,CLIENT_SECRET,oauth2=True,access_token=ACCESS_TOKEN,refresh_token=REFRESH_TOKEN)


def createActivitiesDataFrame(startTime, endTime):
    allDates = pd.date_range(start=startTime, end=endTime)

    df_activities = pd.DataFrame({'Activity': pd.Series(dtype='str'),
                                'Calories': pd.Series(dtype='float'),
                                'Duration': pd.Series(dtype='int'),
                                'startDate': pd.Series(dtype='datetime64[s]'),
                                'startTime': pd.Series(dtype='str'),
                                })

    activityList, caloriesList, durationList, startDateList, startTimeList, activityIdList = [], [], [], [], [], []

    for oneDate in allDates:
        oneDate = oneDate.date().strftime("%Y-%m-%d")
        oneDate = datetime.datetime.strptime(oneDate, '%Y-%m-%d')

        activitiesData = auth2_client.activities(date=oneDate)
        
        for act in activitiesData['activities']:
            activityList.append(act['activityParentName'])
            caloriesList.append(act['calories'])
            durationList.append(act['duration'])
            startDateList.append(datetime.datetime.strptime(act['startDate'], "%Y-%m-%d"))
            startTimeList.append(datetime.datetime.strptime(act['startTime'], "%H:%M").time())

    df_activities['Activity'] = activityList
    df_activities['Calories'] = caloriesList
    df_activities['Duration'] = durationList
    df_activities['startDate'] = startDateList
    df_activities['startTime'] = startTimeList

    return df_activities

def parse_date(date_str: str):
    dateList = []
    dateList = date_str.split('/')
    dateList = [int(el) for el in dateList]
    
    return dateList


@click.command()
@click.argument('start_date', type=str, required=True, default='01/01/2023')
@click.argument('end_date', type=str, required=True, default='02/01/2023')

def main(start_date: str, end_date: str):
    # Connect to the API
    get_authorization()

    # Parse the date for the right format
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    
    # Cast to datetime object
    startTime = pd.datetime(year=start_date[2], month=start_date[1], day=start_date[0])
    endTime = pd.datetime(year=end_date[2], month=end_date[1], day=end_date[0])

    # Create the dataframe
    dfActivities = createActivitiesDataFrame(startTime, endTime)

    # save into CSV file
    if not os.path.exists("data"):
        os.mkdir("data")

    dfActivities.to_csv(f'./data/activitiesData_FROM_{startTime}_TO_{endTime}.csv')

if __name__ == '__main__':
    main()