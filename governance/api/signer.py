from typing import Optional


class QESSigner:
    """
    Tämä on QES-yhteensopiva rajapinta.
    Integroi esim.:
    - DigiDoc
    - eIDAS-palvelut
    - DocuSign Qualified
    """

    def __init__(self, provider: str = "external_qes_provider"):
        self.provider = provider

    def sign_pdf(self, pdf_path: str, output_path: Optional[str] = None) -> str:
        """
        Stub – korvaa tuotannossa aidolla QES-rajapinnalla.
        """
        if output_path is None:
            output_path = pdf_path.replace(".pdf", "_signed.pdf")

        # Tässä kohtaa kutsuttaisiin QES API:a.
        # Nyt kopioidaan tiedosto simuloidusti.
        import shutil
        shutil.copy(pdf_path, output_path)
        return output_path
