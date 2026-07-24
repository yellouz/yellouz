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
# 2. YOUR ASCII ART
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

DETAILS = [
    ("OS", "Linux / Windows 11"),
    ("Uptime", uptime_str),
    ("Host", "Data Analytics & Development"),
    ("IDE", "VS Code, Obsidian, Visual Studio"),
    ("Languages", "Python, C#, C++, Java"),
    ("Hobbies", "Gym, Chess, Self-hosting"),
    ("SECTION", "Contact"),
    ("GitHub", f"github.com/{USERNAME}"),
    ("Email", "youssef@example.com"),
    ("SECTION", "GitHub Stats"),
    ("Repos", "15"),
    ("Commits", "1,420"),
    ("Stars", "48")
]

# ========================================================
# 4. CARD THEMES & ELEGANT BACKGROUNDS
# ========================================================
THEMES = {
    "dark": {
        "bg": "#161b22",        # GitHub's elevated card dark slate-grey
        "border": "#30363d",    # Card border
        "title": "#58a6ff",     # Light Blue Header Accent
        "section": "#79c0ff",   # Section Header Accent
        "label": "#8b949e",     # Muted Gray Labels
        "value": "#c9d1d9",     # Clean Off-White Values
        "ascii": "#58a6ff"      # ASCII Portrait Accent
    },
    "light": {
        "bg": "#f6f8fa",        # GitHub's elevated card light grey
        "border": "#d0d7de",
        "title": "#0969da",
        "section": "#0550ae",
        "label": "#57606a",
        "value": "#24292f",
        "ascii": "#0969da"
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
    
    line_height = 20
    start_y = 35
    
    # Measure column lengths
    ascii_line_count = len(ASCII_ART)
    details_line_count = len(DETAILS) + 1  # Including title
    
    # Calculate vertical spacing adjustment to stretch details column evenly
    num_sections = sum(1 for label, _ in DETAILS if label == "SECTION")
    height_difference = max(0, (ascii_line_count - details_line_count) * line_height)
    
    # Distribute the height gap evenly before section dividers
    extra_section_padding = height_difference // max(1, num_sections)
    
    total_lines = max(ascii_line_count, details_line_count)
    svg_height = start_y + (total_lines * line_height) + height_difference + 20
    
    char_width_px = 7.8
    
    # Left Column Width
    max_ascii_chars = max(len(line) for line in ASCII_ART)
    ascii_width_px = int(max_ascii_chars * char_width_px)
    ascii_x = 25
    
    # Right Column Width Calculation
    max_content_len = len(TITLE) + 10
    for item in DETAILS:
        label, val = item
        if label != "SECTION":
            min_line_len = len(f". {label}: ") + len(f" {val}") + 3
            if min_line_len > max_content_len:
                max_content_len = min_line_len

    TOTAL_RIGHT_CHARS = max(58, max_content_len)
    
    gap_between_columns = 35
    details_x = ascii_x + ascii_width_px + gap_between_columns
    details_width_px = int(TOTAL_RIGHT_CHARS * char_width_px)
    
    svg_width = details_x + details_width_px + 30
    
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" fill="none">',
        '  <style>',
        '    .base { font-family: "JetBrains Mono", Consolas, "Courier New", monospace; font-size: 13px; }',
        f'    .title {{ font-weight: bold; font-size: 14px; fill: {t["title"]}; }}',
        f'    .section-title {{ font-weight: bold; font-size: 14px; fill: {t["section"]}; }}',
        f'    .label {{ font-weight: bold; fill: {t["label"]}; }}',
        f'    .value {{ fill: {t["value"]}; }}',
        f'    .ascii {{ fill: {t["ascii"]}; white-space: pre; }}',
        '  </style>',
        f'  <rect width="{svg_width}" height="{svg_height}" rx="12" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="1.5"/>'
    ]
    
    # Render ASCII Art (Left)
    current_y = start_y
    for line in ASCII_ART:
        svg_lines.append(f'  <text x="{ascii_x}" y="{current_y}" class="base ascii" xml:space="preserve">{escape_xml(line)}</text>')
        current_y += line_height
        
    # Render Title (Right Header)
    current_y = start_y
    title_dashes = "-" * (TOTAL_RIGHT_CHARS - len(TITLE) - 1)
    svg_lines.append(f'  <text x="{details_x}" y="{current_y}" class="base title">{escape_xml(TITLE)} <tspan class="label">{title_dashes}</tspan></text>')
    current_y += line_height
    
    # Render Details with Dynamic Vertical Padding
    for label, val in DETAILS:
        if label == "SECTION":
            current_y += extra_section_padding
            prefix = f"- {val} "
            dashes = "-" * max(1, TOTAL_RIGHT_CHARS - len(prefix))
            svg_lines.append(
                f'  <text x="{details_x}" y="{current_y}" class="base" xml:space="preserve">'
                f'<tspan class="section-title">{escape_xml(prefix)}</tspan>'
                f'<tspan class="label">{dashes}</tspan>'
                f'</text>'
            )
        else:
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