import requests

def checkWebsiteReachability(url):
    """
    Check if a website is reachable and return a report.
    Args:
        url (str): The URL of the website to check.
    Returns:
        dict: A report containing status and details about the request.
    """
    try:
        response = requests.get(url, timeout=10)
        return {
            "url": url,
            "reachable": True,
            "status_code": response.status_code,
            "reason": response.reason,
            "elapsed_time": response.elapsed.total_seconds(),
        }
    except requests.exceptions.Timeout:
        return {
            "url": url,
            "reachable": False,
            "error": "Timeout occurred while trying to reach the website.",
        }
    except requests.exceptions.RequestException as e:
        return {
            "url": url,
            "reachable": False,
            "error": str(e),
        }

def generateReport(result):
    """
    Print a report for the website reachability check.
    Args:
        result (dict): A dictionary containing reachability details.
    """
    print("\nWebsite Reachability Report")
    print("=" * 30)
    print(f"URL: {result['url']}")
    if result["reachable"]:
        print(f"  Status: Reachable")
        print(f"  Status Code: {result['status_code']} ({result['reason']})")
        print(f"  Response Time: {result['elapsed_time']} seconds")
    else:
        print(f"  Status: Not Reachable")
        print(f"  Error: {result.get('error', 'Unknown Error')}")
    print("=" * 30)

def main():
    """
    Main function to test the reachability of a single URL.
    """
    url = input("Enter the URL to check: ").strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        print("Invalid URL. Please include 'http://' or 'https://'.")
        return

    result = checkWebsiteReachability(url)
    generateReport(result)

if __name__ == "__main__":
    main()

