"""PNG 轉 JPG 工具 — 批次轉換 assets/images 下的所有 PNG 為 JPG"""
import sys
from pathlib import Path
from PIL import Image


def convert_png_to_jpg(directory: str | Path, quality: int = 85, delete_png: bool = False):
    """
    將指定目錄下所有 PNG 圖片轉換為 JPG

    Args:
        directory: 要搜尋的目錄
        quality: JPG 品質（1-95，預設 85）
        delete_png: 轉換後是否刪除原始 PNG
    """
    directory = Path(directory)
    png_files = list(directory.rglob("*.png"))

    if not png_files:
        print(f"在 {directory} 中沒有找到 PNG 檔案。")
        return

    print(f"找到 {len(png_files)} 個 PNG 檔案")
    print(f"JPG 品質：{quality}")
    print(f"轉換後刪除 PNG：{'是' if delete_png else '否'}")
    print("-" * 50)

    converted = 0
    skipped = 0
    total_saved = 0

    for png_path in sorted(png_files):
        jpg_path = png_path.with_suffix(".jpg")

        # 如果 JPG 已存在且比 PNG 新，跳過
        if jpg_path.exists() and jpg_path.stat().st_mtime >= png_path.stat().st_mtime:
            print(f"  ⏭ 跳過（JPG 已存在）: {png_path.relative_to(directory)}")
            skipped += 1
            continue

        try:
            img = Image.open(png_path)

            # 如果有透明通道，轉為白色背景
            if img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                img = background
            elif img.mode != "RGB":
                img = img.convert("RGB")

            img.save(jpg_path, "JPEG", quality=quality, optimize=True)

            png_size = png_path.stat().st_size
            jpg_size = jpg_path.stat().st_size
            saved = png_size - jpg_size
            total_saved += saved
            ratio = (1 - jpg_size / png_size) * 100 if png_size > 0 else 0

            print(f"  ✅ {png_path.relative_to(directory)}")
            print(f"     PNG: {png_size/1024:.1f}KB → JPG: {jpg_size/1024:.1f}KB（節省 {ratio:.1f}%）")

            if delete_png:
                png_path.unlink()
                print(f"     🗑️ 已刪除原始 PNG")

            converted += 1

        except Exception as e:
            print(f"  ❌ 失敗: {png_path.relative_to(directory)} — {e}")

    print("-" * 50)
    print(f"完成！轉換 {converted} 個，跳過 {skipped} 個")
    print(f"總共節省 {total_saved/1024:.1f} KB")


if __name__ == "__main__":
    # 預設目錄
    base_dir = Path(__file__).resolve().parent.parent  # tools/ → 專案根目錄
    images_dir = base_dir / "assets" / "images"

    # 可選參數
    quality = 85
    delete_png = "--delete" in sys.argv
    
    for arg in sys.argv[1:]:
        if arg != "--delete":
            try:
                quality = int(arg)
            except ValueError:
                pass

    print(f"🖼️  PNG → JPG 批次轉換工具")
    print(f"目標目錄：{images_dir}")
    print()

    convert_png_to_jpg(images_dir, quality=quality, delete_png=delete_png)
