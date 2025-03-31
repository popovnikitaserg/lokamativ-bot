from create_bot import managers_id, admins
def check(user_id):
    if user_id in managers_id:
        role = "manager"
    elif user_id in admins:
        role = "admin"
    return role