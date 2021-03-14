from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.wallet import Wallet
from app.models.transaction import Transaction
from app.models.transactionNEW import TransactionDetail, TransactionHeader
from app.models.category import Category

server = create_app()

@server.shell_context_processor
def make_shell_context():
    """
    Required by Flask: register all database odbjects.
    """
    return dict(
        db=db,
        User=User,
        Transaction=Transaction,
        Category=Category,
        TransactionDetail=TransactionDetail,
        TransactionHeader=TransactionHeader,
        Wallet=Wallet
    )


if __name__ == "__main__":
    server.run(debug=True) # use_reloader=False
