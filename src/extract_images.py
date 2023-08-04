from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING
from zipfile import ZipFile

from openpyxl import load_workbook
from openpyxl_image_loader import SheetImageLoader
from PIL import Image

if TYPE_CHECKING:
    from typing import Generator, Literal


@dataclass
class Record:
    name: str
    image: Image.Image
    src: Literal["sign"] | Literal["photo"]


def load_records(
    table_filepath: Path, photos_filepath: Path
) -> Generator[Record, None, None]:
    workbook = load_workbook(table_filepath)
    sheet = workbook[workbook.sheetnames[0]]
    image_loader = SheetImageLoader(sheet)

    with ZipFile(photos_filepath) as photos_zip:
        for row in sheet.iter_rows(min_row=2, min_col=2):
            name: str = row[0].value  # type: ignore

            if (photo_filename := row[1].value) is not None:  # type: ignore
                photo_filename: str
                with photos_zip.open(photo_filename) as file:
                    photo = Image.open(BytesIO(file.read()))
            else:
                photo = None

            if image_loader.image_in(row[2].coordinate):
                sign = image_loader.get(row[2].coordinate)
            else:
                sign = None

            assert (
                sum(i is not None for i in (photo, sign)) == 1
            ), f"“{name}”没有正常提供照片或签名：{photo = }，{sign = }"

            yield Record(
                name=name,
                image=photo or sign,  # type: ignore
                src="photo" if photo else "sign",
            )


if __name__ == "__main__":
    table_filepath = next((Path.home() / "Downloads").glob("*.xlsx"))
    photos_filepath = next((Path.home() / "Downloads").glob("*.zip"))
    out_dir = Path("out")
    threshold = 130

    out_dir.mkdir(exist_ok=True)

    records = load_records(table_filepath, photos_filepath)
    for r in records:
        if r.src == "photo":
            if r.image.format == "JPEG":
                # 删除背景
                print(f"正在给“{r.name}”删除背景。")
                r.image.putalpha(
                    r.image.convert("L").point(lambda x: 255 if x < threshold else 0)
                )

        r.image.save(out_dir / f"{r.name}.png")
