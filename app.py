from flask import Flask, render_template, url_for, request
from main import productCompare
from pymongo import MongoClient
import pymongo




app = Flask(__name__)

client = MongoClient('localhost', 27017)
print('connection successful')
db = client.compare_db_3
compare_col = db.compare_col

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        product = request.form.get("search_box")
        print(product)
        pc = productCompare(product)
        amazon= pc.compare()
        print('amazon', amazon)
        compare_col.insert_many(amazon)
        count = 0
        b= db.compare_col.find().sort([("num_rating", pymongo.DESCENDING),( "ratings",pymongo.DESCENDING), ("price",pymongo.ASCENDING)]).limit(1)
        for i in b:    
            if count == 1:
                break
            brand = i['product_link']
            count = count+1
        p_l = brand
    else:
        p_l = ''
        
    return render_template('home.html', link = p_l)
               

@app.route('/about/')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
    client.close()
    print('connection closed')