from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True) # PLEASE don't forget to change this for prod
