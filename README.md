<<<<<<< HEAD
# ats_modules
> ats_modules은 금융 적요 서비스를 위한 전처리 및 태깅 기능 라이브러리 입니다.
![](./png/image.png)


## 설치 방법
1. [ats_ckonlpy](https://github.com/whfh3900/ats_ckonlpy) 을 참고하여 설치.<br>
2. pip install
- tensorflow-gpu==2.10.0<br>
- pandas==1.2.4<br>
- numpy==1.21.4<br>
3. git clone
```bash
git clone https://github.com/whfh3900/ats_module.git
```

## Preprocessing 사용법

```python
# 사용하지 않은 아스키코드 치환
from ats_module.TextPreprocessing import ascii_check
print(ascii_check('ＳＳＧＰＡＹ')) #SSGPAY

# (주)는 주식회사로 치환
from ats_module.TextPreprocessing import corporatebody
printcorporatebody('(주) 닉컴퍼니')) #주식회사 닉컴퍼니

# 특수문자 제거
from ats_module.TextPreprocessing import remove_specialchar
print(remove_specialchar('우리카드결제-00')) #우리카드결제 00

# 숫자는 숫자라는 단어로 치환 (자릿수에 상관없이 “숫자”로 치환)
from ats_module.TextPreprocessing import numbers_check
print(numbers_check('현대라 02-048')) #현대라 숫자 - 숫자

# 빈셀은 공백이란 단어로 치환
from ats_module.TextPreprocessing import find_null
print(find_null('')) #공백

# 전처리 결과 빈셀이면 공백이란 단어로 치환
from ats_module.TextPreprocessing import space_delete
print(space_delete('')) #공백

# 사람이름 인식 후 이름이라는 단어로 치환
from ats_module.TextPreprocessing import Nickonlpy
=======
# ATS

ATS는 금융 적요 서비스를 위한 전처리 및 태깅 기능 라이브러리 입니다.

## Installation

1. git을 설치하신 다음 git clone 명령어를 사용하여 customized konlpy를 내려 받으세요.
2. 설치한 폴더에 들어가 python 명령어를 이용하여 customized konlpy를 설치하세요.
3. 설치가 완료되면 git clone 명령어를 사용하여 ATS를 내려 받으세요.

```bash
git clone http://10.177.234.36:9080/research/customized_konlpy.git
cd customized_konlpy
python setup.py install
git clone http://10.177.234.36:9080/research/ats.git
```

## 정제 및 토큰화 기능 사용법
텍스트 데이터에 대한 정제 및 토큰화 기능이 있습니다.
```python
# 사용하지 않은 아스키코드 치환
from ats.TextPreprocessing import ascii_check
print(ascii_check('ＳＳＧＰＡＹ')) #SSGPAY

# (주)는 주식회사로 치환
from ats.TextPreprocessing import corporatebody
printcorporatebody('(주) 닉컴퍼니')) #주식회사 닉컴퍼니

# 특수문자 제거
from ats.TextPreprocessing import remove_specialchar
print(remove_specialchar('우리카드결제-00')) #우리카드결제 00

# 숫자는 숫자라는 단어로 치환 (자릿수에 상관없이 “숫자”로 치환)
from ats.TextPreprocessing import numbers_check
print(numbers_check('현대라 02-048')) #현대라 숫자 - 숫자

# 빈셀은 공백이란 단어로 치환
from ats.TextPreprocessing import find_null
print(find_null('')) #공백

# 전처리 결과 빈셀이면 공백이란 단어로 치환
from ats.TextPreprocessing import space_delete
print(space_delete('')) #공백

# 사람이름 인식 후 이름이라는 단어로 치환
from ats.TextPreprocessing import Nickonlpy
>>>>>>> abffb8fb6b27d2010e92367efc422c4a2737b521
nk = Nickonlpy()
print(nk.name_check('신한최승언')) #신한 이름

# 토큰화
<<<<<<< HEAD
from ats_module.TextPreprocessing import Nickonlpy
=======
from ats.TextPreprocessing import Nickonlpy
>>>>>>> abffb8fb6b27d2010e92367efc422c4a2737b521
nk = Nickonlpy()
print(nk.predict_tokennize('마이신한포인트')) #마이신한 포인트

```

<<<<<<< HEAD
## Tagging 사용법
적요 텍스트에 대한 금융 카테고리를 Tagging해 줍니다.
딥러닝 기반의 multiple classification 모델로 만들었고, CNN과 LSTM 2가지 버젼이 있습니다.
```python
# 자모
# from ats_module.TextTagging import NicJamoTagging
=======
## 태깅 모델 사용법
적요 텍스트에 대한 금융 카테고리를 태깅해 줍니다.
태깅은 딥러닝 기반의 multiple classification 모델로 만들었고, CNN과 LSTM 2가지 버젼이 있습니다.
```python
# 자모
# from ats.TextTagging import NicJamoTagging
>>>>>>> abffb8fb6b27d2010e92367efc422c4a2737b521
# njt = NicJamoTagging()
# data = njt.text_to_sequences('신한최승언')
# njt.text_tagging(data, '입금') #('소득', '급여')

# 워드
<<<<<<< HEAD
from ats_module.TextPreprocessing import Nickonlpy
nk = Nickonlpy()
data = nk.predict_tokennize('신한최승언') #신한 최승언

from ats_module.TextTagging import NicWordTagging
=======
from ats.TextPreprocessing import Nickonlpy
nk = Nickonlpy()
data = nk.predict_tokennize('신한최승언') #신한 최승언

from ats.TextTagging import NicWordTagging
>>>>>>> abffb8fb6b27d2010e92367efc422c4a2737b521
nwt = NicWordTagging()
nwt.text_tagging(data, '입금') #('대인거래', '개인입금')

```

<<<<<<< HEAD
## 정보

최승언 – [@velog](https://velog.io/@csu5216) – csu5216@gmail.com

라이센스: None

=======


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
GNU General Public License v3.0
>>>>>>> abffb8fb6b27d2010e92367efc422c4a2737b521
