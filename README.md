# 개요
질문 앱

# 프로젝트 구성
- 유저(User)
- 질문(Question)
- 댓글(Comment)
- 좋아요(Nice)
- 코어(Core)

# 전체 구성
- app 폴더하에 config(project 폴더), core, questions, users(각각 앱 폴더) 있음.
- questions 폴더에 Question, Comment, Nice 앱 있음.

# 명령어
- 터미널에서 docker-compose build . (점까지 찍어야 함)로 빌드
- docker-compose build
- docker-compose up $\leftarrow$ 이 명령어로 migrate까지 실행
- 이후 한 번 Ctrl+C로 빠져나옴.

## 단위테스트 방법
- docker-compose run --rm app sh -c "pytest ."

## 슈퍼유저 작성
- docker-compose run --rm app sh -c "python manage.py createsuperuser"

# 필수 기능
- 질문을 DB에 저장, 수정, 삭제
- 질문의 댓글 저장
- 질문의 댓글 목록 출력
- 키워드로 질문의 제목 또는 본문내용 검색
- 질문 작성일 기준 각 월별 전체 질문 중에서 가장 좋아요가 많은 질문 목록 출력

---
## DB명세

### User Signup
- URL   
`/users/signup/`
- Method   
`GET`
- URL Params   
없음
- Request Header   
없음
- Sample Call:
> curl -X POST "http://127.0.0.1:8000/users/signup/" -H "Content-Type: application/json" -d '{"email":"admin5@admin.com","name":"admin5","password":"admin1234"}'
- Success Response
> Code 200   
> Content {"id":1,"email":"admin5@admin.com","name":"admin5"}
- Error Response
> Code 401 UNAUTHORIZED
> Content { error : "You are unauthorized to make this request."}
---
### User Token 발급
- URL   
`/api/token/`
- Method
`POST`
- URL Params   
없음
- Request Header   
없음
- Sample Call:
> curl -X POST "http://127.0.0.1:8000/api/token/" -H "Content-Type: application/json" -d '{"name":"admin5","password":"admin1234"}'
- Success Response
> Code 200
> Content {"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluNSIsImV4cCI6MTYzNTQ4Mzg1NiwiZW1haWwiOiJhZG1pbjVAYWRtaW4uY29tIiwibmFtZSI6ImFkbWluNSIsIm9yaWdfaWF0IjoxNjM1NDgzMjU2fQ.v4O490NDHXGFgRGmkjpsy7Usp77uMTLquPP8PUp6aFE"}
- Error Response
> Code 401 UNAUTHORIZED
> Content { error : "You are unauthorized to make this request."}
---
### User Token Refresh
- URL   
`/api/token/refresh/`
- Method
`POST`
- URL Params   
없음
- Request Header   
없음
- Sample Call:
> curl -X POST "http://127.0.0.1:8000/api/token/refresh/" -H "Content-Type: application/json" -d '{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluNSIsImV4cCI6MTYzNTQ4Mzg1NiwiZW1haWwiOiJhZG1pbjVAYWRtaW4uY29tIiwibmFtZSI6ImFkbWluNSIsIm9yaWdfaWF0IjoxNjM1NDgzMjU2fQ.v4O490NDHXGFgRGmkjpsy7Usp77uMTLquPP8PUp6aFE"}'
- Success Response
> code 200
> {"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluNSIsImV4cCI6MTYzNTQ4NDAzOSwiZW1haWwiOiJhZG1pbjVAYWRtaW4uY29tIiwibmFtZSI6ImFkbWluNSIsIm9yaWdfaWF0IjoxNjM1NDgzMjU2fQ.DWEkyYCS5yPB9Nt-6Cw7giJMZ6Xk86s8EhOhD7aourw"}
---
### Show Question
- URL   
`/questions/`
- Method
`GET`
- URL Params   
없음
- Request Header   
Authorization: Barer {access token]
- Sample Call:
> curl -X GET "http://127.0.0.1:8000/questions/" -H "Content-Type: application/json" -H "Authorization: Baerer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluNSIsImV4cCI6MTYzNTQ4NDAzOSwiZW1haWwiOiJhZG1pbjVAYWRtaW4uY29tIiwibmFtZSI6ImFkbWluNSIsIm9yaWdfaWF0IjoxNjM1NDgzMjU2fQ.DWEkyYCS5yPB9Nt-6Cw7giJMZ6Xk86s8EhOhD7aourw"
-Success Response
> code 200
> [{"id":1,"created_at":"2021-10-29T05:00:41.598447","title":"Test Question","text":"Question!!","nice_count":0,"author":1}]
---
### Show Question
- URL   
`/questions/:id`
- Method
`GET`
- URL Params
없음
- Request Header   
Authorization: Barer {access token]
- Sample Call:
> curl -X GET "http://127.0.0.1:8000/questions/1/" -H "Content-Type: application/json" -H "Authorization: Baerer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluNSIsImV4cCI6MTYzNTQ4NDAzOSwiZW1haWwiOiJhZG1pbjVAYWRtaW4uY29tIiwibmFtZSI6ImFkbWluNSIsIm9yaWdfaWF0IjoxNjM1NDgzMjU2fQ.DWEkyYCS5yPB9Nt-6Cw7giJMZ6Xk86s8EhOhD7aourw"
-Success Response
> code 200
> {"id":1,"created_at":"2021-10-29T05:00:41.598447","title":"Test Question","text":"Question!!","nice_count":0,"author":1}
---
### Create Question
- URL   
`/questions/`
- Method
`POST`
- URL Params
없음
- Request Header   
Authorization: Barer {access token]
- Sample Call:
> curl -X POST "http://127.0.0.1:8000/questions/" -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluMyIsImV4cCI6MTYzNTQ4NTUwOSwiZW1haWwiOiJhZG1pbjNAYWRtaW4uY29tIiwibmFtZSI6ImFkbWluMyIsIm9yaWdfaWF0IjoxNjM1NDg0OTA5fQ.e_nhGZHmf_61CNrAqlfGZjpOawWz0_Jo3FqCu4jUDqU" -d '{"title":"Hey!Whats up?","text":"I want to eat something"}'
-Success Response
> code 201
> {"id":3,"created_at":"2021-10-29T05:25:14.565618","title":"Hey!Whats up?","text":"I want to eat something","nice_count":0,"author":1}
---
### Edit question
- URL   
`/questions/3/`
- Method
`POST`
- URL Params
없음
- Request Header   
Authorization: Barer {access token]
- Sample Call:
> curl -X PUT "http://127.0.0.1:8000/questions/3/" -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluMyIsImV4cCI6MTYzNTQ4NTUwOSwiZW1haWwiOiJhZG1pbjNAYWRtaW4uY29tIiwibmFtZSI6ImFkbWluMyIsIm9yaWdfaWF0IjoxNjM1NDg0OTA5fQ.e_nhGZHmf_61CNrAqlfGZjpOawWz0_Jo3FqCu4jUDqU" -d '{"title":"Can i edit this?","text":"Oh it is edited"}'
-Success Response
> code 200
> {"id":3,"created_at":"2021-10-29T05:25:14.565618","title":"Can i edit this?","text":"Oh it is edited","nice_count":0,"author":1}
---
### Delete question
- URL   
`/questions/3/`
- Method
`PUT`
- URL Params
없음
- Request Header   
Authorization: Barer {access token]
- Sample Call:
> curl -X DELETE "http://127.0.0.1:8000/questions/3/" -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluMyIsImV4cCI6MTYzNTQ4NTUwOSwiZW1haWwiOiJhZG1pbjNAYWRtaW4uY29tIiwibmFtZSI6ImFkbWluMyIsIm9yaWdfaWF0IjoxNjM1NDg0OTA5fQ.e_nhGZHmf_61CNrAqlfGZjpOawWz0_Jo3FqCu4jUDqU"
-Success Response
> code 204
---
### Create a Comment for a Question
- URL   
`/questions/1/add-comment/`
- Method
`POST`
- URL Params
없음
- Request Header   
Authorization: Barer {access token]
- Sample Call:
> curl -X POST "http://127.0.0.1:8000/questions/1/add-comment/" -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluMyIsImV4cCI6MTYzNTQ4NjA5MCwiZW1haWwiOiJhZG1pbjNAYWRtaW4uY29tIiwibmFtZSI6ImFkbWluMyIsIm9yaWdfaWF0IjoxNjM1NDg1NDkwfQ.eI3cURh47pRShB6kr_vbthkq1NeCx6VcVzUPglxt3Vs" -d '{"text":"this is my first comment"}'
-Success Response
> code 200
> {"id":2,"created_at":"2021-10-29T05:33:46.076685","text":"this is my first comment","author":1,"question":1,"parent_comment":null}
---
### Show all comments for a question
- URL   
`/questions/1/comments/`
- Method
`GET`
- URL Params
없음
- Request Header   
Authorization: Barer {access token]
- Sample Call:
> curl -X GET "http://127.0.0.1:8000/questions/1/comments/" -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluMyIsImV4cCI6MTYzNTQ4NjA5MCwiZW1haWwiOiJhZG1pbjNAYWRtaW4uY29tIiwibmFtZSI6ImFkbWluMyIsIm9yaWdfaWF0IjoxNjM1NDg1NDkwfQ.eI3cURh47pRShB6kr_vbthkq1NeCx6VcVzUPglxt3Vs"
-Success Response
> code 200
> [{"id":1,"created_at":"2021-10-29T05:32:22.575178","text":"안녕하세요!","author":1,"question":1,"parent_comment":null},{"id":2,"created_at":"2021-10-29T05:33:46.076685","text":"this is my first comment","author":1,"question":1,"parent_comment":null}]
---
### Search Questions that own title or text contains keyword
- URL   
`/questions/?keyword=`
- Method
`GET`
- URL Params
`keyword`
- Request Header   
Authorization: Barer {access token]
- Sample Call:
> curl -X GET "http://127.0.0.1:8000/questions/?keyword=<span style="color:red">Quest</span>" -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluMyIsImV4cCI6MTYzNTQ4NjA5MCwiZW1haWwiOiJhZG1pbjNAYWRtaW4uY29tIiwibmFtZSI6ImFkbWluMyIsIm9yaWdfaWF0IjoxNjM1NDg1NDkwfQ.eI3cURh47pRShB6kr_vbthkq1NeCx6VcVzUPglxt3Vs"

