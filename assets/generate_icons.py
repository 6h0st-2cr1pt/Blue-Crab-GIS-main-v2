from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(name, size=(24, 24), bg_color=(41, 128, 185), fg_color=(255, 255, 255)):
    """Create a simple icon with the first letter of the name"""
    # Create a new image with a blue background
    img = Image.new('RGBA', size, color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a circle background
    circle_x, circle_y = size[0] // 2, size[1] // 2
    circle_radius = min(size) // 2
    draw.ellipse(
        (circle_x - circle_radius, circle_y - circle_radius, 
         circle_x + circle_radius, circle_y + circle_radius), 
        fill=bg_color
    )
    
    # Try to load a font, use default if not available
    try:
        font = ImageFont.truetype("arial.ttf", size=size[0] // 2)
    except IOError:
        font = ImageFont.load_default()
    
    # Get the first letter of the name
    letter = name[0].upper() if name else "?"
    
    # Calculate text position to center it
    text_width, text_height = draw.textsize(letter, font=font)
    text_x = (size[0] - text_width) // 2
    text_y = (size[1] - text_height) // 2
    
    # Draw the letter
    draw.text((text_x, text_y), letter, font=font, fill=fg_color)
    
    # Save the image
    os.makedirs("assets/icons", exist_ok=True)
    img.save(f"assets/icons/{name}.png")
    print(f"Created icon: assets/icons/{name}.png")

def generate_sidebar_icons():
    """Generate icons for the sidebar"""
    icons = [
        "dashboard", "map", "analytics", "database", "upload", "info",
        "blue_crab_logo"
    ]
    
    for icon in icons:
        create_icon(icon, size=(48, 48) if icon == "blue_crab_logo" else (24, 24))

def generate_map_control_icons():
    """Generate icons for the map controls"""
    icons = [
        "zoom_in", "zoom_out", "home", "layers", "ruler", "fullscreen",
        "search", "dropdown", "upload_file", "location", "population",
        "average", "maximum", "refresh"
    ]
    
    for icon in icons:
        create_icon(icon)

if __name__ == "__main__":
    generate_sidebar_icons()
    generate_map_control_icons()
    print("All icons generated successfully!")
