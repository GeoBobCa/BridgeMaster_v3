# src/pbn_to_html.py
import sys
from pathlib import Path

# --- PATH SETUP ---
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
INPUT_FILE = PROJECT_ROOT / "output" / "generated_hands.pbn"
OUTPUT_FILE = PROJECT_ROOT / "output" / "lesson_hands.html"

HTML_HEADER = """
<!DOCTYPE html>
<html>
<head>
    <title>BridgeMaster Lessons</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #f0f2f5; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; }
        .hand-record { 
            background: white; 
            border-left: 6px solid #00563f;
            margin-bottom: 40px; 
            padding: 25px; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-radius: 8px;
        }
        .header { border-bottom: 1px solid #eee; margin-bottom: 20px; padding-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
        .header h2 { margin: 0; color: #1a1a1a; font-size: 1.4em; }
        .header span { background: #eef; color: #446; padding: 4px 8px; border-radius: 4px; font-size: 0.85em; font-weight: bold; }

        /* Grid Layout */
        .board-layout { display: grid; grid-template-columns: 1.2fr 1fr 1.2fr; gap: 20px; }
        
        .hands-area { grid-column: 1 / 3; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }
        .north { grid-column: 2; text-align: center; }
        .west { grid-column: 1; grid-row: 2; }
        .center-img { grid-column: 2; grid-row: 2; display: flex; justify-content: center; align-items: center; background: #e8f5e9; border-radius: 4px; color: #00563f; font-weight: bold; border: 1px solid #cce5d0; }
        .east { grid-column: 3; grid-row: 2; text-align: right; }
        .south { grid-column: 2; grid-row: 3; text-align: center; }

        .auction-area { grid-column: 3; background: #fafafa; padding: 15px; border-radius: 6px; border: 1px solid #eee; }
        
        .hand-box { padding: 8px; font-size: 0.95em; }
        .hand-box strong { display: block; margin-bottom: 4px; color: #555; text-transform: uppercase; font-size: 0.75em; letter-spacing: 1px; }
        .holding { font-family: 'Consolas', monospace; font-size: 1.1em; }

        .suit-S, .suit-C { color: #222; }
        .suit-H, .suit-D { color: #d32f2f; }
        .symbol { width: 18px; display: inline-block; text-align: center; }

        table.auction { width: 100%; border-collapse: collapse; font-size: 0.95em; margin-bottom: 15px; }
        table.auction th { border-bottom: 2px solid #ddd; padding: 6px; color: #444; }
        table.auction td { padding: 6px; text-align: center; border-bottom: 1px solid #f0f0f0; }

        /* Logic Explanations */
        .logic-section { grid-column: 1 / -1; margin-top: 20px; padding-top: 15px; border-top: 1px dashed #ccc; }
        .logic-section h3 { margin: 0 0 10px 0; font-size: 1em; color: #00563f; }
        .logic-list { list-style: none; padding: 0; margin: 0; }
        .logic-list li { margin-bottom: 8px; padding-left: 20px; position: relative; color: #444; }
        .logic-list li::before { content: "•"; color: #00563f; font-weight: bold; position: absolute; left: 0; }
        .logic-bid { font-weight: bold; color: #000; background: #e8f5e9; padding: 2px 6px; border-radius: 4px; margin-right: 8px; border: 1px solid #c8e6c9; }
    </style>
</head>
<body>
<div class="container">
    <h1 style="text-align:center; color:#00563f; margin-bottom: 40px;">BridgeMaster: Logic Analysis</h1>
"""

HTML_FOOTER = """
</div>
</body>
</html>
"""

def format_suit_html(suit_char, cards_str):
    symbols = {'S': '&spades;', 'H': '&hearts;', 'D': '&diams;', 'C': '&clubs;'}
    suit_class = f"suit-{suit_char}"
    return f"<div class='holding {suit_class}'><span class='symbol'>{symbols[suit_char]}</span>{cards_str}</div>"

