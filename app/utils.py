class FilesConfig:
    """Configuration for all the files used in the backend."""
    allowed_extensions = set(['png', 'jpg', 'jpeg', 'gif'])
    class_map = "app/static/assets/k49_classmap.csv"
    model_name = "app/models/hiragana_classifier_v1.h5"

def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.

    Args:
        filename (str): The name of the uploaded file.

    Returns:
        bool: True if the file has an allowed extension, False otherwise.
    """
    allowed_extensions = FilesConfig.allowed_extensions
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
