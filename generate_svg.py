import os

# ========================================================
# 1. YOUR CLEANED ASCII ART
# ========================================================
ASCII_ART = [
    r"                         __,,,__",
    r"                    _,g$        @g.",
    r"                  _g              g_",
    r"                 ,                  $_",
    r"                g    $$$@$$$$@@@      w",
    r"               _  $$ $$@$@$$$$$ $$$$",
    r"               $ @@ $$$$$$$$@$$ @@$$  P",
    r"                 $       @@$$        L",
    r"               J  $      $@ @",
    r"              ,g $@         $        @,",
    r"               &$$ $$ $  $ $@       $",
    r"               $@$$$@$$ @&@$$$$@@@ $$$@",
    r"                $@$@@$$ $@$$$$ $@  @@@",
    r"                 @ &$ @@$    $  $@$$",
    r"                 $@ @    @ $@$$ $   F",
    r"                  $@$ $$   $",
    r"                 _  $$$$$   $  @$$ g",
    r"                y@@  $ $@@$$      @@@ ;",
    r"              y @@@  @            @@@@@  r",
    r"          _gg  @@@@   $$$    $     @@@@@@ &gg_",
    r"    __,&   @   @@@@@@    @    $$  @@@@@@",
    r"_gg     @@@   @$@@@@@@@         @@@@@@@@     @@@"
]

# ========================================================
# 2. PROFILE DETAILS & STATS
# ========================================================
USERNAME = "yellouz"
TITLE = "youssef@ellouz"

DETAILS = [
    ("OS", "Windows 11"),
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
# 3. SVG THEMES & RENDERER
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
    """Safely escapes XML characters so SVG parsers never throw errors."""
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
    svg_width = 860  # Widen to comfortably fit ASCII art + stats
    
    ascii_x = 20
    details_x = 380  # X offset for the right column
    
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
    
    # Render Details
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
    print(f"Generated {filename} successfully!")

if __name__ == "__main__":
    build_svg("dark")
    build_svg("light")