import requests
from datetime import datetime
import time

# File for communication
FILE_PATH = "randomImageUrl.txt"

# Wikimedia Commons API endpoint
RANDOM_IMAGE_API = "https://commons.wikimedia.org/w/api.php"
POTD_API = "https://en.wikipedia.org/w/api.php"

def write_to_file(url):
    """Write the URL to the text file."""
    with open(FILE_PATH, "w") as file:
        file.write(url)


def get_random_image():
    """Fetch a random image URL from Wikimedia Commons."""
    params = {
        "action": "query",
        "format": "json",
        "generator": "random",
        "grnnamespace": 6,  # File namespace
        "prop": "imageinfo",
        "iiprop": "url"
    }
    response = requests.get(RANDOM_IMAGE_API, params=params)
    if response.status_code == 200:
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            return page.get("imageinfo", [{}])[0].get("url")
    return None


def fetch_potd(cur_date):
    """
    Fetch the Wikimedia Commons Picture of the Day using the correct Wikimedia API endpoint.
    """
    date_iso = cur_date.strftime("%Y-%m-%d")
    title = f"Template:POTD_protected/{date_iso}"

    # First, get the filename of the POTD
    params = {
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "prop": "images",
        "titles": title
    }

    response = requests.get(url=POTD_API, params=params)
    print("POTD API Response (step 1):", response.json())  # Debug print

    if response.status_code == 200:
        data = response.json()
        try:
            # Extract the filename of the image
            filename = data["query"]["pages"][0]["images"][0]["title"]
            print("Extracted filename:", filename)  # Debug print

            # Use the filename to get the image URL
            return fetch_image_src(filename)
        except (KeyError, IndexError) as e:
            print("Error extracting POTD filename:", str(e))
    else:
        print(f"Error fetching POTD metadata: HTTP {response.status_code}")
    return None


def fetch_image_src(filename):
    """
    Fetch the direct image URL for a given file name.
    """
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url",
        "titles": filename
    }

    response = requests.get(url=POTD_API, params=params)
    print("POTD Image Info API Response:", response.json())  # Debug print

    if response.status_code == 200:
        data = response.json()
        try:
            # Extract the URL of the image
            page = next(iter(data["query"]["pages"].values()))
            image_url = page["imageinfo"][0]["url"]
            print("Extracted image URL:", image_url)  # Debug print
            return image_url
        except (KeyError, IndexError) as e:
            print("Error extracting image URL:", str(e))
    else:
        print(f"Error fetching image metadata: HTTP {response.status_code}")
    return None


def get_picture_of_the_day():
    """
    Wrapper function to fetch the current Picture of the Day.
    """
    cur_date = datetime.now()
    return fetch_potd(cur_date)


def serve_request(request_type):
    """
    Serve the request based on the type:
    - 'random': Provide a random image.
    - 'picture_of_day': Provide the picture of the day.
    """
    try:
        if request_type == "random":
            print("Processing random image request...")
            random_image = get_random_image()
            if random_image:
                write_to_file(random_image)
            else:
                write_to_file("Error: Could not fetch random image.")
        elif request_type == "picture_of_day":
            print("Processing Picture of the Day request...")
            potd_image = get_picture_of_the_day()
            if potd_image:
                write_to_file(potd_image)
            else:
                write_to_file("Error: Could not fetch picture of the day.")
    except Exception as e:
        print("Error:", str(e))
        write_to_file(f"Error: {str(e)}")


def listen_for_requests():
    """
    Continuously listen for requests from other programs via the text file.
    """
    last_request = None
    while True:
        try:
            with open(FILE_PATH, "r") as file:
                request_type = file.read().strip()
            if request_type and request_type != last_request:
                serve_request(request_type)
                last_request = request_type
        except FileNotFoundError:
            pass
        time.sleep(1)  # Poll every second for new requests


if __name__ == "__main__":
    print("Microservice is running. Listening for requests...")
    listen_for_requests()
