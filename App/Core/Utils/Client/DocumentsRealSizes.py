from typing import Tuple, Dict


class DocumentsRealSizes:
    A4 = 'a4'
    A5 = 'a5'
    A6 = 'a6'

    SIZES: Dict[str, Tuple[int, int]] = {
        A4: (210, 297),
        A5: (148, 210),
        A6: (105, 148),
    }

    @staticmethod
    def size(size: str) -> Tuple[int, int]:
        if size := DocumentsRealSizes.SIZES.get(size):
            return size

        raise KeyError(f'Unknown document size "{size}"')

    @staticmethod
    def a4() -> Tuple[int, int]:
        return DocumentsRealSizes.SIZES[DocumentsRealSizes.A4]

    @staticmethod
    def a5() -> Tuple[int, int]:
        return DocumentsRealSizes.SIZES[DocumentsRealSizes.A5]

    @staticmethod
    def a6() -> Tuple[int, int]:
        return DocumentsRealSizes.SIZES[DocumentsRealSizes.A6]
