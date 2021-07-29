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

import datetime
import gspread
from my_utils import change_timeformat


def get_list():
    gc = gspread.service_account(filename="creds__.json")
    sheet = gc.open("StressMeOut").sheet1
    data = sheet.get_all_records()

    res = []
    for i in data:
        res.append([i["TITLE"], i["dd.mm.yyyy hh:mm"]])
    return res


def conv_list():
    res = get_list()
    current = datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)
    for i in range(len(res)):
        left = change_timeformat(res[i][1])
        if left:
            left = str(left - current)
            res[i][1] = left[0:len(left) - 10] + " Hours left"
            if left[0] == "-":
                res[i][1] = "over"
        else:
            res[i][1] = "To Be Announced"
    return res
