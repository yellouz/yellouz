import os

# ========================================================
# 1. YOUR NEW ASCII ART
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

# ========================================================
# 2. PROFILE DETAILS & STATS
# ========================================================
USERNAME = "yellouz"
TITLE = "youssef@ellouz"

DETAILS = [
    ("OS", "Linux / Windows 11"),
    ("Uptime", "22 years"),
    ("Host", "Data Analytics & Development"),
    ("IDE", "VS Code, Obsidian, Visual Studio"),
    ("Languages", "Python, C#, C++, Java"),
    ("Hobbies", "Gym, Chess, Self-hosting"),
    ("---", "------------------------------------------"),
    ("GitHub", f"github.com/{USERNAME}"),
    ("---", "------------------------------------------"),
    ("Repos", "15"),
    ("Commits", "1,420"),
    ("Stars", "48")
]

# ========================================================
# 3. CLEAN & SANITIZE ASCII ART
# ========================================================
# Replace non-breaking spaces (\xa0) with standard spaces and strip trailing whitespace
ASCII_ART = [line.replace("\xa0", " ").rstrip() for line in RAW_ASCII_ART]

# ========================================================
# 4. SVG THEMES & DYNAMIC RENDERER
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
    
    char_width_px = 7.8  # Character width in 13px JetBrains Mono / Consolas
    
    # --- 1. Left Column Calculations ---
    max_ascii_chars = max(len(line) for line in ASCII_ART)
    ascii_width_px = int(max_ascii_chars * char_width_px)
    ascii_x = 25
    
    # --- 2. Right Column Calculations ---
    gap_between_columns = 35
    details_x = ascii_x + ascii_width_px + gap_between_columns
    
    # Find the maximum character width of any line in the details column
    max_detail_chars = len(f"{TITLE} ------------------------------------------")
    for label, val in DETAILS:
        if label == "---":
            max_detail_chars = max(max_detail_chars, len(val))
        else:
            dots_count = max(1, 18 - len(label))
            line_len = len(label) + 2 + dots_count + 1 + len(val)
            max_detail_chars = max(max_detail_chars, line_len)
            
    details_width_px = int(max_detail_chars * char_width_px)
    right_padding = 30
    
    # Dynamic SVG Total Width
    svg_width = details_x + details_width_px + right_padding
    
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
        
    # Render Title (Right)
    current_y = start_y
    divider = "-" * (40 - len(TITLE))
    svg_lines.append(f'  <text x="{details_x}" y="{current_y}" class="base title">{escape_xml(TITLE)} <tspan class="label">{divider}</tspan></text>')
    current_y += line_height
    
    # Render Details (Right)
    for label, val in DETAILS:
        if label == "---":
            svg_lines.append(f'  <text x="{details_x}" y="{current_y}" class="base label">{val}</text>')
        else:
            dots = "." * max(1, (18 - len(label)))
            svg_lines.append(
                f'  <text x="{details_x}" y="{current_y}" class="base">'
                f'<tspan class="label">{escape_xml(label)}: </tspan>'
                f'<tspan class="label">{dots} </tspan>'
                f'<tspan class="value">{escape_xml(val)}</tspan>'
                f'</text>'
            )
        current_y += line_height
        
    svg_lines.append('</svg>')
    
    filename = f"neofetch-{theme_name}.svg"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"Generated {filename} (Card Width: {svg_width}px, Stats Offset: {details_x}px)")

if __name__ == "__main__":
    build_svg("dark")
    build_svg("light")