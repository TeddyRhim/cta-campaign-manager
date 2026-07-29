import csv
import io

from fastapi import (UploadFile, HTTPException)


def read_csv(file: UploadFile):

    COLUMN_MAPPINGS = {
        "format_a": {
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "email",
            "phone": "phone",
            "organization": "organization",
        },
        "format_b": {
            "first_name": "Prénom",
            "last_name": "Nom",
            "email": "Mail",
            "phone": "Téléphone",
            "organization": "Société",
        },
    }
    
    content = file.file.read()
    text = content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))

    def detect_format(fieldnames: list[str]) -> dict[str, str]:
        columns = set(reader.fieldnames or [])

        for mapping in COLUMN_MAPPINGS.values():
            if set(mapping.values()) == columns:
                return mapping

        raise HTTPException(
            status_code=404,
            detail="Invalid CSV columns"
        )

    def normalize_row(row: dict, mapping: dict[str, str]) -> dict:
        return {
            internal_name: row[csv_name]
            for internal_name, csv_name in mapping.items()
        }

    mapping = detect_format(reader.fieldnames)

    return [
        normalize_row(row, mapping)
        for row in reader
    ]