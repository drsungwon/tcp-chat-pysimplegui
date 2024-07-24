<h2>실행 방법</h2>	

프로젝트를 다운로드 함

폴더안에서 poetry shell를 실행함<br />
> poetry shell

폴더안에서 필요한 패키지를 설치함<br />
> poetry install

src/client/client.py를 실행하여 채팅 client #1을 실행함<br />
> poetry run python client.py

src/client/client.py를 실행하여 채팅 client #2를 실행함<br />
> poetry run python client.py

src/server/server.py를 실행하여 채팅 서버를 실행함<br />
> python server.py

Client #1의 Chatting ID에 사용자 식별자(ID)를 입력하고,<br />
Client #1의 CONNECT 버튼을 클릭해서 채팅 서버에 접속함

Client #2의 Chatting ID에 사용자 식별자(ID)를 입력하고,<br />
Client #2의 CONNECT 버튼을 클릭해서 채팅 서버에 접속함

Client #1과 Client #2의 Chatting 화면에 글자를 입력하고, SEND 버튼을 클릭함

Client #1과 Client #2의 DISCONNECT 버튼을 클릭하여, 채팅 서버에서 접속을 해제함

Client #1과 Client #2의 EXIT 버튼을 클릭하여, 채팅을 종료함

채팅 서버에 quit 명령을 입력하여 실행을 중지함

Poetry 실행을 중지함<br />
> exit

<h2>실행 화면</h2>	

![Chatting Client #1](/screen/client-1.png)

![Chatting Client #2](/screen/client-2.png)

![Chatting Server](/screen/server.png)
