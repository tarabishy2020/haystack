---
title: File Converters API
excerpt: Extracts text from files in different formats and cast it into the unified Document format.
category: 62e8ef01d9f80405c9a0febb
slug: file_converters_api
hidden: false
---

<a id="base"></a>

# Module base

<a id="base.BaseConverter"></a>

## BaseConverter

```python
class BaseConverter(BaseComponent)
```

Base class for implementing file converts to transform input documents to text format for ingestion in DocumentStore.

<a id="base.BaseConverter.__init__"></a>

#### BaseConverter.\_\_init\_\_

```python
def __init__(remove_numeric_tables: bool = False, valid_languages: Optional[List[str]] = None, id_hash_keys: Optional[List[str]] = None)
```

**Arguments**:

- `remove_numeric_tables`: This option uses heuristics to remove numeric rows from the tables.
The tabular structures in documents might be noise for the reader model if it
does not have table parsing capability for finding answers. However, tables
may also have long strings that could possible candidate for searching answers.
The rows containing strings are thus retained in this option.
- `valid_languages`: validate languages from a list of languages specified in the ISO 639-1
(https://en.wikipedia.org/wiki/ISO_639-1) format.
This option can be used to add test for encoding errors. If the extracted text is
not one of the valid languages, then it might likely be encoding error resulting
in garbled text.
- `id_hash_keys`: Generate the document id from a custom list of strings that refer to the document's
attributes. If you want to ensure you don't have duplicate documents in your DocumentStore but texts are
not unique, you can modify the metadata and pass e.g. `"meta"` to this field (e.g. [`"content"`, `"meta"`]).
In this case the id will be generated by using the content and the defined metadata.

<a id="base.BaseConverter.convert"></a>

#### BaseConverter.convert

```python
@abstractmethod
def convert(file_path: Path, meta: Optional[Dict[str, str]], remove_numeric_tables: Optional[bool] = None, valid_languages: Optional[List[str]] = None, encoding: Optional[str] = "UTF-8", id_hash_keys: Optional[List[str]] = None) -> List[Document]
```

Convert a file to a dictionary containing the text and any associated meta data.

File converters may extract file meta like name or size. In addition to it, user
supplied meta data like author, url, external IDs can be supplied as a dictionary.

**Arguments**:

- `file_path`: path of the file to convert
- `meta`: dictionary of meta data key-value pairs to append in the returned document.
- `remove_numeric_tables`: This option uses heuristics to remove numeric rows from the tables.
The tabular structures in documents might be noise for the reader model if it
does not have table parsing capability for finding answers. However, tables
may also have long strings that could possible candidate for searching answers.
The rows containing strings are thus retained in this option.
- `valid_languages`: validate languages from a list of languages specified in the ISO 639-1
(https://en.wikipedia.org/wiki/ISO_639-1) format.
This option can be used to add test for encoding errors. If the extracted text is
not one of the valid languages, then it might likely be encoding error resulting
in garbled text.
- `encoding`: Select the file encoding (default is `UTF-8`)
- `id_hash_keys`: Generate the document id from a custom list of strings that refer to the document's
attributes. If you want to ensure you don't have duplicate documents in your DocumentStore but texts are
not unique, you can modify the metadata and pass e.g. `"meta"` to this field (e.g. [`"content"`, `"meta"`]).
In this case the id will be generated by using the content and the defined metadata.

<a id="base.BaseConverter.validate_language"></a>

#### BaseConverter.validate\_language

```python
def validate_language(text: str, valid_languages: Optional[List[str]] = None) -> bool
```

Validate if the language of the text is one of valid languages.

<a id="base.BaseConverter.run"></a>

#### BaseConverter.run

```python
def run(file_paths: Union[Path, List[Path]], meta: Optional[Union[Dict[str, str], List[Optional[Dict[str, str]]]]] = None, remove_numeric_tables: Optional[bool] = None, known_ligatures: Dict[str, str] = KNOWN_LIGATURES, valid_languages: Optional[List[str]] = None, encoding: Optional[str] = "UTF-8", id_hash_keys: Optional[List[str]] = None)
```

Extract text from a file.

**Arguments**:

- `file_paths`: Path to the files you want to convert
- `meta`: Optional dictionary with metadata that shall be attached to all resulting documents.
Can be any custom keys and values.
- `remove_numeric_tables`: This option uses heuristics to remove numeric rows from the tables.
The tabular structures in documents might be noise for the reader model if it
does not have table parsing capability for finding answers. However, tables
may also have long strings that could possible candidate for searching answers.
The rows containing strings are thus retained in this option.
- `known_ligatures`: Some converters tends to recognize clusters of letters as ligatures, such as "ﬀ" (double f).
Such ligatures however make text hard to compare with the content of other files,
which are generally ligature free. Therefore we automatically find and replace the most
common ligatures with their split counterparts. The default mapping is in
`haystack.nodes.file_converter.base.KNOWN_LIGATURES`: it is rather biased towards Latin alphabeths
but excludes all ligatures that are known to be used in IPA.
You can use this parameter to provide your own set of ligatures to clean up from the documents.
- `valid_languages`: validate languages from a list of languages specified in the ISO 639-1
(https://en.wikipedia.org/wiki/ISO_639-1) format.
This option can be used to add test for encoding errors. If the extracted text is
not one of the valid languages, then it might likely be encoding error resulting
in garbled text.
- `encoding`: Select the file encoding (default is `UTF-8`)
- `id_hash_keys`: Generate the document id from a custom list of strings that refer to the document's
attributes. If you want to ensure you don't have duplicate documents in your DocumentStore but texts are
not unique, you can modify the metadata and pass e.g. `"meta"` to this field (e.g. [`"content"`, `"meta"`]).
In this case the id will be generated by using the content and the defined metadata.

<a id="docx"></a>

# Module docx

<a id="docx.DocxToTextConverter"></a>

## DocxToTextConverter

```python
class DocxToTextConverter(BaseConverter)
```

<a id="docx.DocxToTextConverter.convert"></a>

#### DocxToTextConverter.convert

```python
def convert(file_path: Path, meta: Optional[Dict[str, str]] = None, remove_numeric_tables: Optional[bool] = None, valid_languages: Optional[List[str]] = None, encoding: Optional[str] = None, id_hash_keys: Optional[List[str]] = None) -> List[Document]
```

Extract text from a .docx file.

Note: As docx doesn't contain "page" information, we actually extract and return a list of paragraphs here.
For compliance with other converters we nevertheless opted for keeping the methods name.

**Arguments**:

- `file_path`: Path to the .docx file you want to convert
- `meta`: dictionary of meta data key-value pairs to append in the returned document.
- `remove_numeric_tables`: This option uses heuristics to remove numeric rows from the tables.
The tabular structures in documents might be noise for the reader model if it
does not have table parsing capability for finding answers. However, tables
may also have long strings that could possible candidate for searching answers.
The rows containing strings are thus retained in this option.
- `valid_languages`: validate languages from a list of languages specified in the ISO 639-1
(https://en.wikipedia.org/wiki/ISO_639-1) format.
This option can be used to add test for encoding errors. If the extracted text is
not one of the valid languages, then it might likely be encoding error resulting
in garbled text.
- `encoding`: Not applicable
- `id_hash_keys`: Generate the document id from a custom list of strings that refer to the document's
attributes. If you want to ensure you don't have duplicate documents in your DocumentStore but texts are
not unique, you can modify the metadata and pass e.g. `"meta"` to this field (e.g. [`"content"`, `"meta"`]).
In this case the id will be generated by using the content and the defined metadata.

<a id="image"></a>

# Module image

<a id="image.ImageToTextConverter"></a>

## ImageToTextConverter

```python
class ImageToTextConverter(BaseConverter)
```

<a id="image.ImageToTextConverter.__init__"></a>

#### ImageToTextConverter.\_\_init\_\_

```python
def __init__(remove_numeric_tables: bool = False, valid_languages: Optional[List[str]] = ["eng"], id_hash_keys: Optional[List[str]] = None)
```

**Arguments**:

- `remove_numeric_tables`: This option uses heuristics to remove numeric rows from the tables.
The tabular structures in documents might be noise for the reader model if it
does not have table parsing capability for finding answers. However, tables
may also have long strings that could possible candidate for searching answers.
The rows containing strings are thus retained in this option.
- `valid_languages`: validate languages from a list of languages specified here
(https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html)
This option can be used to add test for encoding errors. If the extracted text is
not one of the valid languages, then it might likely be encoding error resulting
in garbled text. Run the following line of code to check available language packs:
# List of available languages
print(pytesseract.get_languages(config=''))
- `id_hash_keys`: Generate the document id from a custom list of strings that refer to the document's
attributes. If you want to ensure you don't have duplicate documents in your DocumentStore but texts are
not unique, you can modify the metadata and pass e.g. `"meta"` to this field (e.g. [`"content"`, `"meta"`]).
In this case the id will be generated by using the content and the defined metadata.

<a id="image.ImageToTextConverter.convert"></a>

#### ImageToTextConverter.convert

```python
def convert(file_path: Union[Path, str], meta: Optional[Dict[str, str]] = None, remove_numeric_tables: Optional[bool] = None, valid_languages: Optional[List[str]] = None, encoding: Optional[str] = None, id_hash_keys: Optional[List[str]] = None) -> List[Document]
```

Extract text from image file using the pytesseract library (https://github.com/madmaze/pytesseract)

**Arguments**:

- `file_path`: path to image file
- `meta`: Optional dictionary with metadata that shall be attached to all resulting documents.
Can be any custom keys and values.
- `remove_numeric_tables`: This option uses heuristics to remove numeric rows from the tables.
The tabular structures in documents might be noise for the reader model if it
does not have table parsing capability for finding answers. However, tables
may also have long strings that could possible candidate for searching answers.
The rows containing strings are thus retained in this option.
- `valid_languages`: validate languages from a list of languages supported by tessarect
(https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html).
This option can be used to add test for encoding errors. If the extracted text is
not one of the valid languages, then it might likely be encoding error resulting
in garbled text.
- `encoding`: Not applicable
- `id_hash_keys`: Generate the document id from a custom list of strings that refer to the document's
attributes. If you want to ensure you don't have duplicate documents in your DocumentStore but texts are
not unique, you can modify the metadata and pass e.g. `"meta"` to this field (e.g. [`"content"`, `"meta"`]).
In this case the id will be generated by using the content and the defined metadata.

<a id="markdown"></a>

# Module markdown

<a id="markdown.MarkdownConverter"></a>

## MarkdownConverter

```python
class MarkdownConverter(BaseConverter)
```

<a id="markdown.MarkdownConverter.convert"></a>

#### MarkdownConverter.convert

```python
def convert(file_path: Path, meta: Optional[Dict[str, str]] = None, remove_numeric_tables: Optional[bool] = None, valid_languages: Optional[List[str]] = None, encoding: Optional[str] = "utf-8", id_hash_keys: Optional[List[str]] = None) -> List[Document]
```

Reads text from a txt file and executes optional preprocessing steps.

**Arguments**:

- `file_path`: path of the file to convert
- `meta`: dictionary of meta data key-value pairs to append in the returned document.
- `encoding`: Select the file encoding (default is `utf-8`)
- `remove_numeric_tables`: Not applicable
- `valid_languages`: Not applicable
- `id_hash_keys`: Generate the document id from a custom list of strings that refer to the document's
attributes. If you want to ensure you don't have duplicate documents in your DocumentStore but texts are
not unique, you can modify the metadata and pass e.g. `"meta"` to this field (e.g. [`"content"`, `"meta"`]).
In this case the id will be generated by using the content and the defined metadata.

<a id="markdown.MarkdownConverter.markdown_to_text"></a>

#### MarkdownConverter.markdown\_to\_text

```python
@staticmethod
def markdown_to_text(markdown_string: str) -> str
```

Converts a markdown string to plaintext

**Arguments**:

- `markdown_string`: String in markdown format

<a id="pdf"></a>

# Module pdf

<a id="pdf.PDFToTextConverter"></a>

## PDFToTextConverter

```python
class PDFToTextConverter(BaseConverter)
```

<a id="pdf.PDFToTextConverter.__init__"></a>

#### PDFToTextConverter.\_\_init\_\_

```python
def __init__(remove_numeric_tables: bool = False, valid_languages: Optional[List[str]] = None, id_hash_keys: Optional[List[str]] = None, encoding: Optional[str] = "UTF-8")
```

**Arguments**:

- `remove_numeric_tables`: This option uses heuristics to remove numeric rows from the tables.
The tabular structures in documents might be noise for the reader model if it
does not have table parsing capability for finding answers. However, tables
may also have long strings that could possible candidate for searching answers.
The rows containing strings are thus retained in this option.
- `valid_languages`: validate languages from a list of languages specified in the ISO 639-1
(https://en.wikipedia.org/wiki/ISO_639-1) format.
This option can be used to add test for encoding errors. If the extracted text is
not one of the valid languages, then it might likely be encoding error resulting
in garbled text.
- `id_hash_keys`: Generate the document id from a custom list of strings that refer to the document's
attributes. If you want to ensure you don't have duplicate documents in your DocumentStore but texts are
not unique, you can modify the metadata and pass e.g. `"meta"` to this field (e.g. [`"content"`, `"meta"`]).
In this case the id will be generated by using the content and the defined metadata.
- `encoding`: Encoding that will be passed as `-enc` parameter to `pdftotext`.
Defaults to "UTF-8" in order to support special characters (e.g. German Umlauts, Cyrillic ...).
(See list of available encodings, such as "Latin1", by running `pdftotext -listenc` in the terminal)

<a id="pdf.PDFToTextConverter.convert"></a>

#### PDFToTextConverter.convert

```python
def convert(file_path: Path, meta: Optional[Dict[str, str]] = None, remove_numeric_tables: Optional[bool] = None, valid_languages: Optional[List[str]] = None, encoding: Optional[str] = None, id_hash_keys: Optional[List[str]] = None) -> List[Document]
```

Extract text from a .pdf file using the pdftotext library (https://www.xpdfreader.com/pdftotext-man.html)

**Arguments**:

- `file_path`: Path to the .pdf file you want to convert
- `meta`: Optional dictionary with metadata that shall be attached to all resulting documents.
Can be any custom keys and values.
- `remove_numeric_tables`: This option uses heuristics to remove numeric rows from the tables.
The tabular structures in documents might be noise for the reader model if it
does not have table parsing capability for finding answers. However, tables
may also have long strings that could possible candidate for searching answers.
The rows containing strings are thus retained in this option.
- `valid_languages`: validate languages from a list of languages specified in the ISO 639-1
(https://en.wikipedia.org/wiki/ISO_639-1) format.
This option can be used to add test for encoding errors. If the extracted text is
not one of the valid languages, then it might likely be encoding error resulting
in garbled text.
- `encoding`: Encoding that overwrites self.encoding and will be passed as `-enc` parameter to `pdftotext`.
(See list of available encodings by running `pdftotext -listenc` in the terminal)
- `id_hash_keys`: Generate the document id from a custom list of strings that refer to the document's
attributes. If you want to ensure you don't have duplicate documents in your DocumentStore but texts are
not unique, you can modify the metadata and pass e.g. `"meta"` to this field (e.g. [`"content"`, `"meta"`]).
In this case the id will be generated by using the content and the defined metadata.

<a id="pdf.PDFToTextOCRConverter"></a>

## PDFToTextOCRConverter

```python
class PDFToTextOCRConverter(BaseConverter)
```

<a id="pdf.PDFToTextOCRConverter.__init__"></a>

#### PDFToTextOCRConverter.\_\_init\_\_

```python
def __init__(remove_numeric_tables: bool = False, valid_languages: Optional[List[str]] = ["eng"], id_hash_keys: Optional[List[str]] = None)
```

Extract text from image file using the pytesseract library (https://github.com/madmaze/pytesseract)

**Arguments**:

- `remove_numeric_tables`: This option uses heuristics to remove numeric rows from the tables.
The tabular structures in documents might be noise for the reader model if it
does not have table parsing capability for finding answers. However, tables
may also have long strings that could possible candidate for searching answers.
The rows containing strings are thus retained in this option.
- `valid_languages`: validate languages from a list of languages supported by tessarect
(https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html).
This option can be used to add test for encoding errors. If the extracted text is
not one of the valid languages, then it might likely be encoding error resulting
in garbled text.
- `id_hash_keys`: Generate the document id from a custom list of strings that refer to the document's
attributes. If you want to ensure you don't have duplicate documents in your DocumentStore but texts are
not unique, you can modify the metadata and pass e.g. `"meta"` to this field (e.g. [`"content"`, `"meta"`]).
In this case the id will be generated by using the content and the defined metadata.

<a id="pdf.PDFToTextOCRConverter.convert"></a>

#### PDFToTextOCRConverter.convert

```python
def convert(file_path: Path, meta: Optional[Dict[str, str]] = None, remove_numeric_tables: Optional[bool] = None, valid_languages: Optional[List[str]] = None, encoding: Optional[str] = None, id_hash_keys: Optional[List[str]] = None) -> List[Document]
```

Convert a file to a dictionary containing the text and any associated meta data.

File converters may extract file meta like name or size. In addition to it, user
supplied meta data like author, url, external IDs can be supplied as a dictionary.

**Arguments**:

- `file_path`: path of the file to convert
- `meta`: dictionary of meta data key-value pairs to append in the returned document.
- `remove_numeric_tables`: This option uses heuristics to remove numeric rows from the tables.
The tabular structures in documents might be noise for the reader model if it
does not have table parsing capability for finding answers. However, tables
may also have long strings that could possible candidate for searching answers.
The rows containing strings are thus retained in this option.
- `valid_languages`: validate languages from a list of languages specified in the ISO 639-1
(https://en.wikipedia.org/wiki/ISO_639-1) format.
This option can be used to add test for encoding errors. If the extracted text is
not one of the valid languages, then it might likely be encoding error resulting
in garbled text.
- `encoding`: Not applicable
- `id_hash_keys`: Generate the document id from a custom list of strings that refer to the document's
attributes. If you want to ensure you don't have duplicate documents in your DocumentStore but texts are
not unique, you can modify the metadata and pass e.g. `"meta"` to this field (e.g. [`"content"`, `"meta"`]).
In this case the id will be generated by using the content and the defined metadata.

<a id="tika"></a>

# Module tika

<a id="tika.TikaConverter"></a>

## TikaConverter

```python
class TikaConverter(BaseConverter)
```

<a id="tika.TikaConverter.__init__"></a>

#### TikaConverter.\_\_init\_\_

```python
def __init__(tika_url: str = "http://localhost:9998/tika", remove_numeric_tables: bool = False, valid_languages: Optional[List[str]] = None, id_hash_keys: Optional[List[str]] = None)
```

**Arguments**:

- `tika_url`: URL of the Tika server
- `remove_numeric_tables`: This option uses heuristics to remove numeric rows from the tables.
The tabular structures in documents might be noise for the reader model if it
does not have table parsing capability for finding answers. However, tables
may also have long strings that could possible candidate for searching answers.
The rows containing strings are thus retained in this option.
- `valid_languages`: validate languages from a list of languages specified in the ISO 639-1
(https://en.wikipedia.org/wiki/ISO_639-1) format.
This option can be used to add test for encoding errors. If the extracted text is
not one of the valid languages, then it might likely be encoding error resulting
in garbled text.
- `id_hash_keys`: Generate the document id from a custom list of strings that refer to the document's
attributes. If you want to ensure you don't have duplicate documents in your DocumentStore but texts are
not unique, you can modify the metadata and pass e.g. `"meta"` to this field (e.g. [`"content"`, `"meta"`]).
In this case the id will be generated by using the content and the defined metadata.

<a id="tika.TikaConverter.convert"></a>

#### TikaConverter.convert

```python
def convert(file_path: Path, meta: Optional[Dict[str, str]] = None, remove_numeric_tables: Optional[bool] = None, valid_languages: Optional[List[str]] = None, encoding: Optional[str] = None, id_hash_keys: Optional[List[str]] = None) -> List[Document]
```

**Arguments**:

- `file_path`: path of the file to convert
- `meta`: dictionary of meta data key-value pairs to append in the returned document.
- `remove_numeric_tables`: This option uses heuristics to remove numeric rows from the tables.
The tabular structures in documents might be noise for the reader model if it
does not have table parsing capability for finding answers. However, tables
may also have long strings that could possible candidate for searching answers.
The rows containing strings are thus retained in this option.
- `valid_languages`: validate languages from a list of languages specified in the ISO 639-1
(https://en.wikipedia.org/wiki/ISO_639-1) format.
This option can be used to add test for encoding errors. If the extracted text is
not one of the valid languages, then it might likely be encoding error resulting
in garbled text.
- `encoding`: Not applicable
- `id_hash_keys`: Generate the document id from a custom list of strings that refer to the document's
attributes. If you want to ensure you don't have duplicate documents in your DocumentStore but texts are
not unique, you can modify the metadata and pass e.g. `"meta"` to this field (e.g. [`"content"`, `"meta"`]).
In this case the id will be generated by using the content and the defined metadata.

**Returns**:

A list of pages and the extracted meta data of the file.

<a id="txt"></a>

# Module txt

<a id="txt.TextConverter"></a>

## TextConverter

```python
class TextConverter(BaseConverter)
```

<a id="txt.TextConverter.convert"></a>

#### TextConverter.convert

```python
def convert(file_path: Path, meta: Optional[Dict[str, str]] = None, remove_numeric_tables: Optional[bool] = None, valid_languages: Optional[List[str]] = None, encoding: Optional[str] = "utf-8", id_hash_keys: Optional[List[str]] = None) -> List[Document]
```

Reads text from a txt file and executes optional preprocessing steps.

**Arguments**:

- `file_path`: path of the file to convert
- `meta`: dictionary of meta data key-value pairs to append in the returned document.
- `remove_numeric_tables`: This option uses heuristics to remove numeric rows from the tables.
The tabular structures in documents might be noise for the reader model if it
does not have table parsing capability for finding answers. However, tables
may also have long strings that could possible candidate for searching answers.
The rows containing strings are thus retained in this option.
- `valid_languages`: validate languages from a list of languages specified in the ISO 639-1
(https://en.wikipedia.org/wiki/ISO_639-1) format.
This option can be used to add test for encoding errors. If the extracted text is
not one of the valid languages, then it might likely be encoding error resulting
in garbled text.
- `encoding`: Select the file encoding (default is `utf-8`)
- `id_hash_keys`: Generate the document id from a custom list of strings that refer to the document's
attributes. If you want to ensure you don't have duplicate documents in your DocumentStore but texts are
not unique, you can modify the metadata and pass e.g. `"meta"` to this field (e.g. [`"content"`, `"meta"`]).
In this case the id will be generated by using the content and the defined metadata.
