from ....account.models import User
import json


def test_user_by_email(db, client_query):
    user = User.objects.create(
        email="test@user.pl",
        password="qwerty",
        first_name="test_name",
        last_name="test_lastname",
        is_staff=False,
        is_active=True
    )

    response = client_query(
        """
        query myuser($email: String!){
            user(email: $email){
                id
                email
                password
                firstName
                lastName
                isSuperuser
                isStaff
                isActive
            }    
        }
        """,
        variables={'email': 'test@user.pl'}
    )
    content = json.loads(response.content)

    user_response = content['data']['user']

    assert user_response['id'] == str(user.id)
    assert user_response['email'] == user.email
    assert user_response['password'] == user.password
    assert user_response['firstName'] == user.first_name
    assert user_response['lastName'] == user.last_name
    assert user_response['isSuperuser'] == user.is_superuser
    assert user_response['isStaff'] == user.is_staff
    assert user_response['isActive'] == user.is_active


def test_users(db, staff_query):
    user_1 = User.objects.create(
        email="test1@user.pl",
        password="qwerty1",
        first_name="test_name_1",
        last_name="test_lastname_1",
        is_staff=False,
        is_active=True
    )

    user_2 = User.objects.create(
        email="test2@user.pl",
        password="qwerty2",
        first_name="test_name_2",
        last_name="test_lastname_2",
        is_staff=False,
        is_active=True
    )

    response = staff_query(
        """
        query myusers{
            users{
                id
                email
                password
                firstName
                lastName
                isSuperuser
                isStaff
                isActive
            }    
        }
        """,
        variables={'email': 'test@user.pl'}
    )
    content = json.loads(response.content)

    user_response = content['data']['users']

    assert user_response[0]['id'] == str(user_1.id)
    assert user_response[0]['email'] == user_1.email
    assert user_response[0]['password'] == user_1.password
    assert user_response[0]['firstName'] == user_1.first_name
    assert user_response[0]['lastName'] == user_1.last_name
    assert user_response[0]['isSuperuser'] == user_1.is_superuser
    assert user_response[0]['isStaff'] == user_1.is_staff
    assert user_response[0]['isActive'] == user_1.is_active
    assert user_response[1]['id'] == str(user_2.id)
    assert user_response[1]['email'] == user_2.email
    assert user_response[1]['password'] == user_2.password
    assert user_response[1]['firstName'] == user_2.first_name
    assert user_response[1]['lastName'] == user_2.last_name
    assert user_response[1]['isSuperuser'] == user_2.is_superuser
    assert user_response[1]['isStaff'] == user_2.is_staff
    assert user_response[1]['isActive'] == user_2.is_active
