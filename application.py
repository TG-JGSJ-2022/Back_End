from app import app

if __name__ == '__main__':
    app.debug = True
    #app.run("25.1.186.127",port=5000)
    app.run("localhost",port=5000,debug=True)