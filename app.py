from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

# Data dummy untuk contoh
salons = [
    {"id": "1", "name": "Beauty Glow", "description": "Salon kecantikan dengan pelayanan lengkap", "rating": 4.5},
    {"id": "2", "name": "Elegance Hair", "description": "Spesialis potong rambut dan perawatan wajah", "rating": 4.7},
]
details = {
    "1": {
        "name": "Beauty Glow",
        "description": "Salon kecantikan dengan pelayanan lengkap",
        "rating": 4.5,
        "customerReviews": []
    },
    "2": {
        "name": "Elegance Hair",
        "description": "Spesialis potong rambut dan perawatan wajah",
        "rating": 4.7,
        "customerReviews": []
    }
}

# Data produk salon
products = [
    {"id": "1", "name": "Shampoo", "price": 50000, "description": "Shampoo untuk semua jenis rambut"},
    {"id": "2", "name": "Conditioner", "price": 60000, "description": "Conditioner yang melembutkan rambut"},
]

app = Flask(__name__)
api = Api(app)

# CRUD untuk produk
class ProductList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(products),
            "products": products
        }

    def post(self):
        data = request.get_json()
        new_product = {
            "id": str(len(products) + 1),  # Generate ID sederhana
            "name": data.get("name"),
            "price": data.get("price"),
            "description": data.get("description")
        }
        products.append(new_product)
        return {"error": False, "message": "Product added", "product": new_product}, 201

class ProductDetail(Resource):
    def get(self, product_id):
        product = next((p for p in products if p["id"] == product_id), None)
        if product:
            return {"error": False, "message": "success", "product": product}
        return {"error": True, "message": "Product not found"}, 404

    def put(self, product_id):
        data = request.get_json()
        product = next((p for p in products if p["id"] == product_id), None)
        if product:
            product["name"] = data.get("name", product["name"])
            product["price"] = data.get("price", product["price"])
            product["description"] = data.get("description", product["description"])
            return {"error": False, "message": "Product updated", "product": product}
        return {"error": True, "message": "Product not found"}, 404

    def delete(self, product_id):
        global products
        products = [p for p in products if p["id"] != product_id]
        return {"error": False, "message": "Product deleted"}

# Menambahkan resource dan endpoint untuk produk
api.add_resource(ProductList, '/products')
api.add_resource(ProductDetail, '/product/<string:product_id>')

# Endpoint untuk daftar salon
class SalonList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(salons),
            "salons": salons
        }

# Endpoint untuk detail salon berdasarkan ID
class SalonDetail(Resource):
    def get(self, salon_id):
        if salon_id in details:
            return {
                "error": False,
                "message": "success",
                "salon": details[salon_id]
            }
        return {"error": True, "message": "Salon not found"}, 404

# Endpoint untuk pencarian salon berdasarkan nama atau deskripsi
class SalonSearch(Resource):
    def get(self):
        query = request.args.get('q', '').lower()
        result = [s for s in salons if query in s['name'].lower() or query in s['description'].lower()]
        return {
            "error": False,
            "found": len(result),
            "salons": result
        }

# Endpoint untuk menambah ulasan pada salon
class AddReview(Resource):
    def post(self):
        data = request.get_json()
        salon_id = data.get('id')
        name = data.get('name')
        review = data.get('review')
        
        if salon_id in details:
            new_review = {
                "name": name,
                "review": review,
                "date": datetime.now().strftime("%d %B %Y")
            }
            details[salon_id]['customerReviews'].append(new_review)
            return {
                "error": False,
                "message": "success",
                "customerReviews": details[salon_id]['customerReviews']
            }
        return {"error": True, "message": "Salon not found"}, 404

# Endpoint untuk memperbarui ulasan
class UpdateReview(Resource):
    def put(self):
        data = request.get_json()
        salon_id = data.get('id')
        name = data.get('name')
        new_review_text = data.get('review')
        
        if salon_id in details:
            reviews = details[salon_id]['customerReviews']
            review_to_update = next((r for r in reviews if r['name'] == name), None)
            if review_to_update:
                review_to_update['review'] = new_review_text
                review_to_update['date'] = datetime.now().strftime("%d %B %Y")
                return {
                    "error": False,
                    "message": "success",
                    "customerReviews": reviews
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Salon not found"}, 404

# Endpoint untuk menghapus ulasan
class DeleteReview(Resource):
    def delete(self):
        data = request.get_json()
        salon_id = data.get('id')
        name = data.get('name')
        
        if salon_id in details:
            reviews = details[salon_id]['customerReviews']
            review_to_delete = next((r for r in reviews if r['name'] == name), None)
            if review_to_delete:
                reviews.remove(review_to_delete)
                return {
                    "error": False,
                    "message": "success",
                    "customerReviews": reviews
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Salon not found"}, 404

# Menambahkan resource dan endpoint ke API
api.add_resource(SalonList, '/salons')
api.add_resource(SalonDetail, '/salon/<string:salon_id>')
api.add_resource(SalonSearch, '/salon/search')
api.add_resource(AddReview, '/salon/review')
api.add_resource(UpdateReview, '/salon/review/update')
api.add_resource(DeleteReview, '/salon/review/delete')

if __name__ == '__main__':
    app.run(debug=True)
