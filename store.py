from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

connection = pymysql.connect(host = 'sql11.freesqldatabase.com',
                             user = 'sql11189255',
                             password = 'uLGuLSYBZP',
                             db = 'sql11189255',
                             charset = 'utf8',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

@get("/admin")
def admin_portal():
    return template("pages/admin.html")

@get("/")
def index():
    return template("index.html")

@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')

@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')

@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')

@post ("/category")
def create_category():
    try:
        with connection.cursor() as cursor:
            name = request.POST.get("name")
            sql = "INSERT INTO categories VALUES (0,'{}')".format(name)
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "MSG": result, "CODE": "201"})
    except pymysql.err.IntegrityError:
        return json.dumps({"STATUS": "ERROR", "MSG": "category already exists", "CODE": "200"})
    except pymysql.err.InternalError:
        return json.dump({"STATUS": "ERROR", "MSG": "The category was not created due to an error", "CODE":"500" })

@delete("/category/<id>")
def delete_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM categories WHERE id = {}".format(id)
            cursor.execute(sql)
            return json.dumps({"STATUS": "SUCCESS", "MSG": "The category was deleted successfully", "CODE": "200"})
    except:
        return json.dumps({"STATUS": "ERROR", "MSG": "The category was not deleted due to an error", "CODE": "500"})

@get('/categories')
def list_categories():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id, name from categories"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps ({"STATUS": "SUCCESS", "CATEGORIES": result, "CODE":"200"})
    except:
        return json.dumps({"STATUS": "ERROR", "MSG": "internal error", "CODE": "500"})

@post("/product")
def add_product():
    try:
        with connection.cursor() as cursor:
            # ID was generated and auto-incremented in the SQL generation
            t = request.POST.get("title")
            d = request.POST.get("desc")
            p = request.POST.get("price")
            i = request.POST.get("img_url")
            c = request.POST.get("category")
            f = request.POST.get("favorite")
            # converting favorite's on \ off into boolean
            if f is "on":
                f = True
            else:
                f = False
            sql = "INSERT INTO products values (id,'{}','{}','{}','{}','{}',{})".format(t,d,p,i,c,f)
            cursor.execute(sql)
    except Exception as e:
        try:
            with connection.cursor() as cursor:
                t = request.POST.get("title")
                d = request.POST.get("desc")
                p = request.POST.get("price")
                i = request.POST.get("img_url")
                c = request.POST.get("category")
                f = request.POST.get("favorite")
                if f is "on":
                    f = True
                else:
                    f = False
                sql2 = "UPDATE products SET descrpt = '{}', price= '{}', img_url= '{}', category= '{}', favorite= {} WHERE title = '{}'".format(d, p, i, c, f, t)
                cursor.execute(sql2)
        except Exception as e:
            return json.dumps({"STATUS": "ERROR", "MSG": "The product was not created/updated due to an error"})

@get ("/product/<id>")
def get_product(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * from products where id = {}".format(id)
            cursor.execute(sql)
            result = cursor.fetchone()
            return json.dumps({"STATUS": "SUCCESS", "MSG":result, "CODE":"200"})
    except:
        return json.dumps({"STATUS": "INTERNAL ERROR", "MSG": "The product was not fetched due to an error", "CODE": "500"})

@delete("/product/<id>")
def delete_product(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM products where id = {}".format(id)
            cursor.execute(sql)
            return json.dumps({"STATUS": "SUCCESS", "PRODUCTS": "The product was deleted successfully", "CODE": "200"})
    except:
        return json.dumps({"STATUS": "ERROR", "MSG": "The product was not deleted due to an error", "CODE": "500"})

@get('/products')
def list_products():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * from products"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "PRODUCTS":result, "CODE": "200"})
    except:
        return json.dumps({"STATUS": "INTERNAL ERROR", "MSG": "Internal error", "CODE": "500"})

@get('/category/<id>/products')
def list_products_by_category(id):
    try:
        with connection.cursor() as cursor:
            # favorite products displayed first
            sql = "SELECT * from products WHERE category = {} order by favorite desc, id asc".format(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "PRODUCTS": result, "CODE":"200"})
    except:
        return json.dumps({"STATUS": "INTERNAL ERROR", "MSG": "Internal error", "CODE": "500"})

run(host='127.0.0.1', port=7000)