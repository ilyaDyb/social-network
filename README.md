This is my social-network something like facebook or VK, but have less functions because i'm writing the code alone.
If you want to start project:
1. Create workdir and write: <b>git clone https://github.com/ilyaDyb/social-network.git</b>
2. Then: <b style="text-decoration: underline;">cd social-network/</b> and <span style="text-decoration: underline">docker-compose up</span>
3. !!! By default, when containers start, fixtures are loaded automatically. To skip loading fixtures, change the value of the `LOAD_FIXTURES` variable in the `.env` file:
    ```env
    LOAD_FIXTURES=0
    ```
But you won’t be able to see all the beauty of the application without test users without any activities (created posts, changed the avatar, etc.)
If you load fixtures then you can login how username: test3, password: qwertyuiop2014

And i don't add automatically start celery with redis, you should to use this commands in diffirent consoles:

1. `celery -A application worker -P solo --loglevel=INFO `
2. `celery -A application beat -l info`

<b>WARNING!</b>
If you got some exception with loading fixtures write this in bash in the container:
```
python3 manage.py flush
python3 manage.py loaddata fixtures/fixture_db.json
```
<b>But it would be better if you installed everything using bash rather than docker-compose because it requires some work.</b>

If you are a recruiter and you are interested in me along with my project, please call or write, I can show all the functionality and explain why I used something here or somewhere else.
My contacts:
1. Phone number: <b>+79170760362</b>
2. TG: http://t.me/wicki7
3. Mail: ilya77788899@mail.ru
