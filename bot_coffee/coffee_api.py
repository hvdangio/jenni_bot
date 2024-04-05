from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app, doc='/swagger/', title='Coffee API', description='A simple Coffee API')

@api.route('/order_coffee')
class OrderCoffee(Resource):
    def post(self):
        # Assuming you're sending a JSON with 'type' and 'quantity'
        return {"message": "Coffee ordered successfully!"}, 200

if __name__ == "__main__":
    app.run(debug=True)
