
from flask import Flask
from home import home_bp
from planners import planner_bp

app = Flask(__name__)

app.register_blueprint(home_bp)
app.register_blueprint(planner_bp)


if __name__ == "__main__":
    app.run(debug=True)
