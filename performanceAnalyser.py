import httpx
import argparse
from icecream import ic
from datetime import timedelta


# Constants
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
)


# Function to fetch website and measure detailed performance
def fetch_url_details(url: str, headers: dict) -> dict:
    """
    Fetch the URL and measure performance details.
    Args:
        url (str): The URL to fetch.
        headers (dict): The headers to use for the request.
    Returns:
        dict: A dictionary with performance metrics and response info.
    """
    try:
        with httpx.Client(headers=headers) as client:
            response = client.get(url, follow_redirects=True)

            return {
                "status_code": response.status_code,
                "size_kb": len(response.content) / 1024,  # Convert bytes to KB
                "load_time": response.elapsed.total_seconds(),  # Load time in seconds
                "final_url": str(response.url),
                "redirect_count": len(response.history),
                "headers": response.headers,
            }
    except httpx.RequestError as e:
        ic(f"Request error: {e}")
        return {
            "status_code": None,
            "size_kb": 0.0,
            "load_time": 0.0,
            "final_url": url,
            "redirect_count": 0,
            "headers": None,
            "error": str(e),
        }


# Function to generate and print a performance report
def generate_report(results: dict, url: str) -> None:
    """
    Generate and print the performance analysis report.
    Args:
        results (dict): The results of the performance test.
        url (str): The tested URL.
    """
    print(f"\nPerformance Report for {url}")
    print("=" * 50)
    print(f"Status Code: {results.get('status_code', 'N/A')}")
    print(f"Page Size: {results.get('size_kb', 0):.2f} KB")
    print(f"Load Time: {timedelta(seconds=results.get('load_time', 0))}")
    print(f"Final URL: {results.get('final_url', 'N/A')}")
    print(f"Redirect Count: {results.get('redirect_count', 0)}")
    if results.get("headers"):
        print(f"Response Headers: {dict(results['headers'])}")
    if error := results.get("error"):
        print(f"Error: {error}")
    print("=" * 50)


# Main function to handle CLI arguments
def main():
    """
    Main function to handle command-line arguments and analyze website performance.
    """
    parser = argparse.ArgumentParser(description="Analyze the performance of a website.")
    parser.add_argument("url", type=str, help="The URL of the website to analyze.")
    parser.add_argument(
        "--user-agent",
        type=str,
        default=None,
        help="Custom User-Agent string for the request. "
             "If not provided, a default browser user agent will be used."
    )
    args = parser.parse_args()

    # Validate URL format
    if not args.url.startswith("http://") and not args.url.startswith("https://"):
        print("Invalid URL. Please include 'http://' or 'https://'.")
        return

    # Set user agent
    user_agent = args.user_agent or DEFAULT_USER_AGENT
    headers = {"User-Agent": user_agent}

    # Analyze the website performance
    ic(f"Analyzing performance for {args.url} with User-Agent: {user_agent}")
    results = fetch_url_details(args.url, headers)

    # Generate and print the report
    generate_report(results, args.url)


if __name__ == "__main__":
    main()
