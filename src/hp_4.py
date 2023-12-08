# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
import csv
from collections import defaultdict


def reformat_dates(old_dates):
    
    new_dates =[]
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    for date in old_dates:
        
        date_obj = datetime.strptime(date, "%Y-%m-%d").strftime('%d %b %Y')
        new_dates.append(date_obj)
        
    return new_dates



def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str):
        raise TypeError("Enter the string data type only")
    if not isinstance(n, int):
        raise TypeError("Enter integer data type")
    
    dates = []
    
    start_date = datetime.strptime(start, '%Y-%m-%d')
    
    for i in range(n):
        
        dates.append(start_date + timedelta(days=i))
        
    return dates


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    days = len(values)
    
    date_range_list = date_range(start_date, days)

    date_rang = list(zip(date_range_list, values))
    
    return date_rang


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    headers = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".
              split(','))
    outputs = defaultdict(float)
    with open(infile, 'r') as file:
        lines = DictReader(file, fieldnames=headers)
        rows = [row for row in lines]

    rows.pop(0)
       
    for row in rows:
       
        patron_id = row['patron_id']
        
        date_due = datetime.strptime(row['date_due'], "%m/%d/%Y")
        
        date_returned = datetime.strptime(row['date_returned'], "%m/%d/%Y")
        
        late_days = (date_returned - date_due).days
        
        outputs[patron_id]+= 0.25 * late_days if late_days > 0 else 0.0
        
                 
    headers = [
        {'patron_id': patron_id, 'late_fees': f'{late_fee:0.2f}'} for patron_id, late_fee in outputs.items()
    ]
    finalheader = ['patron_id', 'late_fees']
    with open(outfile, 'w') as f:
        
        writer = DictWriter(f,finalheader)
        writer.writeheader()
        writer.writerows(headers)

            
            
 

# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
