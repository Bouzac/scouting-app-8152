import webserver
import tables

tables.init_tables()

webserver.app.run(host='0.0.0.0', port=5000, debug=True) #à faire marcher en dernier