def index(): return dict(message="hello from profile.py")


@auth.requires_login()
def save():
    profilerows = db(db.profile.created_by == session.auth.user.id).select(orderby = ~ db.profile.id)
    user_ID = session.auth.user.id


    for x in profilerows:
        user_ID = session.auth.user.id
        db.profile.user_name.default = x.user_name
        db.profile.email.default = x.email
        db.profile.password.default = x.password
        db.profile.data_account_created.default = x.data_account_created
        db.profile.user_image.default = x.user_image
        db.profile.nickname.default = x.nickname
        db.profile.user_role.default = x.user_role
        db.profile.farm_name.default = x.farm_name
        db.profile.farm_address.default = x.farm_address
        db.profile.farm_website.default = x.farm_website
        break;

    form=SQLFORM(db.profile).process()
    return locals()



def view():
    rows = db(db.profile.created_by == auth.user.id).select(orderby = ~ db.profile.id)
    return locals()
