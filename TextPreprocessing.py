# -*- coding: utf-8 -*-

# __title__ = 'TextPreprocessing'
# __version__ = '1.0.0'
# __author__ = 'su.choi@niccompany.co.kr'
# __license__ = ''
# __copyright__ = 'Niccompany'


import re
from ckonlpy.tag import Twitter
from ckonlpy.tag import Postprocessor
from konlpy.tag import Okt
import pandas as pd

class Nickonlpy():

    """ 적요 텍스트를 전처리 하기 위한 메소드

    1. Notes
    -----
    Nickonlpy 매서드를 호출하면 적요 텍스트를 전처리하기 위한 ckonlpy 라이브러리를 호출합니다.
    금융 말뭉치를 이용한 형태소 분석기(토크나이저)를 사용하기 위한 함수를 제공합니다.

    2. Parameter
    -----
    base: bool, default=False
        False일시 말뭉치 용어사전을 사용한 ckonlpy, True일시 일반 konlpy 라이브러리를 사용합니다.

    3. Examples
    -----
    >> from ats_module.TextPreprocessing import Nickonlpy
    >> nk = Nickonlpy(base=False)
    """

    def __init__(self, base=False):
        if base == False:
            self.twitter = Twitter()
            self.post = Postprocessor(self.twitter)
        else:
            self.post = Okt()

    def name_check(self, string):

        """ 적요 텍스트에서 사람이름을 찾습니다.

        1. Notes
        -----
        적요 텍스트에서 사람이름에 해당하는 텍스트는 빈 문자열("")로 수정하여 반환합니다.
        단, Nickonlpy 메서드의 base가 False일 때만 유의미 합니다.

        2. Parameter
        -----
        string: str
            적요에 들어간 텍스트

        3. Examples
        -----
        >> from ats_module.TextPreprocessing import Nickonlpy
        >> nk = Nickonlpy(base=False)
        >> nk.name_check("신한최승언")
        """

        # 문자열인지 체크
        string_check(string)

        # 형태소 분석기의 pos 함수를 이용해 태그가 Name일 시 빈 문자열을 반환하도록 합니다
        names = [i[0] for i in self.post.pos(string) if i[1] == 'Name']
        if names:
            for name in names:
                return string.replace(name, '')
        else: return string

    def predict_tokennize(self, string):

        """ 적요 텍스트를 형태소 분석기를 통해 토큰화 합니다.

        1. Parameter
        -----
        string: str
            적요에 들어간 텍스트

        2. Examples
        -----
        >> from ats_module.TextPreprocessing import Nickonlpy
        >> nk = Nickonlpy(base=False)
        >> nk.predict_tokennize("신한최승언")
        """

        # 문자열인지 체크
        string_check(string)

        # 형태소 분석기의 pos 함수를 이용해 토크나이저 기능을 구현합니다.
        return ' '.join([i[0] for i in self.post.pos(string)])


def ascii_check(string):

    """ 사용하지 않은 아스키코드를 치환합니다

    1. Parameter
    -----
    string: str
        적요에 들어간 텍스트

    2. Examples
    -----
    >> from ats_module.TextPreprocessing import ascii_check
    >> ascii_check("ＳＳＧＰＡＹ")
    """

    # 문자열인지 체크
    string_check(string)
    string = list(str(string))
    hex_ascii_diff = int('0xfee0', 16)
    hex_ascii_blank = int('0x3000', 16)
    for i in range(len(string)):

        full = string[i]
        # 16진수인 ascii code
        hex_ascii_full = ord(full)
        # 16진수 형태의 string
        # hex_full = hex(hex_ascii_full)

        # 전각일 경우 전각 기준인 값을 차감해 반각으로 변경
        if hex_ascii_full >= hex_ascii_diff:
            string[i] = chr(hex_ascii_full - hex_ascii_diff)
        # 빈칸이 전각일 경우는 위 공식에 어긋나므로 강제로 반각형태의 빈칸을 지정
        elif hex_ascii_full == hex_ascii_blank:
            string[i] = chr(32)
        # (주)가 전각인 형태가 들어올 수 있으므로 주식회사로 변경
        elif hex_ascii_full == 12828:
            string[i] = ' 주식회사 '
    return ''.join(string)


def corporatebody(string):

    """ ()안에 법인명을 풀어서 치환 합니다

    1. Parameter
    -----
    string: str
        적요에 들어간 텍스트

    2. Examples
    -----
    >> from ats_module.TextPreprocessing import corporatebody
    >> corporatebody('(주) 닉컴퍼니')
    """

    # 문자열인지 체크
    string_check(string)
    cor_dict = {"(주)": " 주식회사 ",
                "(사)": " 사단법인 ",
                "(재단)": " 재단법인 ",
                "(유)": " 유한회사 ",
                "(재)": " 재단법인 ",
                "(학)": " 학교법인 ",
                "(합)": " 합자회사 ",
                "(복)": " 복지재단 ",
                "(의)": " 의료재단 ",
                "(사복)": " 사회복지법인 ",
                "(유한)": " 유한회사 ",}

    for i, n in cor_dict.items():
        string = string.replace(i, n)
    return string


