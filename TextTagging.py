# -*- coding: utf-8 -*-

# __title__ = 'TextTagging'
# __version__ = '1.0.0'
# __author__ = 'su.choi@niccompany.co.kr'
# __license__ = ''
# __copyright__ = 'Niccompany'


from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import models
import os
import json
import numpy as np
import pickle


installpath = os.path.dirname(os.path.realpath(__file__))

class NicWordTagging():

    """ 적요 텍스트를 분류하기 위한 메소드

    1. Notes
    -----
    NicWordTagging 매서드를 호출하면 info에 있는 카테고리.json 파일을
    models에 있는 토크나이저 및 입금, 지급 적요 분류 모델을 호출합니다.
    적요 텍스트 분류를 하기 위한 함수를 제공합니다.

    2. Examples
    -----
    >> from ats_module.TextTagging import NicWordTagging
    >> nwt = NicWordTagging()
    """
    def __init__(self):

        # 적요 텍스트에 대한 카테고리 파일
        with open('%s/info/categorical_name_v0.78.json' % installpath, 'r', encoding="utf-8-sig") as fp:
            self.info = json.load(fp)

        # 입금, 지급별 시퀸스 길이가 등록된 파일
        with open('%s/models/input_length_v0.78.json' % installpath, 'rb') as fp:
            self.inputlength = json.load(fp)

        # 금융 말뭉치에 대한 정수인코딩 모델 파일
        with open('%s/models/tokenizer/tokenizer_v0.78.pkl' % installpath, 'rb') as handle:
            self.tokenizer = pickle.load(handle)

        # 적요 텍스트를 분리하기 위한 머신러닝 모델 파일
        self.model_ex = models.load_model('%s/models/L3/ex_v0.78_9.h5' % installpath)
        self.model_de = models.load_model('%s/models/L3/de_v0.78_14.h5' % installpath)


    def text_tagging(self, string, code):

        """ NicWordTagging의 적요 텍스트를 분류하기 위한 함수

        1. Notes
        -----
        텍스트를 정수인코딩 한 시퀸스로 바꾸고 입금, 지급 여부에 따라
        해당 머신러닝 모델을 이용한 예측결과를 반환합니다.

        2. Parameter
        -----
        string: str
            적요에 들어간 텍스트, text_tagging 사용시 반드시 들어가야 합니다.

        code: str, '1' or '2'
            입금, 지급 여부, text_tagging 사용시 반드시 들어가야 합니다.

        3. Return
        -----
        result: tuple of shape, (1, 2)
            적요 텍스트에 대한 카테고리 결과, 1은 대분류, 2는 중분류 결과를 반환합니다.
            입금, 지급 여부 체크시(code) else로 들어갈 경우 ("error", "error")를 반환합니다.

        4. Examples
        -----
        >> from ats_module.TextTagging import NicWordTagging
        >> nwt = NicWordTagging()
        >> nwt.text_tagging(data, '입금') #('대인거래', '개인입금')
        """

        # 문자열인지 체크
        string_check(string)

        # code가 1 또는 2인지 체크합니다.
        if code == '1':
            code = '지급'
        elif code == '2':
            code = '입금'
        else:
            return ('error', 'error')

        # string에 대한 정수인코딩 된 시퀸스
        sequences_array = self.tokenizer.texts_to_sequences([string.split()])
        lists = pad_sequences(sequences_array, maxlen=self.inputlength[code])

        # 적요 텍스트 분류
        if code == '지급':
            result = str(np.argmax(self.model_ex.predict(lists, verbose=0), axis=1)[0])
            result = [k for k, v in self.info[code].items() if v == result][0]
        elif code == '입금':
            result = str(np.argmax(self.model_de.predict(lists, verbose=0), axis=1)[0])
            result = [k for k, v in self.info[code].items() if v == result][0]
        
        return (result.split("_")[0], result.split("_")[1])
        


#### input 타입체크 
def string_check(x):
    assert type(x) is str, "문자열 형식이 아닙니다. 적요 텍스트의 타입을 확인해주세요. {}".format(x)