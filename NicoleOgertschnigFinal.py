import logging
import psycopg2
import getpass
from psycopg2 import sql



# Set up logging
logging.basicConfig(filename='error.log', level=logging.DEBUG)  #
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('error.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def connect_to_database():
    logger.info("Attempting to connect to database")
    try:
        # print("Entered connect to database function")
        # username = input("Enter username for database: ")
        # password = getpass.getpass("Enter password: ")
        connection = psycopg2.connect(
            host="localhost",
            database="postgres",
            # host="localhost",
            # database="postgres",
            user=postgres,
            password=pass123,
            # user=username,  # Using the provided username above.
            # password=password,  # Using the provided password above or the one you set
            )
        
        # print(f"Connected to the database as user '{username}'")

        #Per the code in your count_rows, this function needs to return a connection
        #or return none so it's checked later.
        logger.info("Sucessful Connection to database")
        return connection
    except psycopg2.Error as e:
        logger.error(f"Error connecting to the database: {e}")
        print("Error connecting to the database. Check error.log for details.")
        return None

def count_rows(table_name: str, limit: int) -> int:
    logger.info(f'Attempting to count rows.')
    

    try:
        if connection:
            with connection.cursor() as cursor:
                stmt = sql.SQL("""
                    SELECT count(*)
                    FROM {}
                    LIMIT %s
                """).format(
                    sql.Identifier(table_name)
                )
                cursor.execute(stmt, (limit,))
                result = cursor.fetchone()
                rowcount, = result
                print(f"Running 'count_rows()' with parameters table_name={table_name} and limit={limit}")
                print(f"Rows: {rowcount}")
                logger.info("Sucessful row count")
                return rowcount
    except psycopg2.Error as e:
        logger.error(f"Error counting rows: {e}")
        print("Error counting rows. Check error.log for details.")
        return -1

def is_admin():
    try:

        if connection:
            while True:
                username = input("Please enter a username to validate admin permissions or type 'Q' to quit: ")
                logger.info(f"Entered {username} for admin validation.")

                if username.lower() == 'q':
                    logger.info("Quit admin validation process")
                    break
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT admin
                        FROM users
                        WHERE username = %s
                    """, (username,))
                    result = cursor.fetchone()
                    if result is None:
                        print(f"Is '{username}' an admin? Result: False")
                        logger.info(f"{username} is not an admin")
                    else:
                        admin, = result
                        print(f"Is '{username}' an admin? Result: {admin}")
    except psycopg2.Error as e:
        logger.error(f"Error checking admin status: {e}")
        print("Error checking admin status. Check error.log for details.")

if __name__ == '__main__':
    correct_username = "postgres"
    correct_password = "pass123"

    attempts_left = 3
    logged_in = False
    while attempts_left > 0:
        postgres = input("Enter username for database: ")
        pass123 = getpass.getpass("Enter password: ")
        logger.info(f"Entered '{postgres}' as username")
        if postgres == correct_username and pass123 == correct_password:
            print("Connected to the database as user 'postgres'.")
            logger.info("Succesful login to database")
            logged_in = True
            break
        else:
            attempts_left -= 1
            if attempts_left > 0:
                print(f"Incorrect username or password. Error connecting to database {attempts_left} attempts left.")
                logger.error(f"Incorrect username or password. Error connecting to database {attempts_left} attempts left.")
                
            else:
                print("Incorrect username or password!! Logging out.")
                logger.info("Too many attemps at logging in. Logged out from system")
                logged_in = False
                
    if logged_in:
        connection = connect_to_database()  # This will call the connect_to_database function
        response = ""
        while response != 'q':
            response = input("Enter 'count rows' to count rows, 'admin' to check admin, or 'q' to quit:").lower()
            if response == "count rows":
                print("Validating 'count_rows()' with parameters table_name='users' and limit=10")
                count_rows('users', 10)  # Function to count rows

            elif response == 'admin':
                admin_username = input("Please enter admin name: ")
                if admin_username == "postgres":
                    logging.info("Welcome Postgres")
                    print("Welcome Postgres")
                else:
                    print("Incorrect admin username.")
                    logger.error("Incorrect admin username.")

            elif response == 'q':
                print("Logging out")
                break
            else:
                print("Invalid command. Please enter 'count rows', 'admin', or 'q'.")

            
            # print(count_rows("(select 1) as foo; update users set admin = true where name = 'ogertschnig'; --", 1))