def remove_specialchar(string):

    """ 모든 특수문자를 빈 공백으로 치환합니다

    1. Parameter
    -----
    string: str
        적요에 들어간 텍스트

    2. Examples
    -----
    >> from ats_module.TextPreprocessing import remove_specialchar
    >> remove_specialchar('우리카드결제-00')
    """

    # 문자열인지 체크
    string_check(string)
    return re.sub(r"[^a-zA-Z0-9가-힣 ]", " ", string)


def numbers_check(string):

    """ 적요 텍스트에 숫자를 "숫자"라는 단어로 치환합니다.

    1. Parameter
    -----
    string: str
        적요에 들어간 텍스트

    2. Examples
    -----
    >> from ats_module.TextPreprocessing import numbers_check
    >> numbers_check('현대라 02-048')
    """

    # 문자열인지 체크
    string_check(string)

    # 숫자로 이루어진 문자열을 리스트 형식으로 반환
    numbers = re.findall(r'\d+', string)
    index = list()
    end_index = 0
    for i in numbers:

        # 문자열에서 해당 숫자가 있는 index의 시작지점과 끝지점을 저장
        start_index = string.find(i, end_index)
        index.append(start_index)
        end_index = string.find(i, end_index)+len(i)
        index.append(end_index)
    string_list = list(string)

    # 리스트로 변경한 문자열에서 시작지점과 끝지점에 공백을 추가
    for jump, i in enumerate(index):
        string_list.insert(i+jump, ' ')

    # 숫자가 들어간 문자열을 모두 '숫자'라는 단어로 치환
    string_list = ''.join(string_list).split()
    string_list = ['숫자' if i in numbers else i for i in string_list]
    string_list = ' '.join(string_list)

    # 숫자 뒤에 해당 리스트의 단어가 들어간 경우 숫자와 해당 단어를 붙여서 반환
    for n in ['월', '차전', '개', '회차', '원', '기', '호', '차', '건', '회', '일', '년', '동']:
        string_list = string_list.replace('숫자 %s'%n, '숫자%s '%n)
    return string_list

def numbers_to_zero(string):

    """ 모든 숫자를 0으로 변경

    1. Parameter
    -----
    string: str
        적요에 들어간 텍스트

    2. Examples
    -----
    >> from ats_module.TextPreprocessing import numbers_to_zero
    >> numbers_to_zero('현대라 02-048')
    """

    # 문자열인지 체크
    string_check(string)
    string = re.sub('[1-9]', '0', string)
    return string


def find_null(string):

    """ null 타입 또는 빈 공백이면 "공백"이라는 단어를 반환합니다

    1. Parameter
    -----
    string: str
        적요에 들어간 텍스트

    2. Examples
    -----
    >> from ats_module.TextPreprocessing import find_null
    >> find_null('')
    """

    if (string == "") or (pd.isnull(string)):
        return "공백"
    else:
        return string

def space_delete(string):

    """ 이중 공백을 제거합니다

    1. Parameter
    -----
    string: str
        적요에 들어간 텍스트

    2. Examples
    -----
    >> from ats_module.TextPreprocessing import space_delete
    >> space_delete(' 주식회사  ')
    """
    # 문자열인지 체크
    string_check(string)
    return string.strip()


def remove_bank(string):

    """ 은행명 뒤에 하이픈이 붙을 경우 해당 텍스트는 제거합니다.

    1. Parameter
    -----
    string: str
        적요에 들어간 텍스트

    2. Examples
    -----
    >> from ats_module.TextPreprocessing import remove_bank
    >> remove_bank('신한-마이신한포인트')
    """

    # 문자열인지 체크
    string_check(string)
    if string.startswith(('신한-', 'SC-', '국민-', 'KB-', '기업-', '농협-', '우리-', \
                          '금고-', '경남-', '대구-', '우체-', '하나-', '수협-', '부산-', \
                          '신협-')):
        return string[3:]
    else:
        return string


def change_upper(string):

    """ 모든 알파벳을 대문자로 변경합니다

    1. Parameter
    -----
    string: str
        적요에 들어간 텍스트

    2. Examples
    -----
    >> from ats_module.TextPreprocessing import change_upper
    >> change_upper('SINHAN')
    """

    # 문자열인지 체크
    string_check(string)
    return string.upper()


#### input 타입체크 
def string_check(x):
    assert type(x) is str, "문자열 형식이 아닙니다. 적요 텍스트의 타입을 확인해주세요. {}".format(x)
