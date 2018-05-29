import urllib.parse
import pandas as pd
from pandas_datareader import data as wb
from datetime import datetime
import sqlite3
import time
from bs4 import BeautifulSoup
import requests
from time import sleep
from multiprocessing import Process
import queue

MARKET_CODE_DICT = {
    'kospi': 'stockMkt',
    'kosdaq': 'kosdaqMkt',
    'konex': 'konexMkt'
}
DOWNLOAD_URL = 'kind.krx.co.kr/corpgeneral/corpList.do'

def download_stock_codes(market=None, delisted=False):
    params = {'method': 'download'}

    if market.lower() in MARKET_CODE_DICT:
        params['marketType'] = MARKET_CODE_DICT[market]

    if not delisted:
        params['searchType'] = 13

    params_string = urllib.parse.urlencode(params)
    request_url = urllib.parse.urlunsplit(['http', DOWNLOAD_URL, '', params_string, ''])

    df = pd.read_html(request_url, header=0)[0]
    df.종목코드 = df.종목코드.map('{:06d}'.format)
    return df

# 종목 이름을 입력하면 종목에 해당하는 코드를 불러와
# 네이버 금융(http://finance.naver.com)에 넣어줌
def get_url_with_company_name(item_name, code_df):
    code = code_df.query("회사명=='{}'".format(item_name))['종목코드'].to_string(index=False)
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    print("요청 URL = {}".format(url))
    return url

def get_daily_price_from_naver(code) :
    code = str(code).zfill(6)
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    # 마지막 페이지
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'lxml')
    pgRR = soup.find_all('td', {'class': 'pgRR'})[0].find('a').get('href')
    last_page = ''
    for digit in pgRR[::-1] :
        if digit == '=' :
            break
        else :
            last_page += digit
    last_page = int(last_page[::-1])
    print("마지막 페이지 :", last_page)

    # 가격정보
    price = pd.DataFrame()
    for page in range(1, last_page+1) :
        pg_url = '{url}&page={page}'.format(url=url, page=page)
        price = price.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)
        price = price[['날짜', '시가', '종가', '고가', '저가', '거래량']]
        # TODO 새로운 날짜 업데이트 하는 것 try, except로 처리\
        sleep(0.05)
        if page % 50 == 0 :
            price.dropna(inplace=True)
            print("------{} : 가격 정보 받아 오는 중 page:{}/{}------".format(code, page, last_page))
    price.dropna(inplace=True)
    print(price.head())
    price.to_csv('./resources/kosdaq/{}.csv'.format(code), sep='\t', encoding='utf-8')

    return price

def get_csv_price_file_from_naver(stock_code, market):
    price = {}
    name = get_company_name_from_code(stock_code[market],code)
    print('회사명:{}({}) '.format(name ,code))
    price[code] = get_daily_price_from_naver(str(code).zfill(6))
    price[code].to_csv('./resources/{}/{}.csv'.format(market, code), sep='\t', encoding='utf-8')
    print('회사명:{}({}) 완료'.format(name ,code))
    return price

def get_stock_code_from_csv() :
    stock_code = {}
    for market in ['kospi', 'kosdaq'] :
        stock_code[market] = pd.read_csv('./resources/{}_code.csv'.format(market))
        stock_code[market] = stock_code[market][['회사명','종목코드']]
    return stock_code

def get_company_name_from_code(code_df, code) :
    name = code_df.query("종목코드=='{}'".format(code))['회사명']
    return name

    # print(get_company_name_from_code(stock_code['kospi'], '000020'))

if __name__ == '__main__' :

    # 종목 코드 csv 파일에서 가져오기
    markets = ['kospi', 'kosdaq']
    stock_code = get_stock_code_from_csv()

    TASKS = 5
    market = 'kosdaq'

    queue_ccode = []
    ccode_count = 1
    for ccode in stock_code[market]['종목코드'] :
        queue_ccode.append(ccode)
        if len(queue_ccode) == 5 :
            procs = []
            for ccode in queue_ccode :
                proc = Process(target=get_daily_price_from_naver, args=(ccode,))
                procs.append(proc)
                proc.start()
            for proc in procs :
                proc.join()

            procs=[]
            queue_ccode = []

        print('================={}/{} {}================='.format(ccode_count, len(stock_code[market]['종목코드']),market))
        ccode_count += 5

'''

    # print(results)
            # df = pd.concat(results, axis=1)
            # df.loc[:, pd.IndexSlice[:, 'Adj Close']].tail()

    Code Snippet

    # 종목 코드 csv로 저장하기
    for market in ['kospi', 'kosdaq'] :
        stock_codes = download_stock_codes(market=market, delisted=False)
        stock_codes.to_csv('./resources/{}_code.csv'.format(market))

    # Pandas로 주가 정보 얻기
    results = {}
    temp_stock_code = stock_code['kosdaq'][:1]
        for code in temp_stock_code.종목코드:
        results[code] = wb.DataReader(str(code).zfill(6) + '.KQ', 'yahoo')
    #

    # DB에 Table생성 및 업데이트
    for name in stock_code['kosdaq']['회사명'] :
        try :
            sql = "create table {} (Date text, Open int, High int, Low int, Close int, Volumn int)"
            cursor.execute(sql.format(name))
            con.commit()
        except :
            print('Already exists')
    con.close()

'''

# TODO 시간별 시세 크롤링.
# TODO 급등주 찾기.(팍스넷, 네이버 등등)
