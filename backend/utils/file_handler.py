import os
import uuid
from werkzeug.utils import secure_filename
from PIL import Image
from config import Config

def allowed_file(filename):
    """
    Check if file extension is allowed
    
    Returns:
        Boolean
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def generate_unique_filename(original_filename):
    """
    Generate a unique filename while preserving extension
    
    Returns:
        Unique filename string
    """
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    return unique_name

def save_uploaded_file(file, subfolder='accidents'):
    """
    Save an uploaded file securely
    
    Args:
        file: FileStorage object from Flask request
        subfolder: Subfolder within uploads directory
        
    Returns:
        Tuple of (success, filepath or error_message)
    """
    try:
        # Check if file is allowed
        if not allowed_file(file.filename):
            return False, "File type not allowed"
        
        # Create subfolder if it doesn't exist
        upload_path = os.path.join(Config.UPLOAD_FOLDER, subfolder)
        os.makedirs(upload_path, exist_ok=True)
        
        # Generate unique filename
        filename = generate_unique_filename(file.filename)
        filepath = os.path.join(upload_path, filename)
        
        # Save file
        file.save(filepath)
        
        # Optimize image
        optimize_image(filepath)
        
        # Return relative path for database storage
        relative_path = os.path.join(subfolder, filename)
        return True, relative_path
        
    except Exception as e:
        return False, str(e)

def optimize_image(filepath, max_size=(1920, 1080), quality=85):
    """
    Optimize image file size while maintaining quality
    
    Args:
        filepath: Path to image file
        max_size: Maximum dimensions (width, height)
        quality: JPEG quality (1-100)
    """
    try:
        with Image.open(filepath) as img:
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Resize if larger than max_size
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save optimized image
            img.save(filepath, optimize=True, quality=quality)
            
    except Exception as e:
        # If optimization fails, keep original file
        pass

def delete_file(filepath):
    """
    Delete a file safely
    
    Args:
        filepath: Relative path to file
        
    Returns:
        Boolean indicating success
    """
    try:
        full_path = os.path.join(Config.UPLOAD_FOLDER, filepath)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False
    except Exception:
        return False

def get_file_url(filepath):
    """
    Get URL for accessing uploaded file
    
    Args:
        filepath: Relative path to file
        
    Returns:
        URL string
    """
    if not filepath:
        return None
    return f"/uploads/{filepath}"
