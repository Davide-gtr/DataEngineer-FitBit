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


def createStepsDataframe(start_time, end_time):
    # Create daily steps count dataframe
    df_dailySteps = pd.DataFrame({'Datetime': pd.Series(dtype='datetime64[ns]'),
                                'Step_count': pd.Series(dtype='int')})

    dailyDataSteps = auth2_client.time_series('activities/steps', base_date=start_time, end_date=end_time)

    datetimeList, stepsList = [], []
    for el in dailyDataSteps['activities-steps']:
        datetimeList.append(datetime.datetime.strptime(el['dateTime'], "%Y-%m-%d"))
        stepsList.append(int(el['value']))

    df_dailySteps['Datetime'] = datetimeList
    df_dailySteps['Step_count'] = stepsList

    df_dailySteps = df_dailySteps.set_index('Datetime')

    return df_dailySteps

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

    # Parse the date for right format
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    
    startTime = pd.datetime(year=start_date[2], month=start_date[1], day=start_date[0])
    endTime = pd.datetime(year=end_date[2], month=end_date[1], day=end_date[0])

    # Create dataframe
    dfSteps = createStepsDataframe(startTime, endTime)

    # save into CSV file
    if not os.path.exists("data"):
        os.mkdir("data")

    dfSteps.to_csv(f'./data/stepsData_FROM_{startTime}_TO_{endTime}.csv')


if __name__ == '__main__':
    main()