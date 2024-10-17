# 📦 ats_module
> ats_module은 금융 적요 서비스를 위한 전처리 및 태깅 기능 라이브러리입니다.
<p align="center">
  <img src="./png/image.png" width="600">
</p>
<br>
<br>
## 📥 설치 방법
1. [ats_ckonlpy](https://github.com/whfh3900/ats_ckonlpy) 을 참고하여 설치.<br>
2. 다음 패키지를 pip로 설치합니다:
   - `tensorflow-gpu==2.10.0`<br>
   - `pandas==1.2.4`<br>
   - `numpy==1.21.4`<br>
3. 저장소를 클론합니다:
   ```bash
   git clone https://github.com/whfh3900/ats_module.git
   ```
<br>
<br>
## 🛠️ Preprocessing 사용법

``` python
# 사용하지 않은 아스키코드 치환
from ats_module.TextPreprocessing import ascii_check
print(ascii_check('ＳＳＧＰＡＹ'))  # SSGPAY

# (주)는 주식회사로 치환
from ats_module.TextPreprocessing import corporatebody
print(corporatebody('(주) 닉컴퍼니'))  # 주식회사 닉컴퍼니

# 특수문자 제거
from ats_module.TextPreprocessing import remove_specialchar
print(remove_specialchar('우리카드결제-00'))  # 우리카드결제 00

# 숫자는 숫자라는 단어로 치환
from ats_module.TextPreprocessing import numbers_check
print(numbers_check('현대라 02-048'))  # 현대라 숫자 - 숫자

# 빈셀은 공백이란 단어로 치환
from ats_module.TextPreprocessing import find_null
print(find_null(''))  # 공백

# 전처리 결과 빈셀이면 공백이란 단어로 치환
from ats_module.TextPreprocessing import space_delete
print(space_delete(''))  # 공백

# 사람이름 제거
from ats_module.TextPreprocessing import Nickonlpy
nk = Nickonlpy()
print(nk.name_check('신한최승언'))  # 신한

# 토큰화
from ats_module.TextPreprocessing import Nickonlpy
nk = Nickonlpy()
print(nk.predict_tokennize('마이신한포인트'))  # 마이신한 포인트
```
<br>
<br>
## 🏷️ Tagging 사용법
적요 텍스트에 대한 금융 카테고리를 Tagging해 줍니다.
딥러닝 기반의 multiple classification 모델로 만들었고, CNN과 LSTM 2가지 버젼이 있습니다.

``` python
from ats_module.TextPreprocessing import Nickonlpy
nk = Nickonlpy()
data = nk.predict_tokennize('신한최승언') #신한 최승언

from ats_module.TextTagging import NicWordTagging
nwt = NicWordTagging()
nwt.text_tagging(data, '입금') #('대인거래', '개인입금')
```
<br>
<br>
## ℹ️ 정보
라이센스: None
