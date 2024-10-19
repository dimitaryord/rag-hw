from langchain_text_splitters import RecursiveCharacterTextSplitter, TokenTextSplitter

MODEL_CHUNK_SIZE = 512
MODEL_CHUNK_OVERLAP = 200

pdf_separators = [
    "\n\n",
    "\n- ",
    "\n* ",
    "\n• ",
    "\n1. ",
    "\n",
    " ",
    ""
]
pdf_splitter = RecursiveCharacterTextSplitter(separators=pdf_separators, chunk_size=MODEL_CHUNK_SIZE, chunk_overlap=MODEL_CHUNK_OVERLAP)
txt_splitter = TokenTextSplitter(chunk_size=MODEL_CHUNK_SIZE, chunk_overlap=MODEL_CHUNK_OVERLAP)
