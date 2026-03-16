"""
File Upload Module for Modern Online Store
Handles profile pictures and other file uploads using local storage
"""

import os
import uuid
import io
from PIL import Image

# Allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
AVATAR_SIZE = (400, 400)  # Resize avatar to 400x400

# Local storage path for avatars
AVATAR_FOLDER = os.path.join('static', 'uploads', 'avatars')


def ensure_upload_folder():
    """Ensure the upload folder exists"""
    if not os.path.exists(AVATAR_FOLDER):
        os.makedirs(AVATAR_FOLDER)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_unique_filename(original_filename):
    """Generate a unique filename"""
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
    return f'{uuid.uuid4().hex}.{ext}'


def resize_image(image_data, size=AVATAR_SIZE):
    """Resize image to specified dimensions"""
    img = Image.open(io.BytesIO(image_data))

    # Convert to RGB if necessary (for PNG with transparency)
    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGB')

    # Resize maintaining aspect ratio
    img.thumbnail(size, Image.Resampling.LANCZOS)

    # Save to bytes
    output = io.BytesIO()
    img.save(output, format='JPEG', quality=85)
    return output.getvalue()


def save_avatar_locally(file_data, filename, user_id=None):
    """
    Save avatar to local storage

    Args:
        file_data: bytes of file content
        filename: original filename
        user_id: optional user ID for folder organization

    Returns:
        dict with 'success', 'url', 'path' keys
    """
    try:
        ensure_upload_folder()

        # Generate unique filename
        unique_filename = generate_unique_filename(filename)

        # Create user folder if needed
        if user_id:
            user_folder = os.path.join(AVATAR_FOLDER, f'user_{user_id}')
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)
            filepath = os.path.join(user_folder, unique_filename)
            rel_path = f'user_{user_id}/{unique_filename}'
        else:
            filepath = os.path.join(AVATAR_FOLDER, unique_filename)
            rel_path = unique_filename

        # Save file
        with open(filepath, 'wb') as f:
            f.write(file_data)

        # Generate URL
        url = f'/static/uploads/avatars/{rel_path}'

        return {
            'success': True,
            'url': url,
            'path': rel_path,
            'filename': unique_filename
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def delete_local_avatar(path):
    """
    Delete avatar from local storage

    Args:
        path: file path relative to avatar folder

    Returns:
        dict with 'success' key
    """
    try:
        filepath = os.path.join(AVATAR_FOLDER, path)
        if os.path.exists(filepath):
            os.remove(filepath)
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def process_avatar_upload(file_storage, user_id):
    """
    Process avatar upload from Flask file storage

    Args:
        file_storage: Flask FileStorage object
        user_id: user ID for folder organization

    Returns:
        dict with upload result
    """
    if not file_storage or file_storage.filename == '':
        return {'success': False, 'error': 'No file selected'}

    if not allowed_file(file_storage.filename):
        return {'success': False, 'error': 'File type not allowed. Use PNG, JPG, or GIF.'}

    # Check file size
    file_storage.seek(0, 2)  # Seek to end
    file_size = file_storage.tell()
    file_storage.seek(0)  # Reset to beginning

    if file_size > MAX_FILE_SIZE:
        return {'success': False, 'error': 'File too large. Maximum size is 5MB.'}

    # Read and resize image
    image_data = file_storage.read()
    resized_data = resize_image(image_data)

    # Save locally
    return save_avatar_locally(resized_data, file_storage.filename, user_id)


def upload_base64_image(base64_string, user_id):
    """
    Process avatar upload from base64 string (for canvas/image editor)

    Args:
        base64_string: base64 encoded image data
        user_id: user ID for folder organization

    Returns:
        dict with upload result
    """
    try:
        import base64

        # Remove data URL prefix if present
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]

        # Decode base64
        image_data = base64.b64decode(base64_string)

        # Resize image
        resized_data = resize_image(image_data)

        # Save locally
        return save_avatar_locally(resized_data, 'avatar.jpg', user_id)
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_default_avatar_url(name):
    """
    Generate default avatar URL using initials
    Uses UI Avatars API for consistent default avatars

    Args:
        name: user's full name

    Returns:
        URL to default avatar image
    """
    initials = ''.join([n[0].upper() for n in name.split()[:2]])
    return f'https://ui-avatars.com/api/?name={initials}&background=6366f1&color=fff&size=400&bold=true'


def get_avatar_url(user):
    """
    Get user's avatar URL

    Args:
        user: User object

    Returns:
        Avatar URL string
    """
    if user and user.avatar and user.avatar != 'default-avatar.png':
        # If it's a full URL, return as is
        if user.avatar.startswith('http'):
            return user.avatar
        # For local paths, return as-is (Flask will serve from static)
        return user.avatar

    # Return default avatar
    return get_default_avatar_url(user.get_full_name() if user else 'User')


def delete_from_supabase(path, bucket='avatars'):
    """
    Delete file from local storage (alias for compatibility)

    Args:
        path: file path in storage
        bucket: ignored (for compatibility)

    Returns:
        dict with 'success' key
    """
    return delete_local_avatar(path)
