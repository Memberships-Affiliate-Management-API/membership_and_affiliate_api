import os
from _cron.scheduler import schedule
from config import config_instance
from main import create_app
from utils.utils import is_development

app = create_app(config_class=config_instance)
scheduled_task = schedule.start()

debug = is_development() and config_instance.DEBUG
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if is_development():
        # NOTE: this is a development server
        app.run(debug=debug, use_reloader=True, host='127.0.0.1', port=int(os.environ.get('PORT', 8081)))
    else:
        app.run(debug=debug, use_reloader=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8081)))
