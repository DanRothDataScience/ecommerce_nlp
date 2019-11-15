import sys
import os
import pickle
import numpy as np
from flask import Flask, request, render_template

root_dir = os.path.dirname(sys.path[0])
sys.path.append(os.path.join(root_dir, 'code'))


app = Flask(__name__)


# Loads df from pickle file
with open("data/product_df.pkl", 'rb') as openfile:
    products = pickle.load(openfile)


def find_item(search):
    query = {'packers': 1,
             'coffee grinder': 3,
             'laptop case': 4,
             'lego': 12,
             'playstation': 13,
             'perfume': 14,
             'yoga pants': 22,
             'bedding': 30,
             'dresses': 31,
             'furniture': 32,
             'sports bra': 33}
    try:
        topic = int(search)
    except:
        topic = query[search]
    sort = 'topic' + str(topic)
    select = products[products.topic_label == topic].dropna()
    try:
        select['topic_ratio'] = select[sort] / select.score_sum
        out = select.sort_values('topic_ratio', ascending=False)[:3]
        status=True
    except:
        out = 0
        status = False
    return out, status


@app.route("/", methods=["POST", "GET"])
def index():
    '''
    Gathers input from user and displays results using a Flask HTML template

    Args:
        None

    Returns:
        None
    '''
    if request.method == 'POST':

        # Collects user input and uses it to get recommendations
        search = request.form.get('search')
        df, status = find_item(search)

        # True status means the recommender returns data
        if status:
            # recos = (df[['name', 'image', 'ingredients', 'url']]
            #          .to_dict(orient='records'))
            recos = (df[['product_title', 'product_image', 'source', 'product_link']]
                     .to_dict(orient='records'))
        else:
            recos = None
    else:
        search = recos = None

    return render_template('index.html',
                           last_search=search,
                           recos=recos)


if __name__ == '__main__':
    # print(find_item(7))
    app.run()
