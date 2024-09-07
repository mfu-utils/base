from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import QWidget


class PdfDoc(QPdfDocument):
    def __init__(self, path: str, parent: QWidget = None):
        super(QPdfDocument, self).__init__(parent)

        self.__document = QPdfDocument()
        self.__document.load(path)

        self.__doc_view = QPdfView()
        self.__doc_view.setObjectName("PrintingFileParametersPDFView")
        self.__doc_view.setPageMode(QPdfView.PageMode.MultiPage)
        self.__doc_view.setZoomMode(QPdfView.ZoomMode.FitInView)
        self.__doc_view.setDocument(self.__document)
