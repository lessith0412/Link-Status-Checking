import requests

def check_urls(file_path):
    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()
            urls = [url.strip() for url in urls]

            results = {}
            for index, url in enumerate(urls, start=1):
                try:
                    response = requests.head(url, allow_redirects=True, timeout=10)
                    if response.status_code == 200:
                        results[url] = {"Status": "Active", "StatusCode": response.status_code}
                    else:
                        results[url] = {"Status": "Inactive", "StatusCode": response.status_code}
                except requests.RequestException as e:
                    results[url] = {"Status": "Error", "Message": str(e)}

                print(f"Processed URL {index}/{len(urls)}")

            return results
    except IOError:
        print("File not found or unable to read the file.")

def save_results(results):
    try:
        with open('url_status_results.txt', 'w') as file:
            for url, status_info in results.items():
                file.write(f"URL: {url} - {status_info['Status']}\n")
                if status_info['Status'] != 'Error':
                    file.write(f"Status Code: {status_info['StatusCode']}\n")
                else:
                    file.write(f"Error Message: {status_info['Message']}\n")
    except IOError:
        print("Unable to write results to file.")

file_path = 'urls.txt'
url_status = check_urls(file_path)

if url_status:
    save_results(url_status)
    print("Results saved to 'url_status_results.txt'")
