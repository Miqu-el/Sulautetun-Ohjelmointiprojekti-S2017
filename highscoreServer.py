import socket
import pymysql
import netifaces #Käytetään Raspberryn IP:n löytämiseen dynaamisesti

class highscoreServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(None)
    def initialise(self):
        try:
            self.sock.bind((self.host, self.port))
        except socket.error:
            print("Socket error in initialise function")
            return
        self.sock.listen(5)
        print("Server running on ",self.host,"and listening to ", self.port)

    def serve_forever(self):
        try:
            request, client_address = self.sock.accept()
            print("Received connection from ", client_address)
            data = request.recv(20)
            stringdata = data.decode('utf-8', 'ignore')
            stringdata = stringdata[2:len(stringdata)].split(",")
            name = stringdata[0]
            score = int(stringdata[1])
            print("Received data: ", name, " with the score of ", score)
            self.insertHighScores(name, score)
        except socket.error:
            print("Socket error in serve_forever-function")
            return
        finally:
            request.close()
    @staticmethod
    def insertHighScores(name, score):
        query = "INSERT INTO leaderboards(name, points) VALUES('{0}',{1})".format(name, score)
        db = pymysql.connect(host="mysli.oamk.fi", user="t6kovi01", passwd="", db="opisk_t6kovi01")
        cur = db.cursor()
        cur.execute(query)
        db.commit()
        db.close()
        
def main():
    netifaces.ifaddresses("wlan0")
    host = netifaces.ifaddresses("wlan0")[2][0]["addr"] #Haetaan raspberryn IP
    server = highscoreServer(host, 20000)
    server.initialise()
    while True:
        server.serve_forever()

if __name__ == "__main__":
    main()
