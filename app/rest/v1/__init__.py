from flask import Blueprint

rest_v1 = Blueprint("rest_v1",
                    __name__,
                    template_folder="templates",
                    static_folder="static",
                    url_prefix='/rest/v1')

from . import view
