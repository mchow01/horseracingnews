# Overview
MCP server to get content from thoroughbreddailynews.com's RSS feed

# Requirements
* `uv`.  Installation instructions at [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

# Getting Started
## Part 1: Running MCP Server
1. Clone this repository
2. `cd horseracingnews`
3. Run `uv run horse_racing_news_mcp_server.py` and keep running.

## Part 2: Update Claude Desktop Configuration (assuming macOS)
1. Run `cd ~/Library/Application\ Support/Claude`
2. Use your favorite editor and open up `claude_desktop_config.json` (e.g., `vim claude_desktop_config.json`)
3. Assuming you never added an MCP server to the configuration file before, add:
```
{
  "mcpServers": {
    "horseracing": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/horseracingnews",
        "run",
        "horse_racing_news_mcp_server.py"
      ]
    }
  }
}
```

Make sure to restart Claude Desktop

# Source
* https://www.thoroughbreddailynews.com/feed/ (RSS)

# Prompts Used

```
I was informed of Thoroughbred Daily News yesterday. They provide an RSS feed at https://www.thoroughbreddailynews.com/feed/.  Can you write a Python program that:

Loads the feed
Parse the XML
For each story, show the title, content, and link
```

`Excellent, thanks so much!  Now, can you turn it into an MCP server using FastMCP? Expose one method for @mcp.tool() named get_horse_racing_news.`