# py-html-download

Download webpage and resources link with it 

## Requirements

1. Python 3.10.11
2. pip install requests
3. pip install beautifulsoup4

## Download URL Current Page

1. Receive a url from a command line.
```
    process_url_from_command_line()
```

2. Check status 200 before proceed.
```
    check_url(url)
```
3. Split the url into parts and save it as a json format file.
    1. The protocol or scheme
    2. The host name or domain name
    3. Port name
    4. Path
    5. Query
    6. Parameters
    7. Fragments
```
    parsed_url = urlparse(url)
```

4. download the webpage based on the url
```
    download_webpage(url, folders, file_name)
```
## Example usage
```
/> python url_processor.py https://getbootstrap.com/2.0.2/examples/hero.html 
```
This will download only the webpage and its folder path.
The result is "2.0.2/examples/hero.html"

## Download URL Current Page Along With Internal Resources

1. Get downloaded file (e.g. hero.html) and fine all tags that has attribute href or src
```
    get_nodes_with_attributes(html_file, attribute_names)
```

2. Get list of paths from tag containing href or src
```
    resolve_relative_paths(relative_paths, folder_path)
```

3. Download the resources
```
    download_webpage(url, folders, file_name)
```

## Example usage 
```
/> python url_processor.py https://getbootstrap.com/2.0.2/examples/hero.html
```