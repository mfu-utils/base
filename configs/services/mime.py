MIME_MS_WORD = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
MIME_PDF = "application/pdf"

MIME_TEXT = "text/plain"

MIME_TIFF = "image/tiff"
MIME_PNG = "image/png"
MIME_JPEG = "image/jpeg"

__CONFIG__ = {
    # Available mime types for printing
    "available_printing_types": {
        # Document types
        MIME_PDF,
        MIME_MS_WORD,

        # Text types
        MIME_TEXT,

        # Image types
        MIME_TIFF,
        MIME_PNG,
        MIME_JPEG,
    },

    "doc_mime_types": [
        MIME_MS_WORD,
        MIME_PDF,
    ],

    "images_mime_types": [
        MIME_TIFF,
        MIME_PNG,
        MIME_JPEG,
    ],

    "view_types": {
        MIME_PDF: "Adobe PDF",
        MIME_MS_WORD: "Microsoft Word",
        MIME_TEXT: "Plain text",
        MIME_TIFF: "TIFF image",
        MIME_PNG: "PNG image",
        MIME_JPEG: "JPEG image",
    }
}
