from app import app

from utils.openapi import register_rules

from modules.user.api import UserResource

register_rules(app, [
    UserResource
])

if __name__ == "__main__":
    app.run(debug=True, port=80, host='0.0.0.0') 