import os

# ========================================================
# 1. YOUR ASCII ART
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
# 2. PROFILE DETAILS & STATS (With Sections)
# ========================================================
USERNAME = "yellouz"
TITLE = "youssef@ellouz"

# Use ("SECTION", "Section Name") to create divider bars like - Contact -----------
DETAILS = [
    ("OS", "Linux / Windows 11"),
    ("Uptime", "22 years"),
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
# 3. SVG THEMES & RIGHT-ALIGNMENT RENDERER
# ========================================================
THEMES = {
    "dark": {
        "bg": "#0d1117",
        "border": "#30363d",
        "title": "#58a6ff",
        "label": "#8b949e",
        "value": "#c9d1d9",
        "ascii": "#58a6ff"
    },
    "light": {
        "bg": "#ffffff",
        "border": "#d0d7de",
        "title": "#0969da",
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
    total_lines = max(len(ASCII_ART), len(DETAILS) + 1)
    svg_height = start_y + (total_lines * line_height) + 20
    
    char_width_px = 7.8  # Character width in 13px JetBrains Mono
    
    # --- 1. Left Column Calculations ---
    max_ascii_chars = max(len(line) for line in ASCII_ART)
    ascii_width_px = int(max_ascii_chars * char_width_px)
    ascii_x = 25
    
    # --- 2. Calculate Fixed Line Width for Right Column ---
    # Find longest content to set a uniform TOTAL_RIGHT_CHARS width
    max_content_len = len(TITLE) + 10
    for item in DETAILS:
        label, val = item
        if label != "SECTION":
            min_line_len = len(f". {label}: ") + len(f" {val}") + 3  # label + min 3 dots + val
            if min_line_len > max_content_len:
                max_content_len = min_line_len

    # Set total column width (at least 56 characters wide)
    TOTAL_RIGHT_CHARS = max(56, max_content_len)
    
    gap_between_columns = 35
    details_x = ascii_x + ascii_width_px + gap_between_columns
    details_width_px = int(TOTAL_RIGHT_CHARS * char_width_px)
    
    # Dynamic Card Width
    svg_width = details_x + details_width_px + 30
    
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" fill="none">',
        '  <style>',
        '    .base { font-family: "JetBrains Mono", Consolas, "Courier New", monospace; font-size: 13px; }',
        f'    .title {{ font-weight: bold; fill: {t["title"]}; }}',
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
    
    # Render Details with Dynamic Dot Fill for Right Alignment
    for label, val in DETAILS:
        if label == "SECTION":
            # Render section divider e.g. - Contact -----------------------
            dashes = "-" * (TOTAL_RIGHT_CHARS - len(val) - 3)
            svg_lines.append(f'  <text x="{details_x}" y="{current_y}" class="base label">- {escape_xml(val)} {dashes}</text>')
        else:
            prefix = f". {label}: "
            suffix = f" {val}"
            
            # Calculate exactly how many dots are needed to reach TOTAL_RIGHT_CHARS
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
    print(f"Generated {filename} (Total Right Column Width: {TOTAL_RIGHT_CHARS} chars)")

if __name__ == "__main__":
    build_svg("dark")
    build_svg("light")