from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import difflib


app = Flask(__name__)
CORS(app)

class Product:
    def __init__(self, name: str, price: float, category: str, keywords: list, image: str, link: str):
        self.name = name
        self.price = price
        self.category = category
        self.image = image
        self.keywords = keywords
        self.link = link

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_category(self):
        return self.category

    def get_keywords(self):
        return self.keywords




products = [
    Product(
        "Apple Air Tag",
        20,
        "Travel",
        ["tag", "apple", "air tag", "find"],
        "https://m.media-amazon.com/images/I/713xuNx00oS._AC_SX425_.jpg",
        "https://www.amazon.com/dp/B0933BVK6T?linkCode=ssc&tag=onamzjust0cd8-20&creativeASIN=B0933BVK6T&asc_item-id=amzn1.ideas.21RWQOANTALWI&ref_=aip_sf_list_spv_ofs_mixed_d_asin"
    ),

    Product(
        "Soap Dispenser",
        16.90,
        "Kitchen",
        ["soap", "cleaning", "kitchen gadget"],
        "https://m.media-amazon.com/images/I/81oKKDQZUUL._AC_SX679_.jpg" ,
        "https://www.amazon.com/dp/B07Y45TVC2?linkCode=ssc&tag=onamzjust0cd8-20&creativeASIN=B07Y45TVC2&asc_item-id=amzn1.ideas.13IB4BP3F7I63&ref_=aip_sf_list_spv_ofs_mixed_d_asin"
    ),

    Product(
        "Soda Can Dispenser",
        24.87,
        "Kitchen",
        ["soda", "dispenser", "can", "organize"],
        "https://m.media-amazon.com/images/I/91gOVsUe5OL._AC_SX679_.jpg",
        "https://www.amazon.com/dp/B07V499VVS?linkCode=ssc&tag=onamzjust0cd8-20&creativeASIN=B07V499VVS&asc_item-id=amzn1.ideas.13IB4BP3F7I63&ref_=aip_sf_list_spv_ofs_mixed_d_asin"
    ),

    Product(
        "Cactus Toilet Plunger",
        26.89,
        "Bathroom",
        ["cactus", "toilet", "plunger", "toilet plunger", "plant", "cleaning"],
        "https://m.media-amazon.com/images/I/51YTvPdGH5L.__AC_SX300_SY300_QL70_FMwebp_.jpg",
        "https://www.amazon.com/dp/B0B85ZPNPM?linkCode=ssc&tag=onamzjust0cd8-20&creativeASIN=B0B85ZPNPM&asc_item-id=amzn1.ideas.13IB4BP3F7I63&ref_=aip_sf_list_spv_ofs_mixed_d_asin"
    ),

    Product(
        "Penguin Egg Cooker",
        21.90,
        "Kitchen",
        ["penguin", "egg", "cooker", "kitchen", "egg cooker"],
        "https://m.media-amazon.com/images/I/71cdtW2e4AL._AC_SX679_.jpg",
        "https://www.amazon.com/dp/B07WD8MF7W?linkCode=ssc&tag=onamzjust0cd8-20&creativeASIN=B07WD8MF7W&asc_item-id=amzn1.ideas.13IB4BP3F7I63&ref_=aip_sf_list_spv_ofs_mixed_d_asin"
    ),

    Product(
        "Collapsible Plastic Laundry Basket",
        10,
        "Houseware",
        ["basket", "compact", "collapsible", "laundry", "plastic"],
        "https://m.media-amazon.com/images/I/61+bJMp+8GL._AC_SX466_.jpg",
        "https://www.amazon.com/dp/B0882ZPRF7?linkCode=ssc&tag=onamzjust0cd8-20&creativeASIN=B0882ZPRF7&asc_item-id=amzn1.ideas.13IB4BP3F7I63&ref_=aip_sf_list_spv_ons_d_asin&th=1"
    ),

    Product(
        "Automatic Stirrer",
        36.95,
        "Kitchen",
        ["stirrer", "automatic", "pan stirrer", "pan", "rotating"],
        "https://m.media-amazon.com/images/I/51JW0bsGhEL._AC_SX679_.jpg",
        "https://www.amazon.com/dp/B008OWT95S?linkCode=ssc&tag=onamzjust0cd8-20&creativeASIN=B008OWT95S&asc_item-id=amzn1.ideas.13IB4BP3F7I63&ref_=aip_sf_list_spv_ofs_mixed_d_asin"
    )
]


for product in products:
    product.get_keywords().append("all")
    product.get_keywords().append(product.get_name().lower())
    product.get_keywords().append(product.get_category().lower())


@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/all', methods=['GET'])
def get_all_products():
    return jsonify([{'name': product.name, 'price': product.price, 'category': product.category, 'link': product.link,'image': product.image} for product in products])


@app.route('/search', methods=['POST'])
def search_products():
    data = request.get_json()
    keyword = data.get('keyword')
    keyword = keyword.lower()
    results = []
    try:
        float(keyword)
        go = True
        keyword = float(keyword)
    except Exception:
        go = False
        pass
    if go == True:
        for product in products:
            if abs(keyword - product.price) <= product.price*0.15:
                results.append({'name': product.name, 'price': product.price, 'category': product.category,'link': product.link, 'image': product.image})
    else:
        product_matches = []
        for product in products:
            product_matches.extend([product.name] + product.keywords)
        close_matches = difflib.get_close_matches(keyword, product_matches, n=1, cutoff=0.6)
        if close_matches:
            for product in products:
                if close_matches[0] in [product.name] + product.keywords:
                    results.append({'name': product.name, 'price': product.price, 'category': product.category, 'link': product.link, 'image': product.image})
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
