from __future__ import annotations

import argparse
import pathlib
import re
import zlib


_STREAM_RE = re.compile(
    rb"<<(?P<dictionary>.*?)>>\s*stream\r?\n(?P<data>.*?)\r?\nendstream",
    re.DOTALL,
)
_TEXT_OPERATOR_RE = re.compile(r"""(?<!\S)(?:BT|ET|Tj|TJ|'|")(?!\S)""")
_TEXT_BLOCK_RE = re.compile(r"BT(.*?)ET", re.DOTALL)
_WHITESPACE_RE = re.compile(r"\s+")


def _decode_stream(stream_dictionary: bytes, stream_data: bytes) -> bytes | None:
    if b"/Filter" not in stream_dictionary:
        return stream_data
    if b"/FlateDecode" in stream_dictionary:
        try:
            return zlib.decompress(stream_data)
        except zlib.error:
            return None
    return None


def _decode_pdf_literal(stream_text: str, start_index: int) -> tuple[str, int]:
    result: list[str] = []
    nesting = 1
    index = start_index + 1

    while index < len(stream_text):
        char = stream_text[index]
        if char == "\\":
            index += 1
            if index >= len(stream_text):
                break
            escape = stream_text[index]
            escape_map = {
                "n": "\n",
                "r": "\r",
                "t": "\t",
                "b": "\b",
                "f": "\f",
                "(": "(",
                ")": ")",
                "\\": "\\",
            }
            if escape in escape_map:
                result.append(escape_map[escape])
            elif escape in "01234567":
                octal_digits = [escape]
                for _ in range(2):
                    next_index = index + 1
                    if next_index >= len(stream_text) or stream_text[next_index] not in "01234567":
                        break
                    index = next_index
                    octal_digits.append(stream_text[index])
                result.append(chr(int("".join(octal_digits), 8)))
            else:
                result.append(escape)
        elif char == "(":
            nesting += 1
            result.append(char)
        elif char == ")":
            nesting -= 1
            if nesting == 0:
                return "".join(result), index + 1
            result.append(char)
        else:
            result.append(char)
        index += 1

    return "".join(result), index


def _decode_pdf_hex(stream_text: str, start_index: int) -> tuple[str, int]:
    end_index = stream_text.find(">", start_index + 1)
    if end_index == -1:
        return "", len(stream_text)

    hex_text = re.sub(r"\s+", "", stream_text[start_index + 1 : end_index])
    if len(hex_text) % 2 == 1:
        hex_text += "0"
    try:
        decoded = bytes.fromhex(hex_text).decode("latin-1")
    except ValueError:
        decoded = ""
    return decoded, end_index + 1


def _extract_text_fragments(stream_bytes: bytes) -> list[str]:
    stream_text = stream_bytes.decode("latin-1", errors="ignore")
    if _TEXT_OPERATOR_RE.search(stream_text) is None:
        return []

    fragments: list[str] = []
    for block in _TEXT_BLOCK_RE.findall(stream_text):
        index = 0
        while index < len(block):
            char = block[index]
            if char == "(":
                fragment, index = _decode_pdf_literal(block, index)
                if fragment:
                    fragments.append(fragment)
                continue
            if char == "<" and index + 1 < len(block) and block[index + 1] != "<":
                fragment, index = _decode_pdf_hex(block, index)
                if fragment:
                    fragments.append(fragment)
                continue
            index += 1
    return fragments


def extract_pdf_text(pdf_path: str | pathlib.Path) -> str:
    """Best-effort stdlib-only extraction for text-based PDFs."""
    path = pathlib.Path(pdf_path)
    pdf_bytes = path.read_bytes()

    fragments: list[str] = []
    for match in _STREAM_RE.finditer(pdf_bytes):
        decoded_stream = _decode_stream(match.group("dictionary"), match.group("data"))
        if decoded_stream is None:
            continue
        fragments.extend(_extract_text_fragments(decoded_stream))

    normalized = [_WHITESPACE_RE.sub(" ", fragment).strip() for fragment in fragments]
    text = "\n".join(fragment for fragment in normalized if fragment)
    if not text:
        raise ValueError(f"No extractable text found in PDF: {path}")
    return text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract text from a text-based PDF.")
    parser.add_argument("pdf_path")
    args = parser.parse_args(argv)
    print(extract_pdf_text(args.pdf_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
