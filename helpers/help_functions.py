#! /usr/bin/env python3

import datetime

def create_cosecha():
    month = datetime.datetime.now().month
    if month == 5:
        year = datetime.datetime.now().year
        full_cos = f'{year}/{year+1}'
        var_cos = f'COS{year}{year+1}'
        return var_cos, full_cos


if __name__ == '__main__':
    create_cosecha()