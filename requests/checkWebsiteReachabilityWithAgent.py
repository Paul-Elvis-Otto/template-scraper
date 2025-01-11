import requests
import argparse

def checkWebsiteReachability(url, user_agent):
    """
    Check if a website is reachable using a custom user agent and return a report.
    Args:
        url (str): The URL of the website to check.
        user_agent (str): The user agent to use for the request.
    Returns:
        dict: A report containing status and details about the request.
    """
    headers = {"User-Agent": user_agent}
    try:
        response = requests.get(url, headers=headers, timeout=10)
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
    Main function to handle command-line arguments and check website reachability.
    """
    parser = argparse.ArgumentParser(description="Check website reachability with a custom User-Agent.")
    parser.add_argument("url", type=str, help="The URL to check.")
    parser.add_argument("--user-agent", type=str, default=None, 
                        help="Custom User-Agent string to use for the request. "
                             "If not provided, a default browser user agent will be used.")
    args = parser.parse_args()

    # Default user agent if none is provided
    default_user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )
    user_agent = args.user_agent or default_user_agent

    # Validate URL
    if not args.url.startswith("http://") and not args.url.startswith("https://"):
        print("Invalid URL. Please include 'http://' or 'https://'.")
        return

    # Check website reachability
    result = checkWebsiteReachability(args.url, user_agent)
    generateReport(result)

if __name__ == "__main__":
    main()
