import re

class Util:
    @staticmethod
    def cleanOrgName(name: str) -> str:
        # remove suffixes that confuse search
        name = re.sub(r",?\s*(Inc\.?|LLC|Ltd\.?|LLP|Co\.?|Group|Corporation|Corp\.?)", "", name, flags=re.I)
        name = re.sub(r"[^a-zA-Z0-9\s]", "", name)  # remove symbols like & or -
        return name.strip()

    @staticmethod
    def normalize(text: str):
        return re.sub(r"[^A-Z0-9\s]", "", text.upper()) 