def parse_pbn_hand(pbn_hand_str):
    suits = pbn_hand_str.split('.')
    return [format_suit_html('S', suits[0]), format_suit_html('H', suits[1]), 
            format_suit_html('D', suits[2]), format_suit_html('C', suits[3])]

def parse_pbn_file(file_path):
    deals = []
    current_deal = {}
    in_auction = False
    auction_lines = []

    with file_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if not line:
            if in_auction and auction_lines:
                current_deal['bidding'] = " ".join(auction_lines)
                deals.append(current_deal)
                current_deal = {}
                in_auction = False
                auction_lines = []
            continue

        if line.startswith('[Event'):
            current_deal['event'] = line.split('"')[1]
        elif line.startswith('[Deal'):
            content = line.split('"')[1]
            if content.startswith("N:"):
                hands = content[2:].split(' ')
                current_deal['north'] = parse_pbn_hand(hands[0])
                current_deal['east'] = parse_pbn_hand(hands[1])
                current_deal['south'] = parse_pbn_hand(hands[2])
                current_deal['west'] = parse_pbn_hand(hands[3])
        elif line.startswith('[Note'):
            current_deal['note'] = line.split('"')[1]
        elif line.startswith('[Auction'):
            current_deal['dealer'] = line.split('"')[1]
            in_auction = True
        elif in_auction:
            auction_lines.append(line)
             
    if current_deal and 'north' in current_deal:
        if in_auction: current_deal['bidding'] = " ".join(auction_lines)
        deals.append(current_deal)

    return deals

def generate_hand_html(deal, index):
    def show(hand_list): return "".join(hand_list)

    # Format Auction
    bids = deal.get('bidding', '').split()
    auction_rows = ""
    row = []
    for bid in bids:
        row.append(bid)
        if len(row) == 4:
            auction_rows += f"<tr><td>{'</td><td>'.join(row)}</td></tr>"
            row = []
    if row:
        auction_rows += f"<tr><td>{'</td><td>'.join(row)}</td></tr>"

    # Format Logic Explanations
    logic_html = ""
    raw_note = deal.get('note', '')
    if raw_note:
        logic_html = '<div class="logic-section"><h3>Why did they bid that?</h3><ul class="logic-list">'
        parts = raw_note.split('|')
        for part in parts:
            if ':' in part:
                bid, expl = part.split(':', 1)
                logic_html += f'<li><span class="logic-bid">{bid.strip()}</span> {expl.strip()}</li>'
            else:
                logic_html += f'<li>{part.strip()}</li>'
        logic_html += '</ul></div>'

    return f"""
    <div class="hand-record">
        <div class="header">
            <h2>Hand #{index}</h2>
            <span>{deal.get('event', 'Practice Deal')}</span>
        </div>
        
        <div class="board-layout">
            <div class="hands-area">
                <div class="north"><div class="hand-box"><strong>North</strong>{show(deal['north'])}</div></div>
                <div class="west"><div class="hand-box"><strong>West</strong>{show(deal['west'])}</div></div>
                <div class="center-img">N / All</div>
                <div class="east"><div class="hand-box"><strong>East</strong>{show(deal['east'])}</div></div>
                <div class="south"><div class="hand-box"><strong>South</strong>{show(deal['south'])}</div></div>
            </div>

            <div class="auction-area">
                <table class="auction">
                    <thead><tr><th>North</th><th>East</th><th>South</th><th>West</th></tr></thead>
                    <tbody>{auction_rows}</tbody>
                </table>
            </div>
            
            {logic_html}
        </div>
    </div>
    """

def main():
    print(f"Reading: {INPUT_FILE}")
    if not INPUT_FILE.exists():
        print("❌ Error: PBN file not found.")
        return

    deals = parse_pbn_file(INPUT_FILE)
    print(f"Found {len(deals)} deals.")

    html_content = HTML_HEADER
    for i, deal in enumerate(deals, 1):
        html_content += generate_hand_html(deal, i)
    html_content += HTML_FOOTER

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ Generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()