-Success Response
> code 200
> [{"id":1,"created_at":"2021-10-29T05:21:08.748804","title":"Test <span style="color:red">Quest</span>ion","text":"Hey!","nice_count":0,"author":1}
---
### Outputs a list of the most liked questions for each month, based on the question creation date.
- URL   
`/questions/most-voted`
- Method
`GET`
- URL Params   
`from_year` 몇년도부터 검색할지
`from_month` 몇월부터 검색할지
`to_year` 몇년도까지 검색할지
`to_month` 몇월까지 검색할지   
`from year`와 `from month`, `to_year`와 `to_month`는 각각 세트로 입력만 받음.   
없을 시 전체 기간에서 검색.
- Request Header   
Authorization: Barer {access token]
- Sample Call:
> curl -X GET "http://127.0.0.1:8000/questions/most-voted/" -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluMyIsImV4cCI6MTYzNTQ4Njk2OCwiZW1haWwiOiJhZG1pbjNAYWRtaW4uY29tIiwibmFtZSI6ImFkbWluMyIsIm9yaWdfaWF0IjoxNjM1NDg2MzY4fQ.yrUN8W0vMc8rUi7pnvTbCX4S3VqrS7HsocCNVsrUeWQ"

-Success Response
> code 200
> [{"id":1,"created_at":"2021-10-29T05:21:08.748804","title":"Test Question","text":"Hey!","nice_count":0,"author":1}]