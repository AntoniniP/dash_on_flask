from app import create_app
from app.extensions import db
from app.models import User 

server = create_app()

@server.shell_context_processor
def make_shell_context():
    """
    Required by Flask: register all database odbjects.
    """
    return dict(
        db=db,
        User=User
    )


if __name__ == "__main__":
    server.run(debug=True)