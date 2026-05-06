from datetime import datetime
import pandas as pd


def generate_report(visual_type: str, analysis: str, df) -> str:
    table_html = ""
    if df is not None:
        table_html = df.to_html(index=False, classes="data-table", border=0)

    timestamp = datetime.now().strftime("%B %d, %Y at %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Visual Analysis Report</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: system-ui, -apple-system, sans-serif;
    background: #08080f;
    color: #c8c0f0;
    min-height: 100vh;
    padding: 40px 20px;
  }}
  .container {{
    max-width: 860px;
    margin: 0 auto;
  }}
  .header {{
    border-bottom: 1px solid #1a1a2e;
    padding-bottom: 24px;
    margin-bottom: 32px;
  }}
  .logo {{
    font-size: 13px;
    color: #4a4a6a;
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 1.2px;
  }}
  h1 {{
    font-size: 28px;
    font-weight: 600;
    color: #e8e0ff;
    margin-bottom: 8px;
  }}
  .timestamp {{
    font-size: 12px;
    color: #4a4a6a;
  }}
  .badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #16162a;
    border: 0.5px solid #2a2a4a;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 12px;
    color: #a89fcc;
    margin-bottom: 28px;
  }}
  .badge-dot {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #6c63ff;
  }}
  .section {{
    background: #0c0c18;
    border: 0.5px solid #1a1a2e;
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 20px;
  }}
  .section-label {{
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #3a3a5a;
    margin-bottom: 14px;
  }}
  .analysis-text {{
    font-size: 15px;
    color: #8a88a0;
    line-height: 1.8;
  }}
  .data-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }}
  .data-table th {{
    background: #16162a;
    color: #a89fcc;
    padding: 10px 14px;
    text-align: left;
    font-weight: 500;
    border-bottom: 1px solid #2a2a4a;
  }}
  .data-table td {{
    padding: 10px 14px;
    color: #6a6888;
    border-bottom: 1px solid #16162a;
  }}
  .data-table tr:last-child td {{
    border-bottom: none;
  }}
  .footer {{
    margin-top: 40px;
    text-align: center;
    font-size: 11px;
    color: #2a2a4a;
    padding-top: 20px;
    border-top: 1px solid #1a1a2e;
  }}
</style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="logo">Visual Analyst Agent · Powered by Gemini</div>
      <h1>Analysis Report</h1>
      <div class="timestamp">Generated {timestamp}</div>
    </div>

    <div class="badge">
      <div class="badge-dot"></div>
      {visual_type}
    </div>

    <div class="section">
      <div class="section-label">Trend Analysis</div>
      <div class="analysis-text">{analysis}</div>
    </div>

    {f'''<div class="section">
      <div class="section-label">Extracted Data</div>
      {table_html}
    </div>''' if table_html else ""}

    <div class="footer">
      Visual Analyst Agent &nbsp;·&nbsp; Powered by Gemini &nbsp;·&nbsp; {timestamp}
    </div>
  </div>
</body>
</html>"""

    return html
