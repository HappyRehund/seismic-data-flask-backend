from dataclasses import dataclass


@dataclass
class ImageDimensions:
    section_type: str
    section_number: int
    width: int
    height: int
    image_path: str

    def to_dict(self) -> dict:
        return {
            "section_type": self.section_type,
            "section_number": self.section_number,
            "width": self.width,
            "height": self.height,
            "image_path": self.image_path,
        }