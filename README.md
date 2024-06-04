This is my pet-project.
If you want to start it:
1. git clone https://github.com/ilyaDyb/social-network.git (in your folder)
2. Install and activate your env
3. Then write: pip install -r requirements.txt
4. You should to change database's settings for your database (preferably not sqlite3)
5. python3 manage.py migrate
6. You should use python-dotenv for token (pip install python-dotenv, then .env: REPLICATE_API_TOKEN=<paste-your-token-here>). (You can get it after authorization on https://replicate.com/)
7. Then you can use full functional in the application
python3 manage.py runserver
______________________________________________________
