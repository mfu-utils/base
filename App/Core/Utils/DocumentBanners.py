from enum import Enum


class DocumentBanners(Enum):
    Classified = "classified"
    Confidential = "confidential"
    Secret = "secret"
    Standard = "standard"
    Topsecret = "topsecret"
    Unclassified = "unclassified"
