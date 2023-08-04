from pathlib import Path

from PIL import Image


def merge(images_dir: Path, names: list[str]) -> Image.Image:
    # 估计尺寸
    sizes = ([], [])
    for n in names:
        if (file := images_dir / f"{n}.png").exists():
            with Image.open(file) as image:
                w, h = image.size
                sizes[0].append(w)
                sizes[1].append(h)
    width, height = (sum(dim) / len(dim) for dim in sizes)
    step_h = 1.1 * height
    step_w = 2 * width

    # 绘制
    canvas = Image.new("RGBA", (round(step_w), round(len(names) * step_h)))
    for i, n in enumerate(names):
        if (file := images_dir / f"{n}.png").exists():
            with Image.open(file) as image:
                k = (width / image.width + height / image.height) / 2
                size = tuple(round(s * k) for s in image.size)
                canvas.paste(
                    image.resize(size),
                    (
                        round(step_w / 2 - size[0] / 2),
                        round((i + 1 / 2) * step_h - size[1] / 2),
                    ),
                )

    return canvas


if __name__ == "__main__":
    names = Path("names.txt").read_text().splitlines()
    out_dir = Path("out")

    merge(out_dir, names).save(out_dir / "merged.png")
