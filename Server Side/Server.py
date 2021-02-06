import tornado.web
import tornado.ioloop


class uploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("client.html")

    def post(self):
        files = self.request.files["midFile"]

        for f in files:
            if(f.filename[-3:] == "mid"):
                print("its a midi")
                fh = open("mid/"+str(f.filename), "wb")
                fh.write(f.body)
                fh.close()
                self.write("<label> download here: </label>"+" "+"<a href='http://localhost:8080/mid/" +
                           str(f.filename)+"'> midi </a>")


if(__name__ == "__main__"):
    app = tornado.web.Application([
        ("/", uploadHandler),
        ("/mid/(.*)", tornado.web.StaticFileHandler,
         {"path": "mid"})
    ])

app.listen(8080)
print("listening on port 8080")

tornado.ioloop.IOLoop.instance().start()