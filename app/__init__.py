"""
Registers extensions, blueprints and individual Dash apps into the Flask server.
"""

import dash
from flask import Flask
from flask import render_template_string
from flask.helpers import get_root_path
from flask_login import login_required
from codetiming import Timer

from config import BaseConfig

@Timer(text="Create app - {:0.4f}")
def create_app():
    server = Flask(__name__)
    server.config.from_object(BaseConfig)

    register_extensions(server)
    register_blueprints(server)

    from app.dashapp1.layout import layout as l_dashapp1
    from app.dashapp1.callbacks import register_callbacks as rc_dashapp1
    register_dashapp(app=server, title='Dashborard', base_pathname='dash', layout=l_dashapp1, register_callbacks=rc_dashapp1)

    from app.dash_settings.layout import layout as l_settings
    from app.dash_settings.callbacks import register_callbacks as rc_settings
    register_dashapp(app=server, title='Settings', base_pathname='settings', layout=l_settings, register_callbacks=rc_settings)

    return server


@Timer(text="Register dashapps - {:0.4f}")
def register_dashapp(app, title, base_pathname, layout, register_callbacks):
    # Meta tags for viewport responsiveness
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no"
    }

    dashapp1 = dash.Dash(__name__,
        server=app,
        url_base_pathname=f'/{base_pathname}/',
        assets_folder=get_root_path(__name__) + '/assets/',
        meta_tags=[meta_viewport],
    )

    dashapp1.css.config.serve_locally = True
    dashapp1.scripts.config.serve_locally = True

    with app.app_context():
        # Render my Flask template to get a special 'index_string' for the Dash app
        path = get_root_path(__name__) + "/templates/dash.html"
        with open(path, 'r') as f:
            template_string = render_template_string(f.read())
        index_string = _get_index_string(template_string)
        dashapp1.index_string = index_string

        dashapp1.title = title
        dashapp1.layout = layout
        register_callbacks(dashapp1)

    _protect_dashviews(dashapp1)

@Timer(text="Get index string - {:0.4f}")
def _get_index_string(template: str) -> str:
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
