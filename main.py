from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) # use_reloader=False to prevent the browser from opening twice (This also seem to make it so changes I make to code do not seem to get applied for some reason)