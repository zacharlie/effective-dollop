import os
import pandas as pd

def fix_covid_dates(input_file):
    df=pd.read_csv(input_file)  # input file to pandas dataframe
    df.rename(columns = {'Date':'old_date'}, inplace = True)  # rename the broken column

    # perform a date conversion that makes the values sensible for computers
    df['Date'] = pd.to_datetime(df['old_date'], format='%m/%d/%y', errors='ignore')
    # note the special use of %y instead of %Y to parse a 2 digit instead of a 4 digit year value
    del df['old_date']  # drop the broken column

    output_file = os.path.basename(os.path.splitext(input_file)[0]) + '_fixed.csv'
    df.to_csv(output_file,index=False)  # save result to file
    print('{} exported...'.format(output_file))       

try:
    fix_covid_dates('Confirmed.csv')
    fix_covid_dates('Deaths.csv')
    fix_covid_dates('Recoveries.csv')

except Exception as err:
    print(err)