from fpdf import FPDF
from datetime import datetime
import os
import re

# --- COLORS (From Stitch Design) ---
COLOR_PRIMARY = (26, 54, 93)      # Deep Navy Blue
COLOR_ACCENT = (185, 28, 28)      # Deep Crimson
COLOR_TEXT_DARK = (15, 23, 42)    # Slate 900
COLOR_TEXT_GRAY = (100, 116, 139) # Slate 500
COLOR_BG_LIGHT = (255, 255, 255)

class NewspaperPDF(FPDF):
    def header(self):
        # 1. Top Metadata Bar (Vol | Date | Edition)
        self.set_y(10)
        self.set_font('Helvetica', 'I', 12)
        self.set_text_color(*COLOR_TEXT_GRAY)
        
        # Calculate width for 3 distinct parts
        page_width = self.w - 20
        col_width = page_width / 3
        
        # Vol No (Left)
        self.cell(col_width, 5, 'VOL. CXXIV ... No. 58,402', 0, 0, 'L')
        # Date (Center)
        date_str = datetime.now().strftime("%A, %B %d, %Y").upper()
        self.cell(col_width, 5, date_str, 0, 0, 'C')
        # Edition (Right)
        self.cell(col_width, 5, 'LONDON & NEW YORK EDITION', 0, 1, 'R')
        
        # 2. Main Title
        self.ln(2)
        self.set_font('Times', 'B', 36)
        self.set_text_color(*COLOR_PRIMARY)
        self.cell(0, 15, 'Daily Law, Politics & Tech Journal', 0, 1, 'C')
        
        # 3. Horizontal Separator (Double Line style)
        self.ln(2)
        self.set_draw_color(*COLOR_TEXT_DARK)
        self.set_line_width(0.6)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(1)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        # No footer as requested
        pass

    def chapter_title(self, label):
        # Section Header
        self.set_font('Times', 'B', 16)
        self.set_text_color(*COLOR_ACCENT)
        self.cell(0, 8, label.upper(), 0, 1, 'L')
        
        # Decorative underscore
        self.set_draw_color(*COLOR_ACCENT)
        self.set_line_width(1)
        self.line(10, self.get_y(), 60, self.get_y()) # Short line
        self.ln(5)

    def write_styled_text(self, text):
        """
        Parses text for *bold* markers and writes it accordingly.
        Respects the CURRENT font family/size/style but toggles Bold.
        """
        # Save current font state
        current_font = self.font_family
        current_style = self.font_style
        current_size = self.font_size_pt
        
        # Split by *bold* markers: "Normal *Bold* Normal" -> ['Normal ', 'Bold', ' Normal']
        parts = re.split(r'\*([^*]+)\*', text)
        
        for i, part in enumerate(parts):
            if not part: continue
            
            if i % 2 == 1:
                # Odd indices are the captured bold text.
                # Logic: Toggle BOLD. 
                # If current style has 'B', remove it (Regular).
                # If current style lacks 'B', add it (Bold).
                
                new_style = current_style
                if 'B' in current_style:
                    new_style = new_style.replace('B', '')
                else:
                    new_style += 'B'
                
                self.set_font(current_font, new_style, current_size)
                self.write(5, part)
                # Revert
                self.set_font(current_font, current_style, current_size)
            else:
                # Even indices are normal text (keep current style)
                self.set_font(current_font, current_style, current_size)
                self.write(5, part)

    def article_content(self, title, body):
        # Headline
        self.set_font('Times', 'B', 14)
        self.set_text_color(*COLOR_TEXT_DARK)
        self.multi_cell(0, 6, clean_text_for_pdf(title))
        self.ln(2)

        # Body Text
        self.set_font('Times', '', 11)
        self.set_text_color(30, 30, 30)
        
        # 1. Parse content into lines first
        lines = body.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line behaves like a title
            is_headline = False
            if re.match(r'^\d+\.', line) or line.startswith('*') or line.startswith('#'):
                is_headline = True
                
            if is_headline:
                self.ln(4) # Extra space before new item
                self.set_font('Times', 'B', 12)
                self.set_text_color(*COLOR_PRIMARY)
            else:
                self.set_font('Times', '', 11)
                self.set_text_color(30, 30, 30)

            # 2. Process Links within the line
            parts = re.split(r'<([^|]+)\|([^>]+)>', line)
            
            for i, part in enumerate(parts):
                text_part = clean_text_for_pdf(part)
                if not text_part: continue

                if i % 3 == 0:
                    # Normal text (or the text before a link) which might contain *bold*
                    self.write_styled_text(text_part)
                elif i % 3 == 2:
                    # Link Text
                    url = parts[i-1] 
                    
                    # Style Link
                    current_font = self.font_family
                    current_style = self.font_style
                    current_size = self.font_size_pt
                    current_color = self.text_color
                    
                    self.set_text_color(*COLOR_ACCENT)
                    self.set_font('', 'U')
                    
                    # Links shouldn't have bold markers usually.
                    self.write(5, text_part, link=url)
                    
                    # Reset style
                    self.set_text_color(current_color.r, current_color.g, current_color.b)
                    self.set_font(current_font, current_style, current_size)
            
            self.ln(6) # New line after each paragraph/item
            
            # If it was a summary paragraph (not a headline), add extra blank line
            if not is_headline:
                self.ln(2)

def clean_text_for_pdf(text):
    if not text: return ""
    # Standardize quotes and dashes for Latin-1
    replacements = {
        '‘': "'", '’': "'", '“': '"', '”': '"', '–': '-', '—': '-',
        '…': '...', '\u2022': '*', '**': ''
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    
    return text.encode('latin-1', 'replace').decode('latin-1')

def generate_daily_pdf(ai_report, learning_item=None):
    pdf = NewspaperPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(10, 10, 10)
    pdf.add_page()
    
    # Mapping Config Keys (with emojis) to Clean PDF Titles
    # Usage: { ConfigKeySubstring: DisplayTitle }
    SECTION_MAPPING = {
        "International Law": "International News",
        "International Relations": "International Relations", 
        "National": "National & Political (Pakistan)",
        "Tech": "Tech & Innovation"
    }

    # Normalize input keys for flexible matching
    # Create a lookup: { CleanedKeySubstring: Content }
    content_map = {}
    for k, v in ai_report.items():
        # Remove emojis and whitespace for safer matching
        clean_key = re.sub(r'[^\w\s&]', '', k).strip() 
        content_map[clean_key] = v
        # Also map the raw key just in case
        content_map[k] = v

    # Iterate through our desired order
    for match_string, display_title in SECTION_MAPPING.items():
        # Find content that contains the match_string
        found_content = None
        
        # 1. Try exact match in normalized map key
        for actual_key, content in ai_report.items():
            if match_string in actual_key:
                found_content = content
                break
        
        if found_content:
            pdf.chapter_title(clean_text_for_pdf(display_title))
            pdf.article_content(f"Latest Developments in {display_title}", found_content)

    # Save logic remains same...
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_path, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    filename = f"Morning_Edition_{datetime.now().strftime('%Y-%m-%d')}_Premium.pdf"
    filepath = os.path.join(data_dir, filename)
    
    try:
        pdf.output(filepath)
        print(f"  > Newspaper PDF Generated: {filepath}")
        return filepath
    except Exception as e:
        print(f"  > Error generating PDF: {e}")
        return None
