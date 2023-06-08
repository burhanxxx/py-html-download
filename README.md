# py-html-download
download webpage and resources links with it 

## Download URL Current Page

1. Receive a url from a command line.
2. check status 200 before proceed.
3. Split the url into parts and save it as a json format file.
    1. The protocol or scheme
    2. The host name or domain name
    3. Port name
    4. Path
    5. Query
    6. Parameters
    7. Fragments
4. download the webpage based on the url

## Example usage

$ python url_processor.py https://getbootstrap.com/2.0.2/examples/hero.html
$ 

## Download URL Current Page Along With Internal Resources

1. Get downloaded file (hero.html) and fine all tag that has attribute href or src
2. Get list of paths from tag containing href or src
3. Download the resources

## Example usage 

$ python url_processor.py https://getbootstrap.com/2.0.2/examples/hero.html
$ 