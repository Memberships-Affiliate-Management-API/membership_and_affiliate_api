import os
from config import config_instance
from main import create_app
from utils.utils import is_development

app = create_app(config_class=config_instance)
debug = is_development() and config_instance.DEBUG
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if is_development():
        app.run(debug=debug, use_reloader=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8081)))
    else:
        # TODO Run the app on production server
        pass
