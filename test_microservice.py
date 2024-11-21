import time

FILE_PATH = "randomImageUrl.txt"


def write_request(request_type):
    """Write a request to the text file."""
    with open(FILE_PATH, "w") as file:
        file.write(request_type)


def read_response():
    """Read the response (image URL) from the text file."""
    with open(FILE_PATH, "r") as file:
        return file.read().strip()


def test_microservice():
    """Test the microservice by sending requests and reading responses."""
    # Test random image
    print("Testing random image request...")
    write_request("random")
    time.sleep(3)  # Give the microservice some time to process
    random_image_url = read_response()
    print(f"Random Image URL: {random_image_url}")

    # Test picture of the day
    print("Testing picture of the day request...")
    write_request("picture_of_day")
    time.sleep(3)  # Give the microservice some time to process
    potd_image_url = read_response()
    print(f"Picture of the Day URL: {potd_image_url}")


if __name__ == "__main__":
    test_microservice()
