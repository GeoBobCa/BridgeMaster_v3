import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, 
                               QTextEdit, QSplitter, QVBoxLayout, QWidget, QLabel, QMessageBox, QHeaderView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QBrush
from ruamel.yaml import YAML, YAMLError

SYSTEM_FILE = "systems/bidding_tree.yaml"

class BridgeTreeViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bridge System Viewer")
        self.resize(1200, 800)

        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Splitter (Tree on Left, Details on Right)
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        # 1. THE TREE WIDGET
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Bid", "Type", "Complexity"])
        self.tree.setColumnWidth(0, 200)
        self.tree.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tree.itemClicked.connect(self.on_item_clicked)
        splitter.addWidget(self.tree)

        # 2. THE DETAILS PANE
        self.details_display = QTextEdit()
        self.details_display.setReadOnly(True)
        self.details_display.setFont(QFont("Consolas", 11))
        splitter.addWidget(self.details_display)

        # Set initial sizes (40% Tree, 60% Details)
        splitter.setSizes([400, 800])

        # Load Data
        self.load_data()

    def load_data(self):
        yaml = YAML()
        if not os.path.exists(SYSTEM_FILE):
            QMessageBox.critical(self, "Error", f"File not found:\n{SYSTEM_FILE}")
            return

        try:
            with open(SYSTEM_FILE, 'r', encoding='utf-8') as f:
                data = yaml.load(f)
                
            self.populate_tree(data)
            
        except YAMLError as e:
            # THIS IS THE DEBUGGER PART
            error_msg = str(e)
            self.details_display.setText(f"❌ YAML SYNTAX ERROR\n\n{error_msg}")
            self.details_display.setStyleSheet("color: red; background-color: #ffeeee;")
            QMessageBox.critical(self, "YAML Syntax Error", f"Could not parse file.\nSee details pane.")

    def populate_tree(self, data):
        self.tree.clear()
        
        # Root Level (The Auction States: "Dealer", "1H", "1S", etc.)
        for auction_key, children in data.items():
            root_item = QTreeWidgetItem(self.tree)
            root_item.setText(0, f"Auction: {auction_key}")
            root_item.setForeground(0, QBrush(QColor("blue")))
            font = root_item.font(0)
            font.setBold(True)
            root_item.setFont(0, font)
            
            # Store the raw data for the root (optional)
            root_item.setData(0, Qt.UserRole, {"description": f"Responses to {auction_key}"})

            # Add Children (The Bids)
            if isinstance(children, list):
                for bid_rule in children:
                    self.add_bid_node(root_item, bid_rule)
            
        self.tree.expandAll()

    def add_bid_node(self, parent_item, rule):
        bid_str = rule.get('bid', '???')
        bid_type = rule.get('type', 'Unknown')
        complexity = rule.get('complexity', 'Basic')

        item = QTreeWidgetItem(parent_item)
        item.setText(0, bid_str)
        item.setText(1, bid_type)
        item.setText(2, complexity)

        # Color coding
        if complexity == "Advanced":
            item.setForeground(2, QBrush(QColor("darkred")))
        
        # Store the full rule dictionary in the item for display later
        item.setData(0, Qt.UserRole, rule)

    def on_item_clicked(self, item, column):
        rule = item.data(0, Qt.UserRole)
        if not rule:
            self.details_display.clear()
            return

        # Format the dictionary nicely for the Right Panel
        text = ""
        
        # Title
        bid = rule.get('bid', 'Unknown')
        convention = rule.get('convention', 'Natural')
        text += f"<h1>Bid: {bid} ({convention})</h1><hr>"

        # Explanation
        if 'explanation' in rule:
            text += f"<h3>Explanation</h3><p>{rule['explanation']}</p>"

        # Inference
        if 'inference' in rule:
            text += f"<h3>Inference</h3><p><i>{rule['inference']}</i></p>"

        # Constraints
        constraints = rule.get('constraints', {})
        if constraints:
            text += "<h3>Requirements</h3><ul>"
            for k, v in constraints.items():
                text += f"<li><b>{k}:</b> {v}</li>"
            text += "</ul>"
        
        # Raw Data (Debug view at bottom)
        text += "<br><hr><br><b>Raw YAML Data:</b><pre>"
        import json
        text += json.dumps(rule, indent=2)
        text += "</pre>"

        self.details_display.setHtml(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = BridgeTreeViewer()
    viewer.show()
    sys.exit(app.exec())