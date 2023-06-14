from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import sys
import os


def print_set_to_file(some_set, file_path):
    with open(file_path, 'w') as file:
        for item in some_set:
            print(item, file=file)

def get_base_url(url):
    parsed_url = urlparse(url)
    if parsed_url.path:
        index = url.find(parsed_url.path)
        if index != -1:
            return url[:index]
        else:
            return url
    else:
        return url

def check_url(url):
    try:
        response = requests.head(url)
        if response.status_code == 200:
            print(f'URL: {url} , Status Code: {response.status_code}')
            return True
        else:
            print('The URL returned a non-200 status code.')
            return False
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
        print('An error occurred during the request:', e)
        return False

def get_nodes_with_attributes(url, attribute_names):

    nodes = []
    attribute_values = set()

    try:
        # Load the HTML file
        response = requests.get(url)
        if (response.status_code == 200) and ('html' in response.headers.get('Content-Type')):

            # Create a BeautifulSoup object to parse the HTML
            content = response.text
            soup = BeautifulSoup(content, 'html.parser')

            # Find all nodes with the specified attribute names
            # nodes = []
            # attribute_values = []
            for attr_name in attribute_names:
                for node in soup.find_all(attrs={attr_name: True}):
                    # if attr_name == 'href' and node.get(attr_name).startswith('#'):
                    #     continue  # Skip attributes with a fragment
                    nodes.append(node)
                    attribute_value = node.get(attr_name)
                    attribute_values.add(attribute_value)
        else:
            print('The URL returned a non-200 status code.')
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
        print('An error occurred during the request:', e)   
    
    return nodes, attribute_values

def resolve_relative_paths(url):

    base_url = get_base_url(url)

    parsed_url = urlparse(url)
    folders, file_name = os.path.split(parsed_url.path)

    _, relative_paths = get_nodes_with_attributes(url, ['href', 'src'])

    resolved_paths = []
    resolved_paths.append(url)

    for relative_path in relative_paths:

        if '#' in relative_path:
            combined_path = f'{base_url}{parsed_url.path}{relative_path}'
            resolved_paths.append(combined_path)
        elif not ('://' in relative_path):
            combined_path = os.path.join(folders.lstrip('/'), relative_path)
            resolved_path = os.path.abspath(combined_path)
            resolved_path = os.path.relpath(resolved_path, start = os.curdir).replace('\\', '/')
            resolved_path = f'{base_url}/{resolved_path}'
            resolved_paths.append(resolved_path)
        else:
            resolved_paths.append(relative_path)
    return resolved_paths

def download(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            
            parsed_url = urlparse(url)
            folders, file_name = os.path.split(parsed_url.path)
            
            if not file_name:
                file_name = "index.html"
            
            if folders:
                folders = folders.lstrip('/')
                try:
                    os.makedirs(folders, exist_ok=True)
                    print("Folder created successfully:", folders)
                except OSError as e:
                    print("Error occurred while creating folder:", str(e))
                    return
                file_path = folders + "/" + file_name
            else:
                file_path = file_name

            content = requests.get(url, stream=True)
            with open(file_path, 'wb') as file:
                for chunk in content:
                    file.write(chunk)
            print("File downloaded successfully:", file_path)
        
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

    if check_url(url):
        
        # get list of sub urls available in the base url
        url_list = resolve_relative_paths(url)

        # print url list into file
        print_set_to_file(url_list, 'download_paths.txt')

        # Print the attribute values
        for u in url_list:
            print(f'Download: {u}')
            download(u)

# Call the function
process_url_from_command_line()

