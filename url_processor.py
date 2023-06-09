from urllib.parse import urlparse
from bs4 import BeautifulSoup
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

def download_webpage(url, folder=None, file_name=None):
    if not file_name:
        file_name = "index.html"

    if folder:
        try:
            os.makedirs(folder, exist_ok=True)
            print("Folder created successfully:", folder)
        except OSError as e:
            print("Error occurred while creating folder:", str(e))
            return
        file_path = os.path.join(folder, file_name)
    else:
        file_path = file_name

    print(file_path)

    try:
        response = requests.get(url)
        if response.status_code == 200:

            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.ico']
            file_extension = os.path.splitext(file_name)[1].lower()

            if file_extension in image_extensions:

                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print("Image downloaded successfully:", file_path)

            else:

                content = response.text
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print("Webpage " + file_path + " saved successfully.")
                
        else:
            print("Error: Response status code", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error occurred:", str(e))

def get_nodes_with_attributes(html_file, attribute_names):
    # Load the HTML file
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Create a BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all nodes with the specified attribute names
    nodes = []
    attribute_values = []
    for attr_name in attribute_names:
        for node in soup.find_all(attrs={attr_name: True}):
            if attr_name == 'href' and node.get(attr_name).startswith('#'):
                continue  # Skip attributes with a fragment
            nodes.append(node)
            attribute_value = node.get(attr_name)
            attribute_values.append(attribute_value)

    return nodes, attribute_values

def resolve_relative_paths(relative_paths, folder_path):
    resolved_paths = []
    for relative_path in relative_paths:
        combined_path = os.path.join(folder_path, relative_path)
        resolved_path = os.path.abspath(combined_path)
        resolved_path = os.path.relpath(resolved_path, start = os.curdir).replace('\\', '/')
        resolved_paths.append(resolved_path)
    return resolved_paths

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
        
        path_split = {"base_url": parsed_url.scheme + '://' + parsed_url.netloc, "path": parsed_url.path.lstrip('/'), "folders": folders.lstrip('/'), "file_name": file_name}
        print(path_split)
        
        download_webpage(url, path_split["folders"], path_split["file_name"])

        nodes, attribute_values = get_nodes_with_attributes(path_split["path"], ['href', 'src'])

        if attribute_values:
            # The list is not empty
            resolved_paths = resolve_relative_paths(attribute_values, path_split["folders"])
            # Further processing or actions with the resolved paths
            for value in resolved_paths:
                (sub_folders, sub_file_name) = os.path.split(value)
                sub_url = path_split["base_url"] + "/" + value
                download_webpage(sub_url, sub_folders, sub_file_name)
        else:
            # The list is empty
            print("No attribute values found.")
            # Handle the case when the list is empty

        # Print the nodes
        # for node in nodes:
        #     print(node)

        # Print the attribute values
        # for value in attribute_values:
        #     print(value)

        # Print the resolved paths
        # for path in resolved_paths:
        #     print(path)

    else:
        pass

# Call the function
process_url_from_command_line()