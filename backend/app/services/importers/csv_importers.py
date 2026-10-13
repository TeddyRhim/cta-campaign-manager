import codecs
import csv
import io

from fastapi import HTTPException, UploadFile

MAX_FILE_BYTES = 5 * 1024 * 1024

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


def read_csv(file: UploadFile) -> list[dict]:
    # Lecture bornée : un fichier trop gros est refusé sans être chargé en entier.
    content = file.file.read(MAX_FILE_BYTES + 1)
    if len(content) > MAX_FILE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"CSV file is larger than {MAX_FILE_BYTES // (1024 * 1024)} MB",
        )

    try:
        text = codecs.decode(content, "utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="CSV file must be UTF-8 encoded"
        ) from None

    reader = csv.DictReader(io.StringIO(text, newline=""))
    columns = set(reader.fieldnames or [])

    for mapping in COLUMN_MAPPINGS.values():
        if set(mapping.values()) == columns:
            return [
                {internal: row.get(csv_name) for internal, csv_name in mapping.items()}
                for row in reader
            ]

    raise HTTPException(
        status_code=400,
        detail="Invalid CSV columns"
    )
