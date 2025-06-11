@nightyScript(
    name="GitHub Trending Fetcher",
    author="AutoGPT",
    description="Fetches top GitHub trending repositories",
    usage="<p>trending",
)
def github_trending_fetcher():
    """
    GitHub Trending Fetcher
    -----------------------

    Fetches the titles of trending repositories from GitHub using requests and BeautifulSoup.

    COMMANDS:
    <p>trending - Fetch trending repository names from GitHub

    EXAMPLE:
    <p>trending

    NOTES:
    - Requires `requests` and `beautifulsoup4` packages.
    - Install with: `pip install requests beautifulsoup4`
    - Uses synchronous HTTP requests with requests library.
    """

    import requests
    from bs4 import BeautifulSoup

    @bot.command(name="trending", description="Fetch GitHub trending repositories")
    async def trending_command(ctx):
        await ctx.message.delete()

        url = "https://github.com/trending"
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code != 200:
            await ctx.send(f"Failed to fetch trending page (status {resp.status_code})")
            return

        soup = BeautifulSoup(resp.text, "html.parser")
        repo_names = [a.text.strip() for a in soup.select('h1.h3 a')]
        top_repos = repo_names[:5]
        formatted = "\n".join(top_repos) if top_repos else "No repositories found"
        await ctx.send(f"Top GitHub Trending Repos:\n```\n{formatted}\n```")

github_trending_fetcher()
