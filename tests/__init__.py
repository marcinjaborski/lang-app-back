import pytest
from website import create_app, db, User, Note


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres:admin@localhost/noteo_test',
    })
    with app.app_context():
        db.create_all()
        populate_database()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def populate_database():
    user = User()
    user.username = 'johndoe'
    user.email = 'john.doe@example.com'
    user.password = 'qwerty123'
    db.session.add(user)
    user = User.query.filter_by(username=user.username).first()

    note = Note()
    note.title = 'John note'
    note.content = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras vitae porta nibh. Cras diam diam, ' \
                   'consectetur non lorem id, tempus hendrerit nibh. Integer faucibus augue nec lectus imperdiet ' \
                   'ullamcorper. Duis sit amet ante tellus. In sodales diam a libero fermentum lobortis. Pellentesque' \
                   ' cursus blandit eleifend.'
    note.user_id = user.id
    db.session.add(note)

    db.session.commit()
