from config import create_app
from app.route import register_routes
from app.database import init_mysql_database
# Get the server
server = create_app()

# Configure the sql database
init_mysql_database(server=server)

# Configure caching database

# Configure routes
register_routes(server)

if __name__ == "__main__":
    PORT = 5001
    server.run(debug=True, port=PORT)