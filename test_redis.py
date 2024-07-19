import redis
from redis.exceptions import RedisError, ConnectionError
from colorama import init, Fore, Style

# Initialize colorama
init()

# Connect to the Redis server running on Docker Desktop
try:
    client = redis.StrictRedis(host='localhost', port=6379, db=0)
    client.ping()
    print(Fore.GREEN + "Connected to Redis server successfully." + Style.RESET_ALL)
except (ConnectionError, RedisError) as e:
    print(Fore.RED + f"Error connecting to Redis server: {e}" + Style.RESET_ALL)
    exit(1)

# Function to test CRUD operations
def test_redis_crud():
    try:
        # Key and values for testing
        key = "test_key"
        initial_value = "initial_value"
        updated_value = "updated_value"

        # Create
        print("Creating key...")
        client.set(key, initial_value)
        value = client.get(key)
        if value != initial_value.encode('utf-8'):
            raise ValueError(f"Expected value '{initial_value}', but got '{value.decode('utf-8')}'")
        print(Fore.GREEN + f"Pass: Created key '{key}' with value '{initial_value}'" + Style.RESET_ALL)

        # Read
        print("Reading key...")
        value = client.get(key)
        if value != initial_value.encode('utf-8'):
            raise ValueError(f"Expected value '{initial_value}', but got '{value.decode('utf-8')}'")
        print(Fore.GREEN + f"Pass: Read key '{key}' with value '{value.decode('utf-8')}'" + Style.RESET_ALL)

        # Update
        print("Updating key...")
        client.set(key, updated_value)
        value = client.get(key)
        if value != updated_value.encode('utf-8'):
            raise ValueError(f"Expected value '{updated_value}', but got '{value.decode('utf-8')}'")
        print(Fore.GREEN + f"Pass: Updated key '{key}' to value '{updated_value}'" + Style.RESET_ALL)

        # Delete
        print("Deleting key...")
        client.delete(key)
        value = client.get(key)
        if value is not None:
            raise ValueError(f"Expected key '{key}' to be deleted, but it still exists with value '{value.decode('utf-8')}'")
        print(Fore.GREEN + f"Pass: Deleted key '{key}'" + Style.RESET_ALL)

    except RedisError as e:
        print(Fore.RED + f"Fail: Redis error: {e}" + Style.RESET_ALL)
    except ValueError as e:
        print(Fore.RED + f"Fail: Value error: {e}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Fail: Unexpected error: {e}" + Style.RESET_ALL)

# Run the CRUD test
if __name__ == "__main__":
    test_redis_crud()
