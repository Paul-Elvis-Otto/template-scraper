import httpx
import argparse
from icecream import ic
from tqdm import tqdm


def load_potential_sitemaps(file_path):
    """
    Load potential sitemap paths from a text file.
    Args:
        file_path (str): The path to the text file containing sitemap paths.
    Returns:
        list: A list of potential sitemap paths.
    """
    try:
        with open(file_path, "r") as file:
            sitemaps = [line.strip() for line in file if line.strip()]
            ic(f"Loaded {len(sitemaps)} sitemap paths from {file_path}")
            return sitemaps
    except FileNotFoundError:
        ic(f"File not found: {file_path}")
        return []
    except Exception as e:
        ic(f"Error reading file {file_path}: {e}")
        return []


def check_sitemap(base_url, path, user_agent):
    """
    Check if a specific sitemap path is reachable.
    Args:
        base_url (str): The base URL of the website.
        path (str): The sitemap path to check.
        user_agent (str): The user agent to use for the request.
    Returns:
        dict: A result dictionary containing the URL, status, and details.
    """
    full_url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
    headers = {"User-Agent": user_agent}
    try:
        response = httpx.get(full_url, headers=headers, timeout=10)
        ic(f"Checked {full_url}: {response.status_code} {response.reason_phrase}")
        return {
            "url": full_url,
            "reachable": response.status_code == 200,
            "status_code": response.status_code,
            "reason": response.reason_phrase,
        }
    except httpx.RequestError as e:
        ic(f"Request error for {full_url}: {e}")
        return {
            "url": full_url,
            "reachable": False,
            "error": str(e),
        }


def generate_report(results):
    """
    Generate and print a report of sitemap checks.
    Args:
        results (list): A list of result dictionaries from sitemap checks.
    """
    print("\nSitemap Check Report")
    print("=" * 30)
    for result in results:
        print(f"URL: {result['url']}")
        if result["reachable"]:
            print(f"  Status: Reachable")
            print(f"  Status Code: {result['status_code']} ({result['reason']})")
        else:
            print(f"  Status: Not Reachable")
            print(f"  Error: {result.get('error', 'Unknown Error')}")
        print("-" * 30)


def main():
    """
    Main function to handle command-line arguments and check for sitemaps.
    """
    parser = argparse.ArgumentParser(description="Check for a website's sitemap availability.")
    parser.add_argument("url", type=str, help="The base URL of the website to check.")
    parser.add_argument(
        "--sitemap-file",
        type=str,
        default="potentialSitemaps.txt",
        help="Path to the file containing potential sitemap paths (default: potentialSitemaps.txt)."
    )
    parser.add_argument(
        "--user-agent",
        type=str,
        default=None,
        help="Custom User-Agent string to use for the requests. "
             "If not provided, a default browser user agent will be used."
    )
    args = parser.parse_args()

    # Default user agent
    default_user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )
    user_agent = args.user_agent or default_user_agent

    # Validate URL
    if not args.url.startswith("http://") and not args.url.startswith("https://"):
        print("Invalid URL. Please include 'http://' or 'https://'.")
        return

    # Load potential sitemaps
    sitemap_paths = load_potential_sitemaps(args.sitemap_file)
    if not sitemap_paths:
        print("No sitemap paths to check. Please ensure the sitemap file is populated.")
        return

    # Check each sitemap with progress bar
    results = []
    print(f"Checking {len(sitemap_paths)} sitemap paths for {args.url}...")
    for path in tqdm(sitemap_paths, desc="Sitemap checks", unit="sitemaps"):
        results.append(check_sitemap(args.url, path, user_agent))

    # Generate and print the report
    generate_report(results)


if __name__ == "__main__":
    main()
