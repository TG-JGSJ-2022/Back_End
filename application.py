from app import application

if __name__ == '__main__':
    application.debug = False
    #app.run("25.1.186.127",port=5000)
    application.run("localhost",port=5000,debug=True)