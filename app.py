from flask import *
import pymongo
import string
import random
import os

main_data = "SESHU"
database = os.environ.get('DATABASE_URL')
title = os.environ.get('TITLE','Yss Projects')
logo = os.environ.get('LOGO')
myclient = pymongo.MongoClient(database)

mydb = myclient["mydatabase"]
mycol = mydb["urls"]
app = Flask(__name__)

def rando():
    res = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k = 5))
    return res

@app.route("/")
def main():
    return render_template("main.html",title=title,logo=logo)

@app.route("/api",methods=['GET'])
def api():
    url = request.args.get('url')
    if "http" in url:
        x= mycol.find_one(main_data)
        urls = x['urls']
        ids = x['ids']
        if url in urls:
            indx = urls.index(url)
            id = ids[indx]
        else:
            urls.append(url)
            id = rando()
            ids.append(id)
            up = mycol.update_one({"_id":main_data},{"$set":{"urls":urls,"ids":ids}})
        data = {"status":True,"id":id,"url":url}
    else:
        data = {"status":False,"error":"Please Enter A Valid Url"}
    resp = make_response(jsonify(data))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/<id>")
def redir(id):
    x= mycol.find_one(main_data)
    urls = x['urls']
    ids = x['ids']
    if id in ids:
        indx = ids.index(id)
        url = urls[indx]
        return redirect(url)
    else:
        return render_template("error.html",logo=logo)


if __name__ == '__main__':
    x= mycol.find_one(main_data)
    if x == None:
        data = {'ids':["create"],"urls":["https://github.com/iseshu/short-url"],"_id":main_data}
        a = mycol.insert_one(data)
        print("Data Created")
        app.run()
    else:
        print("Data Already Created")
        app.run()
