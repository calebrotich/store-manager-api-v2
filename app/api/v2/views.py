"""Define API endpoints as routes"""

from flask_restful import Api, Resource

from . import endpoint_v2_blueprint, auth_v2_blueprint
from .resources import (
    auth, products, saleorders, category
)

API = Api(endpoint_v2_blueprint)
AUTH_API = Api(auth_v2_blueprint)


API.add_resource(products.Product, '/products')
API.add_resource(products.SpecificProduct, '/product/<int:product_id>')
API.add_resource(saleorders.SaleOrder, '/saleorder')
API.add_resource(saleorders.SpecificSaleOrder, '/saleorder/<int:saleorder_id>')
API.add_resource(category.ProductCategory, '/category')
API.add_resource(category.SpecificCategory, '/category/<int:category_id>')

AUTH_API.add_resource(auth.SignUp, '/signup')
AUTH_API.add_resource(auth.Login, '/login')
AUTH_API.add_resource(auth.Logout, '/logout')