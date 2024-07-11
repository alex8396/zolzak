
MySQL 설치 후
cmd 실행
1. mysql -u root -p sys 입력 후 본인이 설정한 비밀번호 입력
2. create database `movie-parser`
3. exit

cmd 상에서 cd -> zolzak 디렉터리 (python 설치 되어있어야함)
1. pip install poetry
2. poetry install
3. poetry shell
4. cd movieroot
5. python manage.py makemigrations
6. python mange.py migrate
7. python manage.py init_tmdb (영화 정보 DB에 채우는 명령어)
8. python manage.py createsuperuser (Name: admin, Password: 1234 입력 후 Y)
9. python manage.py runserver


위에서 만든 superuser로
http://127.0.0.1:8000/admin에서 DB 확인 가능

API Docs
-> https://documenter.getpostman.com/view/35020233/2sA3JT3yWx#intro