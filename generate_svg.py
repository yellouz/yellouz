import os

# ========================================================
# 1. YOUR ASCII ART
# ========================================================
ASCII_ART = [
    r"                            __,,,__",
    r"                        _,g$        @g.",
    r"                      _g              g_",
    r"                     ,                  $_",
    r"                    g    $$$@$$$$@@@      w",
    r"                   _  $$ $$@$@$$$$$ $$$$",
    r"                   $ @@ $$$$$$$$@$$ @@$$  P",
    r"                     $       @@$$        L",
    r"                   J  $      $@ @",
    r"                  ,g $@         $        @,",
    r"                   &$$ $$ $  $ $@       $",
    r"                   $@$$$@$$ @&@$$$$@@@ $$$@",
    r"                    $@$@@$$ $@$$$$ $@  @@@",
    r"                     @ &$ @@$    $  $@$$",
    r"                     $@ @    @ $@$$ $   F",
    r"                      $@$ $$   $",
    r"                     _  $$$$$   $  @$$ g",
    r"                    y@@  $ $@@$$      @@@ ;",
    r"                  y @@@  @            @@@@@  r",
    r"              _gg  @@@@   $$$    $     @@@@@@ &gg_",
    r"        __,&   @   @@@@@@    @    $$  @@@@@@",
    r"    _gg     @@@   @$@@@@@@@         @@@@@@@@     @@@"
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
# 3. AUTO-CALIBRATION LOGIC
# ========================================================
def calibrate_ascii(lines):
    """Automatically strips unnecessary leading spaces and measures exact width."""
    cleaned_lines = [line.rstrip() for line in lines]
    non_empty = [line for line in cleaned_lines if line.strip()]
    
    if not non_empty:
        return cleaned_lines, 0
        
    # Find minimum leading whitespace across all lines
    min_leading = min(len(line) - len(line.lstrip()) for line in non_empty)
    
    # Strip common leading whitespace
    dedented_lines = [line[min_leading:] if len(line) >= min_leading else "" for line in cleaned_lines]
    
    # Get maximum character length
    max_char_len = max(len(line) for line in dedented_lines)
    
    return dedented_lines, max_char_len

# ========================================================
# 4. SVG THEMES & RENDERER
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

def build_svg(theme_name, ascii_lines, max_ascii_len):
    t = THEMES[theme_name]
    
    line_height = 20
    start_y = 35
    total_lines = max(len(ascii_lines), len(DETAILS) + 1)
    svg_height = start_y + (total_lines * line_height) + 20
    
    # --- Dynamic Positioning Calculations ---
    ascii_x = 25
    char_width_px = 7.8  # Width of 1 char in 13px JetBrains Mono / Consolas
    ascii_width_px = int(max_ascii_len * char_width_px)
    
    # Place stats column smoothly 35px after the ASCII art ends
    details_x = ascii_x + ascii_width_px + 35
    svg_width = details_x + 390  # Room for the stats text block
    
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
    for line in ascii_lines:
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
    print(f"Generated {filename} (Width: {svg_width}px, Stats X-offset: {details_x}px)")

if __name__ == "__main__":
    calibrated_art, max_len = calibrate_ascii(ASCII_ART)
    build_svg("dark", calibrated_art, max_len)
    build_svg("light", calibrated_art, max_len)