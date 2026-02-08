from fpdf import FPDF
from datetime import datetime
import os
import re

# --- COLORS ---
# Navy Blue: #2C3E50 -> (44, 62, 80)
# Emerald Green: #27AE60 -> (39, 174, 96)
# Gray Text: #7F8C8D -> (127, 140, 141)
# Black Text: #2C3E50 (Dark Blue-Black)

class PDF(FPDF):
    def header(self):
        # Top Bar
        self.set_fill_color(44, 62, 80) # Navy
        self.rect(0, 0, 210, 20, 'F')
        
        # Title
        self.set_y(5)
        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, 'Morning Edition', 0, 1, 'C')
        
        # Subtitle / Date
        self.set_font('Helvetica', 'I', 10)
        self.set_text_color(200, 200, 200) # Light Gray
        date_str = datetime.now().strftime("%A, %B %d, %Y")
        self.cell(0, 5, f'Daily Knowledge Digest | {date_str}', 0, 1, 'C')
        
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(127, 140, 141)
        self.cell(0, 10, f'Curated by Antigravity Bot | Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, label):
        # Section Header with colored background strip
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(44, 62, 80) # Navy
        self.cell(0, 8, label, 0, 1, 'L')
        
        # Underline
        self.set_draw_color(39, 174, 96) # Green Accent
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.set_text_color(50, 50, 50)
        
        # Parse Slack-style links <url|text> and render
        # We split by the regex pattern to get chunks of (text, url)
        # Pattern: <(http[^|]+)\|([^>]+)>
        parts = re.split(r'<([^|]+)\|([^>]+)>', body)
        
        # Starting content
        for i, part in enumerate(parts):
            if i == 0:
                # Normal text
                self.write(6, clean_text_for_pdf(part))
            elif i % 3 == 0:
                # This is normal text after a link
                self.write(6, clean_text_for_pdf(part))
            elif i % 3 == 2:
                # This is the LINK TEXT (captured in group 2)
                # The previous part (i-1) was the URL (group 1)
                url = parts[i-1]
                link_text = part
                
                # Render Link
                self.set_text_color(39, 174, 96) # Green Link
                self.set_font('', 'U')
                self.write(6, clean_text_for_pdf(link_text), link=url)
                
                # Reset
                self.set_text_color(50, 50, 50)
                self.set_font('', '')
        
        self.ln(8)

def clean_text_for_pdf(text):
    if not text: return ""
    # Replace common markdown bold ** with nothing or handle formatted logic later
    text = text.replace('**', '').replace('*', '') 
    return text.encode('latin-1', 'ignore').decode('latin-1')

def generate_daily_pdf(ai_report, learning_item=None):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # 1. Main News Content
    for category, content in ai_report.items():
        pdf.chapter_title(clean_text_for_pdf(category.upper()))
        pdf.chapter_body(content)

    # 2. Learning Content (Styled Box)
    if learning_item:
        pdf.ln(5)
        pdf.set_fill_color(235, 245, 238) # Very Light Green
        pdf.rect(10, pdf.get_y(), 190, 40, 'F')
        
        pdf.set_xy(15, pdf.get_y() + 5)
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(39, 174, 96)
        pdf.cell(0, 6, "LEARNING CORNER: " + clean_text_for_pdf(learning_item.get('title', '')), 0, 1)
        
        pdf.set_x(15)
        pdf.set_font('Arial', 'I', 11)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(180, 6, clean_text_for_pdf(learning_item.get('content', '')))

    # Save
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_path, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    filename = f"Morning_Edition_{datetime.now().strftime('%Y-%m-%d')}_Premium.pdf"
    filepath = os.path.join(data_dir, filename)
    
    try:
        pdf.output(filepath)
        print(f"  > Premium PDF Generated: {filepath}")
        return filepath
    except Exception as e:
        print(f"  > Error generating PDF: {e}")
        return None
