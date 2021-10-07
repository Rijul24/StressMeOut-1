"""MIT License

Copyright (c) 2021 armaanbadhan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import gspread
import datetime

from utils.misc import change_timeformat


def conv_list():
    gc = gspread.service_account(filename="creds__.json")
    sheet = gc.open("StressMeOut").sheet1
    data = sheet.get_all_records()

    over, curr, tba = [], [], []
    current_time = datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)
    for i in data:
        if not change_timeformat(i["dd.mm.yyyy hh:mm"]):       # time format doesnt match
            tba.append([i["TITLE"], "To Be Announced"])
        else:
            if ( xmas := change_timeformat(i["dd.mm.yyyy hh:mm"]) ) < current_time:
                over.append([i["TITLE"], "OVER"])
            else:
                curr.append([i["TITLE"], xmas])

    curr.sort(key=lambda x: x[1])

    for i in curr:
        left = str(i[1] - current_time)
        i[1] = left[0:len(left) - 10] + " Hours left"

    res = over + curr + tba

    return res, len(res)
