# AI Exam Eval

A pipeline for evaluating handwritten student answer sheets. It extracts text from scanned copies with OCR, breaks the marking rubric into checkable parts, and compares each student's answers against them. The design goal is to rely on LLMs as little as possible and to run everything locally with small models.

## Status

| Stage | Status |
|-------|--------|
| 1. PDF to page images | Done |
| 2. Handwriting extraction (OCR) | Not started |
| 3. Rubric decomposition | Not started |
| 4. Comparison and scoring | Not started |

## Pipeline

### 1. PDF to images (`ocr.py`)

Each student answer sheet PDF is rendered page by page into PNG images using PyMuPDF.

- Input: `data/stu_ans_pdf/<student_copy>`
- Output: `data/stu_ans_img/<student_copy>/page-00.png`, `page-01.png`, ...

### 2. Handwriting extraction (planned)

- Primary engine: `pytesseract`
- Fallback engine: LLaVA (via Ollama) when the Tesseract output is judged unusable
- The engine used for each page should be recorded alongside its extracted text

### 3. Rubric decomposition (planned)

Break each question's rubric into smaller, individually checkable criteria. Local small model (for example Phi-3 via Ollama) where an LLM is needed.

### 4. Comparison and scoring (planned)

Compare the extracted student answers against the decomposed rubric criteria and produce a score per question. Local small model (for example Phi-3 via Ollama) where an LLM is needed.

## Project structure

```
.
├── data
│   ├── questions
│   │   └── AL_402
│   ├── stu_ans_img        # generated page images
│   │   ├── AL_402_1
│   │   └── AL_402_2
│   └── stu_ans_pdf        # input student answer sheets
│       ├── AL_402_1
│       └── AL_402_2
├── docs
├── ocr.py
├── README.md
└── requirements.txt
```

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. For the planned OCR and evaluation stages, install:
   - [Tesseract](https://github.com/tesseract-ocr/tesseract) (system package, required by `pytesseract`)
   - [Ollama](https://ollama.com), then pull the models:

     ```bash
     ollama pull llava
     ollama pull phi3
     ```

## Usage

Place student answer sheet PDFs in `data/stu_ans_pdf/`, then run:

```bash
python ocr.py
```

Page images are written to `data/stu_ans_img/<student_copy>/`.

## Known considerations

- Handwriting OCR quality limits everything downstream. A misread word can make a correct answer score as wrong.
- Tesseract tends to return garbled text on handwriting rather than raising an error, so a fallback needs an explicit quality check.
- Small local models can be inconsistent on judgment tasks and have limited context windows.
- Keep each stage's intermediate output on disk so a wrong score can be traced to the stage that caused it.
