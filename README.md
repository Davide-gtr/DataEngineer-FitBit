# DataEngineer-FitBit

### By Davide Garcia Civiero

This Data Engineer project consist in building a pipeline to retrieve data from connected watch FitBit.


As a FitBit connected watch owner I wanted to retrieve the data collected by my watch and do some analysis on my own. <br>
This project was the opportunity to develop my Python programming skills as well as my Data Engineering competences such as connecting to an API. 

The project consist in different steps : <br>

- Connect to the FitBit API with the credentials
- Extract the desired data (sleep, calories, activities etc.)
- Transform the data in a useful form (parsing and cleaning)
- Storing the data in DataFrames and CSV files
- Further analysis

The repository has different files, one for each data category (sleep, activities, heart rate, steps number).

For example, if I want to retrieve sleep information I must execute the following command in the Terminal : <br>
`python getSleepData.py [initial date] [final date]`

It will give a CSV file containing all the sleep data between the two dates (in format `DD-MM-YYYY`

