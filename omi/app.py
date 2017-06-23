import logging.config

from flask import Flask, Blueprint
from werkzeug.routing import BaseConverter, ValidationError
from omi import settings
from omi.api.gateway.endpoints.recordings import ns as omi_recordings_namespace
from omi.api.gateway.endpoints.works import ns as omi_works_namespace
from omi.api.restplus import api
from omi.database import db

class MatrixConverter(BaseConverter):
    def __init__(self, url_map, **defaults):
        super(MatrixConverter, self).__init__(url_map)
        self.defaults = {k: str(v) for k, v in defaults.items()}

    def to_python(self, value):
        if not value.startswith(';'):
            raise ValidationError()
        value = value[1:]
        parts = value.split(';')
        result = self.defaults.copy()
        for part in value.split(';'):
            try:
                key, value = part.split('=')
            except ValueError:
                raise ValidationError()
            result[key.strip()] = value.strip()
        return result

    def to_url(self, value):
        return ';' + ';'.join('{}={}'.format(*item) for item in value.items())


app = Flask(__name__)
app.url_map.converters['matrix'] = MatrixConverter
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(omi_recordings_namespace)
    api.add_namespace(omi_works_namespace)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)

if __name__ == "__main__":
    main()
