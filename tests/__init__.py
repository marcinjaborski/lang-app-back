import pytest
from website import create_app, db, User


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres:admin@localhost/noteo_test',
    })
    with app.app_context():
        db.create_all()
        user = User()
        user.username = 'johndoe'
        user.email = 'john.doe@example.com'
        user.password = 'qwerty123'
        db.session.add(user)
        db.session.commit()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
