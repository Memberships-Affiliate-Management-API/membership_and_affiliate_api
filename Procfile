web: gunicorn run:app
cron: python cron.py
tasks: python tasks.py
heroku ps:scale web=2 cron=1 tasks=1