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


def createSleepDataframe(start_time, end_time):
    dateOfSleepList, awakeCountList, awakeDurationList, awakeningsCountList, efficiencyList = [], [], [], [], []
    startTimeList, endTimeList, timeInBedList, minutesAsleepList, minutesAwakeList = [], [], [], [], []
    minutesToFallAsleepList, restlessCountList, restlessDurationList = [], [], []
    df_sleep = pd.DataFrame({'dateOfSleep': pd.Series(dtype='datetime64[ns]'),
                            'awakeCount': pd.Series(dtype='int'),
                            'awakeDuration': pd.Series(dtype='int'),
                            'awakeningsCount': pd.Series(dtype='int'),
                            'efficiency': pd.Series(dtype='int'),
                            'startTime': pd.Series(dtype='datetime64[ns]'),
                            'endTime': pd.Series(dtype='datetime64[ns]'),
                            'timeInBed': pd.Series(dtype='int'),
                            'minutesAsleep': pd.Series(dtype='int'),
                            'minutesAwake': pd.Series(dtype='int'),
                            'minutesToFallAsleep': pd.Series(dtype='int'),
                            'restlessCount': pd.Series(dtype='int'),
                            'restlessDuration': pd.Series(dtype='int'),
                            })
    
    sleepData = auth2_client.time_series('sleep', base_date=start_time, end_date=end_time)

    for sleepNight in sleepData['sleep']:
        dateOfSleepList.append(datetime.datetime.strptime(sleepNight['dateOfSleep'], "%Y-%m-%d"))
        awakeCountList.append(sleepNight['awakeCount'])
        awakeDurationList.append(sleepNight['awakeDuration'])
        awakeningsCountList.append(sleepNight['awakeningsCount'])
        efficiencyList.append(sleepNight['efficiency'])
        startTimeList.append(datetime.datetime.strptime(sleepNight['startTime'][11:-4], "%H:%M:%S").time())
        endTimeList.append(datetime.datetime.strptime(sleepNight['endTime'][11:-4], "%H:%M:%S").time())
        timeInBedList.append(sleepNight['timeInBed'])
        minutesAsleepList.append(sleepNight['minutesAsleep'])
        minutesAwakeList.append(sleepNight['minutesAwake'])
        minutesToFallAsleepList.append(sleepNight['minutesToFallAsleep'])
        restlessCountList.append(sleepNight['restlessCount'])
        restlessDurationList.append(sleepNight['restlessDuration'])

    # Update dataframe
    df_sleep['dateOfSleep'] = dateOfSleepList
    df_sleep['awakeCount'] = awakeCountList
    df_sleep['awakeDuration'] = awakeDurationList
    df_sleep['awakeningsCount'] = awakeningsCountList
    df_sleep['efficiency'] = efficiencyList
    df_sleep['startTime'] = startTimeList
    df_sleep['endTime'] = endTimeList
    df_sleep['timeInBed'] = timeInBedList
    df_sleep['minutesAsleep'] = minutesAsleepList
    df_sleep['minutesAwake'] = minutesAwakeList
    df_sleep['minutesToFallAsleep'] = minutesToFallAsleepList
    df_sleep['restlessCount'] = restlessCountList
    df_sleep['restlessDuration'] = restlessDurationList

    # set index to date of sleep
    df_sleep = df_sleep.set_index('dateOfSleep')

    return df_sleep

def parse_date(date_str: str):
    dateList = []
    dateList = date_str.split('/')
    dateList = [int(el) for el in dateList]
    print("DateList =", dateList)
    return dateList


@click.command()
@click.argument('start_date', type=str, required=True, default='10/06/2023')
@click.argument('end_date', type=str, required=True, default='22/07/2023')

def main(start_date: str, end_date: str):
    # Connect to the API
    get_authorization()

    # Parse the date for right format
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    
    startTime = pd.datetime(year=start_date[2], month=start_date[1], day=start_date[0])
    endTime = pd.datetime(year=end_date[2], month=end_date[1], day=end_date[0])

    # Create dataframe
    dfSleep = createSleepDataframe(startTime, endTime)

    # save into CSV file
    if not os.path.exists("data"):
        os.mkdir("data")

    dfSleep.to_csv(f'./data/sleepData_FROM_{startTime}_TO_{endTime}.csv')


if __name__ == '__main__':
    main()
