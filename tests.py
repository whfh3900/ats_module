# -*- coding: utf-8 -*-

# __title__ = 'tests'
# __version__ = '1.0.0'
# __author__ = 'su.choi@niccompany.co.kr'
# __license__ = ''
# __copyright__ = 'Niccompany'

import sys
import platform
from TextPreprocessing import *
from TextTagging import *
import multiprocessing
import datetime
import time

if platform.system() == 'Windows':
    from multiprocessing import Pool
elif platform.system() == 'Linux':
    from multiprocessing.pool import ThreadPool as Pool

nk = Nickonlpy()
nwt = NicWordTagging()

def work_func(df):
    for i, n in df.iterrows():
        ori_text = str(n['적요'])
        trans_md = str(n['거래구분'])

        if trans_md in ['1', '2']:
            # preprocessing
            pro_text = find_null(ori_text)
            pro_text = ascii_check(pro_text)
            pro_text = change_upper(pro_text)
            pro_text = space_delete(pro_text)
            pro_text = remove_bank(pro_text)
            pro_text = corporatebody(pro_text)
            pro_text = numbers_to_zero(pro_text)
            pro_text = remove_specialchar(pro_text)
            pro_text = space_delete(pro_text)
            pro_text = find_null(pro_text)

            if (pro_text != "공백") or (len(pro_text) >= 1):
                # tagging
                pro_text = nk.predict_tokennize(pro_text)
                result = nwt.text_tagging(pro_text, trans_md)
                pro_text = nk.name_check(pro_text)
            else:
                result = ("", "")
        else:
            result = ("", "")

        df.at[i, "대분류"] = result[0]
        df.at[i, "중분류"] = result[1]

    return df

def parallel_dataframe(df, func, num_cores):
    df_split = np.array_split(df, num_cores)
    pool = Pool(num_cores)
    return pd.concat(pool.map(func, df_split))


if __name__ == '__main__':
    if platform.system() == 'Windows':
        multiprocessing.freeze_support()

    # 90만개 데이터
    # 2번쨰 인자로 원하는 개수만큼 데이터 지정
    path = "./data/new_test_v2-0.9mega.csv"
    df = pd.read_csv(path, encoding='utf-8-sig')[:int(sys.argv[2])]
    df["대분류"] = np.nan
    df["중분류"] = np.nan
    df["비고"] = np.nan

    # 1번째 인자로 사용할 cpu코어 개수 설정
    num_cores = int(sys.argv[1])
    start = time.time()
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Start Time", start_time)
    print("진행중...")
    df = parallel_dataframe(df, work_func, num_cores)
    end = time.time()
    end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("End Time", end_time)

    sec = (end - start)
    result = datetime.timedelta(seconds=sec)
    print("총 걸린시간: ", result)

    del df

