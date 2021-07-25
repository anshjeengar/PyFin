import datetime
import os
from zipfile import ZipFile

import requests
from icecream import ic
from wget import download

ic.enable()


date_from = (datetime.date.today() - datetime.timedelta(days=5)).isoformat()
date_to = (datetime.date.today()).isoformat()
ic(f'Date Range: {date_from} to {date_to}')


def getbhav_data(date_from: str, date_to: str):
    date1 = datetime.date.fromisoformat(date_from)
    date2 = datetime.date.fromisoformat(date_to)

    months = {
        1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN',
        7: 'JUL', 8: 'AUG', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DEC'
    }

    if not os.path.exists('./bhavcopy/'):
        os.mkdir('./bhavcopy/')
        os.chdir('./bhavcopy/')

    def daterange(date_from, date_to):
        for n in range(int((date_to - date_from).days + 1)):
            yield date_from + datetime.timedelta(n)

    for date in daterange(date1, date2):
        url_NSE_archive_of_daily_monthly_reports = 'https://www1.nseindia.com/products/content/equities/equities/archieve_eq.htm'
        url_bhavcopy_daily = f'https://www1.nseindia.com/content/historical/EQUITIES/{date.year}/{months[date.month]}/cm{date.day}{months[date.month]}{date.year}bhav.csv.zip'
        req = requests.get(url_NSE_archive_of_daily_monthly_reports)
        ic(req.status_code)
        ZipFile = download(url_bhavcopy_daily)


        # def extract_zip(zip_file, extract_path):
getbhav_data(date_from, date_to)
