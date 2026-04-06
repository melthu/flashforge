from pathlib import Path

MAX_CHARS = 80_000
MIN_CHARS = 200
SEPARATOR = "\n\n---\n\n"


def _read_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_pdf(path: Path) -> str:
    import pdfplumber
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    return "\n".join(pages)


def ingest_directory(dir_path: str) -> str:
    directory = Path(dir_path)
    if not directory.is_dir():
        raise NotADirectoryError(f"'{dir_path}' is not a valid directory")

    parts = []
    for path in directory.iterdir():
        if path.suffix in (".txt", ".md"):
            parts.append(_read_txt(path))
        elif path.suffix == ".pdf":
            parts.append(_read_pdf(path))
        else:
            print(f"Skipping {path.name} — unsupported format")

    combined = SEPARATOR.join(parts)

    if len(combined) < MIN_CHARS:
        raise ValueError(f"Not enough readable content found in {dir_path}")

    if len(combined) > MAX_CHARS:
        n_files = len(parts)
        print(f"Input truncated to 80k chars — {n_files} files may be partially used")
        combined = combined[:MAX_CHARS]

    return combined
