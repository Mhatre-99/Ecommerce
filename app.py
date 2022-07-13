from flask import Flask, render_template, url_for, request
from main import productCompare



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        product = request.form.get("search_box")
        print(product)
        pc = productCompare(product)
        brand = pc.compare()
        p_l = brand
    else:
        p_l = ''
        
    return render_template('home.html', link = p_l)
               

@app.route('/about/')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)