import httpx
from typing import Dict, Any

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)


def fetch_robots_txt(url: str, user_agent: str = DEFAULT_USER_AGENT) -> str:
    """
    Fetch the content of the robots.txt file for a given website.

    Args:
        url (str): The base URL of the website (e.g., "https://example.com").
        user_agent (str): The User-Agent header to use when making the request.

    Returns:
        str: The content of the robots.txt file as a string, or an error message.
    """
    robots_url = url.rstrip("/") + "/robots.txt"
    headers = {"User-Agent": user_agent}

    try:
        response = httpx.get(robots_url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except httpx.RequestError as exc:
        return f"Request error: {exc}"
    except httpx.HTTPStatusError as exc:
        return f"HTTP error: {exc}"


def parse_robots_txt(content: str) -> Dict[str, Any]:
    """
    Parse the content of a robots.txt file into a structured dictionary.

    Args:
        content (str): The content of the robots.txt file.

    Returns:
        Dict[str, Any]: A dictionary with parsed directives (e.g., User-Agent, Allow, Disallow) and sitemaps.
    """
    parsed_data = {"Sitemaps": [], "Rules": {}}
    current_user_agent = None

    for line in content.splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if line.lower().startswith("sitemap"):
            sitemap_url = line.split(":", 1)[-1].strip()
            parsed_data["Sitemaps"].append(sitemap_url)

        elif line.lower().startswith("user-agent"):
            current_user_agent = line.split(":", 1)[-1].strip()
            parsed_data["Rules"][current_user_agent] = {"Allow": [], "Disallow": []}

        elif current_user_agent and ":" in line:
            directive, path = map(str.strip, line.split(":", 1))
            if directive.lower() in {"allow", "disallow"}:
                parsed_data["Rules"][current_user_agent][directive.capitalize()].append(path)

    return parsed_data


def generate_report(parsed_data: Dict[str, Any]) -> str:
    """
    Generate a human-readable report from the parsed robots.txt data.

    Args:
        parsed_data (Dict[str, Any]): The parsed robots.txt data.

    Returns:
        str: A formatted string report of the robots.txt rules and sitemaps.
    """
    report = []

    if parsed_data["Sitemaps"]:
        report.append("Sitemaps found:")
        report.extend([f"  - {sitemap}" for sitemap in parsed_data["Sitemaps"]])
        report.append("")

    for user_agent, rules in parsed_data["Rules"].items():
        report.append(f"User-Agent: {user_agent}")
        for directive, paths in rules.items():
            if paths:
                report.append(f"  {directive}:")
                report.extend([f"    - {path}" for path in paths])

    return "\n".join(report)


def check_robots_txt(url: str, user_agent: str = DEFAULT_USER_AGENT) -> str:
    """
    Check and report on the robots.txt file of a website.

    Args:
        url (str): The base URL of the website.
        user_agent (str): The User-Agent header to use when making the request.

    Returns:
        str: A human-readable report of the robots.txt file content and parsed rules.
    """
    content = fetch_robots_txt(url, user_agent)

    if content.startswith("Request error") or content.startswith("HTTP error"):
        return content

    parsed_data = parse_robots_txt(content)
    return generate_report(parsed_data)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Check and report on a site's robots.txt file.")
    parser.add_argument("url", help="The base URL of the website (e.g., https://example.com).")
    parser.add_argument(
        "--user-agent", help="Custom User-Agent for the request.", default=DEFAULT_USER_AGENT
    )

    args = parser.parse_args()
    report = check_robots_txt(args.url, args.user_agent)
    print(report)

