import os
from config import Config
from main import create_app
from utils.utils import is_development

api = create_app(config_class=Config)
debug = is_development() and Config.DEBUG
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    api.run(debug=debug, use_reloader=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8081)))
