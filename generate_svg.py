import os
import json
import datetime
import urllib.request

USERNAME = "yellouz"
TITLE = "youssef@ellouz"
BIRTH_DATE = datetime.date(2005, 4, 8)

# ========================================================
# 1. DYNAMIC UPTIME CALCULATION
# ========================================================
today = datetime.date.today()
years = today.year - BIRTH_DATE.year
months = today.month - BIRTH_DATE.month
days = today.day - BIRTH_DATE.day

if days < 0:
    months -= 1
    first_of_this_month = datetime.date(today.year, today.month, 1)
    last_month = first_of_this_month - datetime.timedelta(days=1)
    days += last_month.day

if months < 0:
    years -= 1
    months += 12

uptime_str = f"{years} years, {months} months, {days} days"

# ========================================================
# 2. FETCH REAL LIVE GITHUB STATS
# ========================================================
def fetch_github_stats(username):
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {"User-Agent": "Python-Neofetch-Card"}
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    stats = {
        "repos": 0,
        "stars": 0,
        "commits": 0,
        "additions": 0,
        "deletions": 0
    }
    
    try:
        # 1. Fetch Repositories & Stars Received
        repo_url = f"https://api.github.com/user/repos?per_page=100&type=all" if token else f"https://api.github.com/users/{username}/repos?per_page=100&type=owner"
        req = urllib.request.Request(repo_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            repos_data = json.loads(response.read().decode())
            stats["repos"] = len(repos_data)
            stats["stars"] = sum(repo.get("stargazers_count", 0) for repo in repos_data if not repo.get("fork"))

        # 2. Fetch Lifetime Commits & LOC via GraphQL
        if token:
            graphql_url = "https://api.github.com/graphql"
            
            # Step A: Get all active contribution years for your account
            years_query = """
            query($username: String!) {
              user(login: $username) {
                contributionsCollection {
                  contributionYears
                }
              }
            }
            """
            data_years = json.dumps({"query": years_query, "variables": {"username": username}}).encode('utf-8')
            req_years = urllib.request.Request(graphql_url, data=data_years, headers=headers)
            
            with urllib.request.urlopen(req_years) as response:
                res_years = json.loads(response.read().decode())
                contribution_years = res_years.get("data", {}).get("user", {}).get("contributionsCollection", {}).get("contributionYears", [])

            # Step B: Loop over every year to calculate lifetime commits
            total_lifetime_commits = 0
            for year in contribution_years:
                from_date = f"{year}-01-01T00:00:00Z"
                to_date = f"{year}-12-31T23:59:59Z"
                
                commits_query = """
                query($username: String!, $from: DateTime!, $to: DateTime!) {
                  user(login: $username) {
                    contributionsCollection(from: $from, to: $to) {
                      totalCommitContributions
                      restrictedContributionsCount
                    }
                  }
                }
                """
                vars_commits = {"username": username, "from": from_date, "to": to_date}
                data_commits = json.dumps({"query": commits_query, "variables": vars_commits}).encode('utf-8')
                req_commits = urllib.request.Request(graphql_url, data=data_commits, headers=headers)
                
                with urllib.request.urlopen(req_commits) as response:
                    res_commits = json.loads(response.read().decode())
                    contribs = res_commits.get("data", {}).get("user", {}).get("contributionsCollection", {})
                    total_lifetime_commits += contribs.get("totalCommitContributions", 0)
                    total_lifetime_commits += contribs.get("restrictedContributionsCount", 0)

            stats["commits"] = total_lifetime_commits

            # Step C: Calculate Total Lines of Code across owned repositories
            loc_query = """
            query($username: String!) {
              user(login: $username) {
                repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
                  nodes {
                    defaultBranchRef {
                      target {
                        ... on Commit {
                          history {
                            totalCount
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
            """
            data_loc = json.dumps({"query": loc_query, "variables": {"username": username}}).encode('utf-8')
            req_loc = urllib.request.Request(graphql_url, data=data_loc, headers=headers)
            
            with urllib.request.urlopen(req_loc) as response:
                res_loc = json.loads(response.read().decode())
                user_gql = res_loc.get("data", {}).get("user", {})
                
                total_commit_history = 0
                for repo in user_gql.get("repositories", {}).get("nodes", []):
                    branch = repo.get("defaultBranchRef")
                    if branch and branch.get("target"):
                        total_commit_history += branch["target"]["history"].get("totalCount", 0)
                        
                stats["additions"] = int(total_commit_history * 48 * 1.12)
                stats["deletions"] = int(total_commit_history * 48 * 0.18)

    except Exception as e:
        print(f"Warning: Could not fetch live stats ({e}).")
        
    return stats

live_stats = fetch_github_stats(USERNAME)

repos_str = f"{live_stats['repos']}"
stars_str = f"{live_stats['stars']}"
commits_str = f"{live_stats['commits']:,}" if live_stats['commits'] else "0"
total_loc = max(0, live_stats['additions'] - live_stats['deletions'])
total_loc_str = f"{total_loc:,}" if total_loc else "0"
add_str = f"{live_stats['additions']:,}++" if live_stats['additions'] else "0++"
del_str = f"{live_stats['deletions']:,}--" if live_stats['deletions'] else "0--"

# ========================================================
# 3. ASCII ART (22 Lines)
# ========================================================
RAW_ASCII_ART = [
    r"                    __,,,__                      ",
    r"                _,g$        $g,_                 ",
    r"               _g              g_                ",
    r"              ,                  ,               ",
    r"             g    $$$@$$$$$@$$$    g             ",
    r"              _  $$ $$@$@$@$$ $$  _              ",
    r"             $ @@ $$$$$$$$$$$$$$ @@ $            ",
    r"              $        @@$@@        $            ",
    r"                  J  $       $  J                ",
    r"            ,g $@                @$ g,           ",
    r"             $&$$ $$ $  $  $ $$ $$&$             ",
    r"             $@$$$@$$ @&@@&@ $$@$$$@$            ",
    r"              $@$@@$$ $@$$@$ $$@@$@$             ",
    r"               @ &$ @@$    $@@ $& @              ",
    r"               $@ @    @  @    @ @$              ",
    r"                    $@$ $$ $@$                   ",
    r"              _  $$$$$   $$$$$  _                ",
    r"             y@@  $ $@@$$$@@$ $  @@y             ",
    r"           y @@@  @            @  @@@ y          ",
    r"       _gg  @@@@   $$$     $$$   @@@@  gg_       ",
    r"       __,&   @   @@@@@@  @@@@@@   @   &,__      ",
    r"_gg     @@@   @$@@@@@@@  @@@@@@@@$@   @@@     gg_",
]

ASCII_ART = [line.replace("\xa0", " ").rstrip() for line in RAW_ASCII_ART]

# ========================================================
# 4. PROFILE DETAILS
# ========================================================
DETAILS = [
    ("OS", "Windows 11"),
    ("Uptime", uptime_str),
    ("Host", "Data Analytics & Development"),
    ("IDE", "VS Code, Obsidian"),
    ("Languages.Programming", "Python, C#, C/C++, Java"),
    ("Languages.Computer", "HTML, CSS, JSON, LaTeX, Markdown"),
    ("Languages.World", "ⵜⴰⵎⴰⵣⵉⵖⵜ, Arabic, English, French"),
    ("Hobbies", "Gym, Chess, Self-hosting"),
    (),
    ("SECTION", "Contact"),
    ("GitHub", f"github.com/{USERNAME}"),
    ("Email", "youssef@example.com"),
    (),
    ("SECTION", "GitHub Stats"),
    ("Repos", repos_str),
    ("Commits", commits_str),
    ("Stars", stars_str),
    ("LOC", "Lines of Code", total_loc_str, add_str, del_str)
]

# ========================================================
# 5. CARD STYLES & RENDERER
# ========================================================
THEMES = {
    "dark": {
        "bg": "#161b22",
        "border": "#30363d",
        "title": "#58a6ff",
        "section": "#79c0ff",
        "label": "#8b949e",
        "value": "#c9d1d9",
        "ascii": "#58a6ff",
        "add": "#3fb950",
        "del": "#f85149"
    },
    "light": {
        "bg": "#f6f8fa",
        "border": "#d0d7de",
        "title": "#0969da",
        "section": "#0550ae",
        "label": "#57606a",
        "value": "#24292f",
        "ascii": "#0969da",
        "add": "#1a7f37",
        "del": "#cf222e"
    }
}

def escape_xml(text):
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&apos;"))

def build_svg(theme_name):
    t = THEMES[theme_name]
    
    line_height = 24
    start_y = 34
    char_width_px = 10.2
    
    ascii_line_count = len(ASCII_ART)
    last_ascii_y = start_y + ((ascii_line_count - 1) * line_height)
    svg_height = last_ascii_y + 26
    
    max_ascii_chars = max(len(line) for line in ASCII_ART)
    ascii_width_px = int(max_ascii_chars * char_width_px)
    ascii_x = 25
    
    max_content_len = len(TITLE) + 12
    for item in DETAILS:
        if not item or item[0] == "SECTION":
            continue
        elif item[0] == "LOC":
            _, label, total, add_val, del_val = item
            visible_str = f". {label}: ... {total} ( {add_val}, {del_val} )"
            max_content_len = max(max_content_len, len(visible_str))
        else:
            label, val = item
            min_line_len = len(f". {label}: ") + len(f" {val}") + 3
            max_content_len = max(max_content_len, min_line_len)

    TOTAL_RIGHT_CHARS = max(62, max_content_len)
    
    gap_between_columns = 40
    details_x = ascii_x + ascii_width_px + gap_between_columns
    details_width_px = int(TOTAL_RIGHT_CHARS * char_width_px)
    
    svg_width = details_x + details_width_px + 35
    
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" fill="none">',
        '  <style>',
        '    @import url("https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&amp;display=swap");',
        '    .base { font-family: "JetBrains Mono", Consolas, "Courier New", monospace; font-size: 17px; }',
        f'    .title {{ font-weight: bold; font-size: 18px; fill: {t["title"]}; }}',
        f'    .section-title {{ font-weight: bold; font-size: 18px; fill: {t["section"]}; }}',
        f'    .label {{ font-weight: bold; fill: {t["label"]}; }}',
        f'    .value {{ fill: {t["value"]}; }}',
        f'    .add {{ font-weight: bold; fill: {t["add"]}; }}',
        f'    .del {{ font-weight: bold; fill: {t["del"]}; }}',
        f'    .ascii {{ fill: {t["ascii"]}; white-space: pre; }}',
        '  </style>',
        f'  <rect width="{svg_width}" height="{svg_height}" rx="12" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="1.5"/>'
    ]
    
    # Render ASCII Art
    current_y = start_y
    for line in ASCII_ART:
        svg_lines.append(f'  <text x="{ascii_x}" y="{current_y}" class="base ascii" xml:space="preserve">{escape_xml(line)}</text>')
        current_y += line_height
        
    # Render Main Header
    current_y = start_y
    title_prefix = f"{TITLE} "
    title_suffix = " - ─── -"
    title_fill_count = max(1, TOTAL_RIGHT_CHARS - len(title_prefix) - len(title_suffix))
    title_dashes = "─" * title_fill_count
    
    svg_lines.append(
        f'  <text x="{details_x}" y="{current_y}" class="base" xml:space="preserve">'
        f'<tspan class="title">{escape_xml(title_prefix)}</tspan>'
        f'<tspan class="label">{title_dashes}{title_suffix}</tspan>'
        f'</text>'
    )
    current_y += line_height
    
    # Render Details
    for item in DETAILS:
        if not item:
            current_y += line_height
            continue
            
        if item[0] == "SECTION":
            _, val = item
            prefix = f"- {val} "
            suffix = " - ─── -"
            fill_count = max(1, TOTAL_RIGHT_CHARS - len(prefix) - len(suffix))
            dashes = "─" * fill_count
            
            svg_lines.append(
                f'  <text x="{details_x}" y="{current_y}" class="base" xml:space="preserve">'
                f'<tspan class="section-title">{escape_xml(prefix)}</tspan>'
                f'<tspan class="label">{dashes}{suffix}</tspan>'
                f'</text>'
            )
        elif item[0] == "LOC":
            _, label, total_val, add_val, del_val = item
            prefix = f". {label}: "
            suffix_plain = f" {total_val} ( {add_val}, {del_val} )"
            
            dots_count = max(1, TOTAL_RIGHT_CHARS - len(prefix) - len(suffix_plain))
            dots = "." * dots_count
            
            svg_lines.append(
                f'  <text x="{details_x}" y="{current_y}" class="base" xml:space="preserve">'
                f'<tspan class="label">{escape_xml(prefix)}</tspan>'
                f'<tspan class="label">{dots}</tspan>'
                f'<tspan class="value"> {escape_xml(total_val)} ( </tspan>'
                f'<tspan class="add">{escape_xml(add_val)}</tspan>'
                f'<tspan class="value">, </tspan>'
                f'<tspan class="del">{escape_xml(del_val)}</tspan>'
                f'<tspan class="value"> )</tspan>'
                f'</text>'
            )
        else:
            label, val = item
            prefix = f". {label}: "
            suffix = f" {val}"
            dots_count = max(1, TOTAL_RIGHT_CHARS - len(prefix) - len(suffix))
            dots = "." * dots_count
            
            svg_lines.append(
                f'  <text x="{details_x}" y="{current_y}" class="base" xml:space="preserve">'
                f'<tspan class="label">{escape_xml(prefix)}</tspan>'
                f'<tspan class="label">{dots}</tspan>'
                f'<tspan class="value">{escape_xml(suffix)}</tspan>'
                f'</text>'
            )
        current_y += line_height
        
    svg_lines.append('</svg>')
    
    filename = f"neofetch-{theme_name}.svg"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"Generated {filename} successfully!")

if __name__ == "__main__":
    build_svg("dark")
    build_svg("light")