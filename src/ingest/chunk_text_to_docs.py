import re
from pathlib import Path
from typing import List, Dict, Optional

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


RE_RECORD_START = re.compile(r"^Record from:\s*(?P<file>[^,]+),\s*line:\s*(?P<line>\d+)\s*$")
RE_FIELD = re.compile(r"^(?P<key>term|definition|category|source):\s*(?P<value>.*)\s*$", re.IGNORECASE)


def parse_records(raw_text: str) -> List[str]:
    # Split on lines that start a new record, keeping boundaries clean
    parts = re.split(r"(?m)^(?=Record from:\s)", raw_text)
    return [p.strip() for p in parts if p.strip()]


def record_to_document(record_text: str) -> Optional[Document]:
    lines = [ln.rstrip("\n") for ln in record_text.splitlines() if ln.strip()]

    # First line should be the Record from line
    m = RE_RECORD_START.match(lines[0])
    if not m:
        return None

    meta: Dict[str, str] = {
        "source_file": m.group("file").strip(),
        "source_line": m.group("line").strip(),
    }

    fields: Dict[str, str] = {}
    for ln in lines[1:]:
        fm = RE_FIELD.match(ln)
        if fm:
            k = fm.group("key").lower()
            v = fm.group("value").strip()
            fields[k] = v

    term = fields.get("term", "").strip()
    definition = fields.get("definition", "").strip()
    category = fields.get("category", "").strip()
    src = fields.get("source", "").strip()

    if term:
        meta["term"] = term
    if category:
        meta["category"] = category
    if src:
        meta["glossary_source"] = src

    # Retrieval friendly content, keep term and definition together
    content_lines = []
    if term:
        content_lines.append(f"term: {term}")
    if definition:
        content_lines.append(f"definition: {definition}")
    if category:
        content_lines.append(f"category: {category}")
    if src:
        content_lines.append(f"source: {src}")

    page_content = "\n".join(content_lines).strip()
    if not page_content:
        return None

    return Document(page_content=page_content, metadata=meta)


def build_documents(
    txt_path: str,
    max_chars_per_chunk: int = 2000,
    overlap_chars: int = 150,
) -> List[Document]:
    raw = Path(txt_path).read_text(encoding="utf-8", errors="replace")
    records = parse_records(raw)

    base_docs: List[Document] = []
    for rec in records:
        doc = record_to_document(rec)
        if doc is not None:
            base_docs.append(doc)

    # Only sub split records that are too long, while preserving metadata
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_chars_per_chunk,
        chunk_overlap=overlap_chars,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    final_docs: List[Document] = []
    for doc in base_docs:
        if len(doc.page_content) <= max_chars_per_chunk:
            final_docs.append(doc)
        else:
            subs = splitter.split_text(doc.page_content)
            for i, sub in enumerate(subs):
                md = dict(doc.metadata)
                md["subchunk_index"] = i
                final_docs.append(Document(page_content=sub, metadata=md))

    return final_docs


if __name__ == "__main__":
    docs = build_documents("../../storage/corpus/cibc_finance_terms.txt")
    print(f"Built {len(docs)} Documents")
    print("\nFirst Document:\n")
    print(docs[0].page_content)
    print("\nMetadata:\n")
    print(docs[0].metadata)