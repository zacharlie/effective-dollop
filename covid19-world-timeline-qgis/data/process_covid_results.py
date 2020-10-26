import pandas as pd

def process_covid_csv(input_file, case_type='cases',
    attr_fields=1, date_fields=1):
    '''convert CSSEGIS COVID-19 time series data from 2D
    matrix into multi-row elements for use with QGIS
    https://github.com/CSSEGISandData/COVID-19'''
    df=pd.read_csv(input_file)  # input file to pandas dataframe
    column_names = df.columns.tolist()  # get a list of columns
    id_fields = column_names[0:attr_fields]  # attribute fields to replicate
    dates_end = attr_fields + date_fields  # get total number of columns
    data_fields = column_names[attr_fields:dates_end]  # get index of data field columns

    data = pd.melt(df, id_vars=id_fields, value_vars=data_fields,
                   var_name='Date', value_name=case_type)
    data.reset_index(drop=True)  # index cleanup
    output_file = case_type + '.csv'
    data.to_csv(output_file,index=False)  # save result to file
    print('{} exported...'.format(output_file))

try:
    process_covid_csv(input_file="time_series_covid19_confirmed_global.csv",
                      case_type='Confirmed', attr_fields=4, date_fields=277)

    process_covid_csv(input_file="time_series_covid19_deaths_global.csv",
                      case_type='Deaths', attr_fields=4, date_fields=277)

    process_covid_csv(input_file="time_series_covid19_recovered_global.csv",
                      case_type='Recoveries',  attr_fields=4, date_fields=277)

except Exception as err:
    print(err)