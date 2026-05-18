from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "custom_components" / "m3566_rgb" / "brand"

COLORS = {
    "bg": (16, 20, 24, 255),
    "body": (29, 39, 48, 255),
    "strip": (45, 59, 69, 255),
    "edge": (217, 238, 245, 230),
    "red": (255, 59, 48, 255),
    "green": (52, 199, 89, 255),
    "blue": (10, 132, 255, 255),
}


def make_asset(size: int, path: Path) -> None:
    image = Image.new("RGBA", (size, size), COLORS["bg"])
    draw = ImageDraw.Draw(image)
    scale = size / 108

    def points(items: list[tuple[int, int]]) -> list[tuple[int, int]]:
        return [(int(x * scale), int(y * scale)) for x, y in items]

    draw.polygon(points([(18, 68), (78, 28), (90, 40), (30, 80)]), fill=COLORS["body"])
    draw.polygon(points([(24, 67), (77, 32), (84, 39), (31, 74)]), fill=COLORS["strip"])

    for x, y, color in (
        (35, 59, COLORS["red"]),
        (53, 47, COLORS["green"]),
        (71, 35, COLORS["blue"]),
    ):
        radius = int(7 * scale)
        center_x = int(x * scale)
        center_y = int(y * scale)
        draw.ellipse(
            (
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
            ),
            fill=color,
        )

    draw.polygon(points([(25, 77), (83, 38), (88, 43), (31, 82)]), fill=COLORS["edge"])
    image.save(path)


def main() -> None:
    BRAND.mkdir(parents=True, exist_ok=True)
    make_asset(256, BRAND / "icon.png")
    make_asset(512, BRAND / "logo.png")
    make_asset(512, ROOT / "logo.png")


if __name__ == "__main__":
    main()
