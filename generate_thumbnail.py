"""
LinkedIn Thumbnail Generator for Crypto AI Dashboard
Generates a professional thumbnail image using Python Pillow library
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_thumbnail():
    """Create LinkedIn thumbnail for Crypto AI Dashboard"""
    
    # Image dimensions (LinkedIn recommended: 1200x627)
    width, height = 1200, 627
    
    # Create image with gradient background
    img = Image.new('RGB', (width, height), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    # Add gradient effect (simple version)
    for y in range(height):
        # Create gradient from dark blue to slightly lighter blue
        r = int(26 + (y / height) * 30)
        g = int(26 + (y / height) * 40)
        b = int(46 + (y / height) * 60)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Try to load fonts, fallback to default if not available
    try:
        title_font = ImageFont.truetype("arial.ttf", 60)
        subtitle_font = ImageFont.truetype("arial.ttf", 40)
        tech_font = ImageFont.truetype("arial.ttf", 30)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        tech_font = ImageFont.load_default()
    
    # Draw title
    title = "Crypto AI Dashboard"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 150), title, font=title_font, fill='#ffffff')
    
    # Draw subtitle
    subtitle = "Multi-Agent Intelligence Platform"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    draw.text((subtitle_x, 230), subtitle, font=subtitle_font, fill='#00d4ff')
    
    # Draw tech stack
    tech_stack = "Python • TensorFlow • Hugging Face"
    tech_bbox = draw.textbbox((0, 0), tech_stack, font=tech_font)
    tech_width = tech_bbox[2] - tech_bbox[0]
    tech_x = (width - tech_width) // 2
    draw.text((tech_x, 320), tech_stack, font=tech_font, fill='#a0a0a0')
    
    # Draw decorative elements (squares)
    draw.rectangle((50, 50, 100, 100), fill='#00d4ff', outline=None)
    draw.rectangle((width-100, height-100, width-50, height-50), fill='#00ff88', outline=None)
    draw.rectangle((50, height-100, 100, height-50), fill='#ff6b6b', outline=None)
    draw.rectangle((width-100, 50, width-50, 100), fill='#ffd93d', outline=None)
    
    # Save the image
    output_file = 'linkedin_thumbnail.png'
    img.save(output_file)
    print(f"✅ Thumbnail created: {output_file}")
    return output_file

if __name__ == "__main__":
    # Check if Pillow is installed
    try:
        from PIL import Image, ImageDraw, ImageFont
        create_thumbnail()
    except ImportError:
        print("❌ Error: Pillow library not installed")
        print("Install with: pip install pillow")
