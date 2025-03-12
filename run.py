from app import create_app
from app.routers.test_router import test_bp

app = create_app()
app.register_blueprint(test_bp, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True)
