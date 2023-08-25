# Python script to retrieve all the data heart

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


outOfRange = 0
fatBurn = 1
cardio = 2
peak = 3

def createHeartDataframe(category, startTime, endTime):
        date_list = []
        df_list = []
        allDates = pd.date_range(start=startTime, end=endTime)

        for oneDate in allDates:
            oneDate = oneDate.date().strftime("%Y-%m-%d")
            oneDate = datetime.datetime.strptime(oneDate, '%Y-%m-%d')

            oneDayData = auth2_client.intraday_time_series('activities/heart', base_date=oneDate, detail_level='1sec')
            df = pd.DataFrame(oneDayData['activities-heart'])

            date_list.append(oneDate)

            df_list.append(df)

        final_df_list = []

        for date, df in zip(date_list, df_list):
            if len(df) == 0:
                continue
            df.loc[:, 'date'] = pd.to_datetime(date)

            final_df_list.append(df)

        final_df = pd.concat(final_df_list, axis = 0, ignore_index=True)

        df = pd.DataFrame({'Calories': pd.Series(dtype='float64'),
                     'MaxHeartRate':pd.Series(dtype='float64'),
                     'MinHeartRate':pd.Series(dtype='float64'),
                     'Duration (min)':pd.Series(dtype='int')
                     })
        
        caloriesList, maxList, minList, minutesList, datetimeList = [], [], [], [], []
        for _, row in final_df.iterrows():
            
            datetimeList.append(row['date']) # retrieve the datetime for each element

            # Retrieve calories
            caloriesList.append(row['value']['heartRateZones'][category]['caloriesOut'])
            # Retrieve max heart rate
            maxList.append(row['value']['heartRateZones'][category]['max'])
            # Retrieve min heart rate
            minList.append(row['value']['heartRateZones'][category]['min'])
            # Retrieve duration
            minutesList.append(row['value']['heartRateZones'][category]['minutes'])
            
        # Create the dataframe
        df['Calories'] = caloriesList
        df['MaxHeartRate'] = maxList
        df['MinHeartRate'] = minList
        df['Minutes'] = minutesList
        df['datetime'] = datetimeList
        
        # Set datetime as index
        df = df.set_index('datetime')

        return df


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

    # Create dataframes
    categoryDict = {'OOR': 0, 'FB': 1, 'C': 2, 'P': 3}
    df_OOR = createHeartDataframe(categoryDict['OOR'], startTime, endTime)
    df_FB = createHeartDataframe(categoryDict['FB'], startTime, endTime)
    df_C = createHeartDataframe(categoryDict['C'], startTime, endTime)
    df_P = createHeartDataframe(categoryDict['P'], startTime, endTime)
    
    # save into CSV file into data folder
    if not os.path.exists("data"):
         os.mkdir("data")
         
    df_OOR.to_csv(f'./data/OORData_FROM_{startTime}_TO_{endTime}.csv')
    df_FB.to_csv(f'./data/fatBurnData_FROM_{startTime}_TO_{endTime}.csv')
    df_C.to_csv(f'./data/cardioData_FROM_{startTime}_TO_{endTime}.csv')
    df_P.to_csv(f'./data/peakData_FROM_{startTime}_TO_{endTime}.csv')


if __name__ == '__main__':
    main()
