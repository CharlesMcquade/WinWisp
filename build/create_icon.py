"""
Create a simple icon for WinWisp
This creates a basic microphone icon for the application
"""
from PIL import Image, ImageDraw

def create_app_icon():
    """Create application icon in multiple sizes for .ico file"""
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    images = []
    
    for size in sizes:
        # Create image
        img = Image.new('RGBA', size, color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Calculate proportions
        width, height = size
        center_x = width // 2
        
        # Colors
        mic_color = (66, 135, 245)  # Blue
        stand_color = (66, 135, 245)
        
        # Scale factors
        scale = width / 64.0
        
        # Draw microphone body (rounded rectangle)
        mic_width = int(24 * scale)
        mic_height = int(20 * scale)
        mic_top = int(15 * scale)
        
        # Microphone capsule (ellipse + rectangle)
        draw.ellipse(
            [center_x - mic_width//2, mic_top, 
             center_x + mic_width//2, mic_top + mic_height//2],
            fill=mic_color
        )
        draw.rectangle(
            [center_x - mic_width//2, mic_top + mic_height//4,
             center_x + mic_width//2, mic_top + mic_height],
            fill=mic_color
        )
        
        # Microphone stand
        stand_width = int(4 * scale)
        stand_height = int(10 * scale)
        stand_top = mic_top + mic_height
        
        draw.rectangle(
            [center_x - stand_width//2, stand_top,
             center_x + stand_width//2, stand_top + stand_height],
            fill=stand_color
        )
        
        # Base
        base_width = int(20 * scale)
        base_height = int(3 * scale)
        base_top = stand_top + stand_height
        
        draw.rectangle(
            [center_x - base_width//2, base_top,
             center_x + base_width//2, base_top + base_height],
            fill=stand_color
        )
        
        images.append(img)
    
    # Save as .ico file
    images[0].save(
        'build/app_icon.ico',
        format='ICO',
        sizes=[(img.width, img.height) for img in images],
        append_images=images[1:]
    )
    
    print("Icon created successfully: build/app_icon.ico")

if __name__ == '__main__':
    create_app_icon()
