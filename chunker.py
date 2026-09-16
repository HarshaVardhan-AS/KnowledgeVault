from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=0,
    separators=[
        "\n\n",
        "\n• ",
        "\n◦ ",
        "\n",
        ". ",
        " ",
        ""
    ]
)
def chunk_text(raw_text: str) -> list[str]:
    clean_text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    chunks = text_splitter.split_text(clean_text)
    return chunks


