import pandas


WEATHER_FNAME = 'weather.dat'
FOOTBALL_FNAME = 'football.dat'


def read_weather(fname=WEATHER_FNAME):
    """Read the weather file into a DataFrame and return it.

    Pandas has many input routines (all prefixed with "read")

      - http://pandas.pydata.org/pandas-docs/stable/io.html

    Examining the weather.dat file we see that it has 17 columns.  This file
    might look like it's white space delimited but no!  This, my friends, is
    a fixed width file.  Although Pandas allows arbitrary regular expressions
    for delimiter values (for example we could use "\s+" for one or more white
    spaces) there are some columns that have no values and this would break.
    For example, the column HDDay has no values until the 9th row.  Using "one
    or more white spaces" as the delimiter would make 53.8 the value for HDDay
    in the first row.

    The function that we want is pandas.read_fwf (for fixed width file).  It
    turns out that pandas.read_fwf is *almost* smart enough to automatically
    determine the widths of the columns.  In the end we need to specify them
    to get the last columns read correctly.
    """

    # things I tried that don't work
    # 1) df = pandas.read_csv(fname)
    # 2) df = pandas.read_csv(fname, delimiter=' ')
    # 3) df = pandas.read_csv(fname, delimiter='\s+')
    # 4) df = pandas.read_fwf(fname)
    df = pandas.read_fwf(
        fname, widths=[4, 6, 6, 6, 7, 6, 5, 6, 6, 6, 5, 4, 4, 4, 4, 4, 6])

    # we still have a row on top full of NaN because there was a blank line
    # just below the header.  we could use dropna(axis=0, how='all') but that
    # would also drop any rows that happen to be empty in the middle of the
    # data.  instead we can simply use drop(0) which is the label of the row.
    # also note that almost every pandas operation returns a new object and
    # doesn't operate in place so we assign the results to df.
    df = df.drop(0)
    return df




if __name__ == '__main__':

    # I usually use a naming convention that appends "_df" to DataFrames
    weather_df = read_weather()

    # Pandas guesses the types for each column.  "object" is a native python
    # string and what Pandas defaults to when it cant guess.
    print(weather_df.dtypes)
    print()

    # you can index columns by passing a string or a list of strings
    # into the square bracket operator
    print(weather_df['WxType'])
    print

    print(weather_df[['HDDay', 'AvSLP']])
    print

    # "loc" and "iloc" are ways to index into the DataFrame
