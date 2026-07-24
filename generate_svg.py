import os
import datetime

# ========================================================
# 1. DYNAMIC EXACT UPTIME (April 8, 2005)
# ========================================================
BIRTH_DATE = datetime.date(2005, 4, 8)
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
# 2. YOUR ASCII ART (22 Lines)
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
# 3. PROFILE DETAILS & STATS
# ========================================================
USERNAME = "yellouz"
TITLE = "youssef@ellouz"

# Format for special LOC tuple: ("LOC", "Label", "Total Lines", "Additions++", "Deletions--")
DETAILS = [
    ("OS", "Linux / Windows 11"),
    ("Uptime", uptime_str),
    ("Host", "Data Analytics & Development"),
    ("IDE", "VS Code, Obsidian, Visual Studio"),
    ("Languages", "Python, C#, C++, Java"),
    ("Hobbies", "Gym, Chess, Self-hosting"),
    (),
    ("SECTION", "Contact"),
    ("GitHub", f"github.com/{USERNAME}"),
    ("Email", "youssef@example.com"),
    (),
    ("SECTION", "GitHub Stats"),
    ("Repos", "15"),
    ("Commits", "1,420"),
    ("Stars", "48"),  # Stars received on your repos
    ("LOC", "Lines of Code", "446,276", "523,178++", "76,902--")
]

# ========================================================
# 4. CARD THEMES & STYLES
# ========================================================
THEMES = {
    "dark": {
        "bg": "#161b22",        # GitHub elevated card dark slate
        "border": "#30363d",
        "title": "#58a6ff",     # Title Accent
        "section": "#79c0ff",   # Section Header Accent
        "label": "#8b949e",     # Muted Gray
        "value": "#c9d1d9",     # Off-White Values
        "ascii": "#58a6ff",     # ASCII Accent
        "add": "#3fb950",       # Green for Additions (++)
        "del": "#f85149"        # Red for Deletions (--)
    },
    "light": {
        "bg": "#f6f8fa",        # GitHub elevated card light grey
        "border": "#d0d7de",
        "title": "#0969da",
        "section": "#0550ae",
        "label": "#57606a",
        "value": "#24292f",
        "ascii": "#0969da",
        "add": "#1a7f37",       # Darker Green for Light Mode
        "del": "#cf222e"        # Darker Red for Light Mode
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
    char_width_px = 10.2  # Character width in 17px JetBrains Mono
    
    # Strictly bound height to 22-line ASCII Art length
    ascii_line_count = len(ASCII_ART)
    last_ascii_y = start_y + ((ascii_line_count - 1) * line_height)
    svg_height = last_ascii_y + 26
    
    # Left Column Width
    max_ascii_chars = max(len(line) for line in ASCII_ART)
    ascii_width_px = int(max_ascii_chars * char_width_px)
    ascii_x = 25
    
    # Calculate Required Character Width for Right Column
    max_content_len = len(TITLE) + 12
    for item in DETAILS:
        if not item:
            continue
        if item[0] == "SECTION":
            continue
        elif item[0] == "LOC":
            _, label, total, add_val, del_val = item
            visible_str = f". {label}: ... {total} ( {add_val}, {del_val} )"
            max_content_len = max(max_content_len, len(visible_str))
        else:
            label, val = item
            min_line_len = len(f". {label}: ") + len(f" {val}") + 3
            max_content_len = max(max_content_len, min_line_len)

    TOTAL_RIGHT_CHARS = max(60, max_content_len)
    
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
    
    # Render ASCII Art (Left Column)
    current_y = start_y
    for line in ASCII_ART:
        svg_lines.append(f'  <text x="{ascii_x}" y="{current_y}" class="base ascii" xml:space="preserve">{escape_xml(line)}</text>')
        current_y += line_height
        
    # Render Main Title Header (Right Column)
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
    
    # Render Details & Section Dividers
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