import dash
from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required

from flask import render_template_string

from config import BaseConfig


def create_app():
    server = Flask(__name__)
    server.config.from_object(BaseConfig)

    register_extensions(server)
    register_blueprints(server)
    register_dashapps(server)

    return server


def _get_index_string(template):
    """
    Replace the following 'commented-out' placeholders in my 'dash.html' 
    Flask template with the placeholders that Dash requires, for modifying the 
    'index_string' of the dash app
    """
    template = template.replace(r'<!-- %metas% -->', r'{%metas%}')
    template = template.replace(r'<!-- %title% -->', r'{%title%}')
    template = template.replace(r'<!-- %favicon% -->', r'{%favicon%}')
    template = template.replace(r'<!-- %css% -->', r'{%css%}')
    template = template.replace(r'<!-- %app_entry% -->', r'{%app_entry%}')
    template = template.replace(r'<!-- %config% -->', r'{%config%}')
    template = template.replace(r'<!-- %scripts% -->', r'{%scripts%}')
    template = template.replace(r'<!-- %renderer% -->', r'{%renderer%}')

    return template


# def register_dashapps(app):
#     from app.dashapp1.layout import layout
#     from app.dashapp1.callbacks import register_callbacks

#     # Meta tags for viewport responsiveness
#     meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

#     dashapp1 = dash.Dash(__name__,
#                          server=app,
#                          url_base_pathname='/dashboard/',
#                          assets_folder=get_root_path(__name__) + '/dashboard/assets/',
#                          meta_tags=[meta_viewport])

#     with app.app_context():
#         dashapp1.title = 'Dashapp 1'
#         dashapp1.layout = layout
#         register_callbacks(dashapp1)

#     _protect_dashviews(dashapp1)


def register_dashapps(app):
    """
    Register Dash apps with the Flask app
    """

    from app.dashapp1.layout import layout
    from app.dashapp1.callbacks import register_callbacks

    # Meta tags for viewport responsiveness
    meta_viewport = {
        "name": "viewport", 
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no"
    }

    dashapp1 = dash.Dash(__name__,
        server=app,
        url_base_pathname='/dash/',
        assets_folder=get_root_path(__name__) + '/assets/',
        meta_tags=[meta_viewport], 
    )

    with app.app_context():
        # Render my Flask template to get a special 'index_string' for the Dash app
        path = get_root_path(__name__) + "/templates/dash.html"
        with open(path, 'r') as f:
            template_string = render_template_string(f.read())
        index_string = _get_index_string(template_string)
        dashapp1.index_string = index_string

        dashapp1.title = 'CHANGING THE LANDSCAPE'
        dashapp1.layout = layout
        register_callbacks(dashapp1)

    _protect_dashviews(dashapp1)

    return app


def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])


def register_extensions(server):
    from app.extensions import db
    from app.extensions import login
    from app.extensions import migrate

    db.init_app(server)

    with server.app_context():
        db.create_all()

    login.init_app(server)
    login.login_view = 'main.login'
    migrate.init_app(server, db)


def register_blueprints(server):
    from app.webapp import server_bp

    server.register_blueprint(server_bp)
