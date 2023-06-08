from urllib.parse import urlparse
import requests
import sys
import os

def check_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("URL is valid (status code: 200)")
            return True
        else:
            print("URL is valid, but returned status code:", response.status_code)
            return False
    except requests.exceptions.RequestException as e:
        print("Error occurred:", str(e))
        return False

def download_webpage(url, file_name=None):
    if not file_name:
        file_name = "index.html"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(content)
            print("Webpage saved successfully.")
        else:
            print("Error: Response status code", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error occurred:", str(e))

def process_url_from_command_line():
    if len(sys.argv) < 2:
        print("Please provide a URL as a command-line argument.")
        return

    url = sys.argv[1]
    print("URL:", url)

    # Perform further processing with the URL
    # ...

    if check_url(url):

        parsed_url = urlparse(url)
        print(parsed_url)

        (folders, file_name) = os.path.split(parsed_url.path)
        path_split = {"path": parsed_url.path, "folders": folders, "file_name": file_name}
        print(path_split)
        
        download_webpage(url, path_split.get("file_name"))


    else:
        pass

# Call the function
process_url_from_command_line()