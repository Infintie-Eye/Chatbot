"""
File processing utilities for various document formats.
"""
import logging
import io
import json
from typing import Dict, Optional, Tuple
from pathlib import Path
import pandas as pd
from PIL import Image
import PyPDF2
from docx import Document
from config.settings import settings

# Configure logging
logger = logging.getLogger(__name__)


class FileProcessor:
    """Handles processing of various file types."""

    def __init__(self):
        """Initialize the file processor."""
        self.max_file_size = settings.max_file_size_mb * 1024 * 1024  # Convert to bytes
        self.supported_text_formats = settings.supported_text_formats
        self.supported_image_formats = settings.supported_image_formats

    def validate_file(self, uploaded_file) -> Tuple[bool, str]:
        """
        Validate uploaded file.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Check file size
            if uploaded_file.size > self.max_file_size:
                return False, f"File size exceeds {settings.max_file_size_mb}MB limit"

            # Check file extension
            file_extension = Path(uploaded_file.name).suffix.lower().lstrip('.')

            all_supported = self.supported_text_formats + self.supported_image_formats
            if file_extension not in all_supported:
                return False, f"Unsupported file format: {file_extension}"

            return True, ""

        except Exception as e:
            logger.error(f"File validation error: {str(e)}")
            return False, f"File validation failed: {str(e)}"

    def process_text_file(self, uploaded_file) -> Tuple[bool, str, str]:
        """
        Process text-based files.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Tuple of (success, content, error_message)
        """
        try:
            file_extension = Path(uploaded_file.name).suffix.lower().lstrip('.')
            content = ""

            if file_extension == 'txt':
                content = uploaded_file.read().decode('utf-8')

            elif file_extension == 'csv':
                df = pd.read_csv(uploaded_file)
                content = f"CSV File Analysis:\n"
                content += f"Shape: {df.shape[0]} rows, {df.shape[1]} columns\n"
                content += f"Columns: {', '.join(df.columns.tolist())}\n\n"
                content += "First 10 rows:\n"
                content += df.head(10).to_string()
                if df.shape[0] > 10:
                    content += f"\n\n... and {df.shape[0] - 10} more rows"

            elif file_extension == 'json':
                json_data = json.load(uploaded_file)
                content = json.dumps(json_data, indent=2, ensure_ascii=False)

            elif file_extension == 'pdf':
                reader = PyPDF2.PdfReader(uploaded_file)
                content = ""
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    content += f"--- Page {page_num + 1} ---\n{page_text}\n\n"

            elif file_extension == 'docx':
                doc = Document(uploaded_file)
                content = ""
                for paragraph in doc.paragraphs:
                    content += paragraph.text + "\n"

            elif file_extension == 'xlsx':
                # Read all sheets
                excel_file = pd.ExcelFile(uploaded_file)
                content = f"Excel File Analysis:\n"
                content += f"Number of sheets: {len(excel_file.sheet_names)}\n"
                content += f"Sheet names: {', '.join(excel_file.sheet_names)}\n\n"

                for sheet_name in excel_file.sheet_names:
                    df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                    content += f"--- Sheet: {sheet_name} ---\n"
                    content += f"Shape: {df.shape[0]} rows, {df.shape[1]} columns\n"
                    content += f"Columns: {', '.join(df.columns.tolist())}\n"
                    content += "First 5 rows:\n"
                    content += df.head(5).to_string()
                    content += "\n\n"

            return True, content, ""

        except Exception as e:
            logger.error(f"Text file processing error: {str(e)}")
            return False, "", f"Failed to process file: {str(e)}"

    def process_image_file(self, uploaded_file) -> Tuple[bool, Image.Image, str]:
        """
        Process image files.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Tuple of (success, image, error_message)
        """
        try:
            image = Image.open(uploaded_file)

            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')

            return True, image, ""

        except Exception as e:
            logger.error(f"Image processing error: {str(e)}")
            return False, None, f"Failed to process image: {str(e)}"

    def get_file_info(self, uploaded_file) -> Dict[str, any]:
        """
        Get information about the uploaded file.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Dictionary with file information
        """
        try:
            file_path = Path(uploaded_file.name)
            return {
                'name': uploaded_file.name,
                'size': uploaded_file.size,
                'size_mb': round(uploaded_file.size / (1024 * 1024), 2),
                'extension': file_path.suffix.lower().lstrip('.'),
                'stem': file_path.stem,
                'type': uploaded_file.type if hasattr(uploaded_file, 'type') else 'unknown'
            }
        except Exception as e:
            logger.error(f"Error getting file info: {str(e)}")
            return {'error': str(e)}

    def is_text_file(self, file_extension: str) -> bool:
        """Check if file extension is a text file."""
        return file_extension.lower() in self.supported_text_formats

    def is_image_file(self, file_extension: str) -> bool:
        """Check if file extension is an image file."""
        return file_extension.lower() in self.supported_image_formats


# Global file processor instance
file_processor = FileProcessor()
