"""
File I/O Module
Handles file operations including text and JSON import/export
"""
import json
import datetime
import os


class FileManager:
    """Manages file loading and saving for macros"""

    @staticmethod
    def load_text(filepath):
        """
        Load a plain text script file

        Args:
            filepath: Path to the file

        Returns:
            File content as string
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def save_text(filepath, content):
        """
        Save content as plain text file

        Args:
            filepath: Path to save to
            content: Text content to save
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def load_json(filepath):
        """
        Load a JSON macro file (V4 format)

        Args:
            filepath: Path to JSON file

        Returns:
            Dictionary with keys: version, speed, script, metadata
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Validate V4 format
        required_keys = ['version', 'speed', 'script']
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Invalid V4 JSON format: missing '{key}' field")

        return data

    @staticmethod
    def save_json(filepath, script, speed=1.0, iterations=1, metadata=None):
        """
        Save macro as JSON file with V4 format

        Args:
            filepath: Path to save to
            script: Script content
            speed: Speed multiplier
            iterations: Iteration count
            metadata: Optional additional metadata dict
        """
        # Build metadata
        base_metadata = {
            "created_at": datetime.datetime.now().isoformat(),
            "created_by": "Macro Builder v4.0",
            "iterations": iterations
        }

        # Merge with provided metadata
        if metadata:
            base_metadata.update(metadata)

        # Create V4 JSON structure
        data = {
            "version": "4.0",
            "speed": speed,
            "script": script,
            "metadata": base_metadata
        }

        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def detect_format(filepath):
        """
        Detect file format based on extension and content

        Args:
            filepath: Path to file

        Returns:
            'json' or 'text'
        """
        # Check extension
        _, ext = os.path.splitext(filepath)
        if ext.lower() == '.json':
            return 'json'

        # Try to detect by parsing
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'version' in data:
                    return 'json'
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

        return 'text'

    @staticmethod
    def load_file(filepath):
        """
        Auto-detect format and load file

        Args:
            filepath: Path to file

        Returns:
            Tuple of (script_content, speed, iterations, metadata)
        """
        file_format = FileManager.detect_format(filepath)

        if file_format == 'json':
            data = FileManager.load_json(filepath)
            return (
                data['script'],
                data.get('speed', 1.0),
                data.get('metadata', {}).get('iterations', 1),
                data.get('metadata', {})
            )
        else:
            content = FileManager.load_text(filepath)
            return (content, 1.0, 1, {})
