def index():
    redirect(URL('view'))


def view():
    userdict = {}
    userrows = db(db.auth_user).select()
    for x in userrows:
        userdict[x.id] = x.first_name + " " + x.last_name
    rows = db(db.products.product_status == 'available').select(orderby = ~ db.products.id)
    return locals()


@auth.requires_membership('Poster_use_group')
@auth.requires_login()
def post():
    response.flash = T('Welcome to Poster_use_group')
    profilerows = db(db.profile.created_by == session.auth.user.id).select(orderby = ~ db.profile.id)
    for x in profilerows: # ..acces rapid
        db.products.farm_name.default = x.farm_name
        db.products.farm_address.default = x.farm_address
        db.products.farm_website.default = x.farm_website
        break;
    form = SQLFORM(db.products).process()
    return locals()


@auth.requires_login()
def myposts():
    rows = db(db.products.created_by == session.auth.user.id).select(orderby = db.products.product_status | ~ db.products.id)
    return locals()


@auth.requires_membership('Poster_use_group')
@auth.requires_login()
def update():
    isValid = False
    row = db(db.products.id == request.args(0)).select()
    for x in row:
        if x.created_by == session.auth.user.id:
            isValid = True
    if isValid:
        record = db.products(request.args(0)) or redirect(URL('view'))
        form = SQLFORM(db.products, record)
        if form.process().accepted:
            response.flash = T('Successfully updated')
        else:
            response.flash = T('Please insert info')
    return locals()


@auth.requires_login()
def processing():
    prodDict = {}
    productRows = db(db.products).select()
    for x in productRows:
        prodDict[x.id] = x.product_name
    date_ordered = str(request.now.year) + "-" + str(request.now.month) + "-" + str(request.now.day)
    quantity = request.vars.quantity
    productId = request.vars.productId
    product_name = request.vars.product_name
    user_ID = session.auth.user.id
    sql = "Insert into online_orders (productId, user_ID, quantity, status, date_ordered) values"
    sql = sql + "(" + str(productId) + ", " + str(user_ID) + ", " + str(quantity) + ", 'cart', '" + str(date_ordered) + "')"
    r = db.executesql(sql)
    rows = db(db.online_orders.user_ID == session.auth.user.id).select(orderby = ~ db.online_orders.id)
    return locals()

