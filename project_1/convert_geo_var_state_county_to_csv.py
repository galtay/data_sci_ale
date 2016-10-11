import os
import sys
import time
import pandas

def convert_xlsx_to_csv(excel_fname):
    """Convert sheets in Excel file to CSVs for faster I/O"""

    print()
    print('converting Excel file to CSVs ...')
    print('excel file: {}'.format(excel_fname))
    dirname = os.path.dirname(excel_fname)
    basename = os.path.basename(excel_fname)
    fbase, ext = basename.split('.')

    print('reading sheetnames ...')
    excel_file = pandas.ExcelFile(excel_fname)
    sheetnames = excel_file.sheet_names
    print('sheetnames: {}'.format(sheetnames))

    for sheetname in sheetnames:
        if sheetname != 'Documentation':
            year = sheetname.split(' ')[-1]
            csv_fname = '{}_{}.csv'.format(os.path.join(dirname, fbase), year)
            if os.path.isfile(csv_fname):
                print('csv file {} already exists'.format(csv_fname))
                continue
            print('reading file: {}, sheet: {}'.format(excel_fname, sheetname))
            t1 = time.time()
            df = pandas.read_excel(
                excel_fname, sheetname=sheetname, header=1, engine='xlrd',
                na_values=['.', '*'])
            t2 = time.time()
            print('I/O took {} seconds'.format(t2-t1))
            print('writing to {}'.format(csv_fname))
            df.to_csv(csv_fname)


if __name__ == '__main__':

    USAGE = """
     > python convert_geo_var_state_county_to_csv.py ./data/County_All_Table.xlsx
    """

    if len(sys.argv) != 2:
        print(USAGE)

    excel_fname = sys.argv[1]
    convert_xlsx_to_csv(excel_fname)
