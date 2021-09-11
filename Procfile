web: gunicorn run:app
cron: python cron.py
heroku ps:scale web=2 cron=1