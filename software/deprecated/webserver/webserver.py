""" test_webserver sets up a basic Flask webserver to 
server html to/from localhost interface following this tutorial:
https://towardsdatascience.com/python-webserver-with-flask-and-raspberry-pi-398423cc6f5d and
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
 """

from app import app
from app import routes

if __name__ == "__main__":
    print(routes.index())

