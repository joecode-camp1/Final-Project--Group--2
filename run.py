from app import create_app
<<<<<<< HEAD
from app.extensions import db

app = create_app()

with app.app_context():
    db.create_all()


=======


app = create_app()

>>>>>>> 9a170a78507a70e27bfb3891a6193573db7602d0
if __name__ == "__main__":
    
    app.run(debug=True)