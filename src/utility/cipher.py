class CaesarCipher:
    """
    Cifra de César com offset fixo = 5.
    Métodos:
        - encode(text: str) -> str
        - decode(text: str) -> str
    Só opera sobre letras A-Z e a-z; outros caracteres são preservados.
    """
    OFFSET = 5

    @classmethod
    def _shift_char(cls, ch: str, offset: int) -> str:
        """Desloca um único caractere alfabético; preserva case."""
        if 'A' <= ch <= 'Z':
            base = ord('A')
            return chr((ord(ch) - base + offset) % 26 + base)
        if 'a' <= ch <= 'z':
            base = ord('a')
            return chr((ord(ch) - base + offset) % 26 + base)
        return ch

    @classmethod
    def encode(cls, text: str) -> str:
        """Codifica text deslocando cada letra +5."""
        return ''.join(cls._shift_char(ch, cls.OFFSET) for ch in text)

    @classmethod
    def decode(cls, text: str) -> str:
        """Decodifica text deslocando cada letra -5."""
        return ''.join(cls._shift_char(ch, -cls.OFFSET) for ch in text)
