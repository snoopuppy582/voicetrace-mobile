from __future__ import annotations

import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parents[0]
MOBILE_ASSETS = PROJECT_ROOT / "04_프로토타입" / "voicetrace-mobile" / "assets"
GENERATED_BG = Path(
    r"C:\Users\mnb09\.codex\generated_images\019edca5-209d-73f3-8524-b07f814ec49f\ig_09df938377ad3e8d016a34e3783d3c81919ef899d75957015c.png"
)

SOURCE_DIR = ROOT / "source"
FEATURE_DIR = ROOT / "feature_graphic"
SCREENSHOT_DIR = ROOT / "screenshots_phone"
ICON_DIR = ROOT / "icons"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path(r"C:\Windows\Fonts\malgunbd.ttf" if bold else r"C:\Windows\Fonts\malgun.ttf"),
        Path(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


FONT_REG = lambda size: font(size, False)
FONT_BOLD = lambda size: font(size, True)


def ensure_dirs() -> None:
    for path in [SOURCE_DIR, FEATURE_DIR, SCREENSHOT_DIR, ICON_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def crop_cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    src_w, src_h = image.size
    scale = max(target_w / src_w, target_h / src_h)
    new_w, new_h = int(src_w * scale), int(src_h * scale)
    resized = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def gradient(size: tuple[int, int], top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        color = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        for x in range(w):
            px[x, y] = color
    return img


def fit_text(draw: ImageDraw.ImageDraw, text: str, font_obj: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split(" ")
    lines: list[str] = []
    current = ""
    for word in words:
        probe = word if not current else f"{current} {word}"
        if draw.textbbox((0, 0), probe, font=font_obj)[2] <= max_width:
            current = probe
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wave(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], color: tuple[int, int, int, int], width: int = 6) -> None:
    left, top, right, bottom = box
    mid = (top + bottom) / 2
    amp = (bottom - top) * 0.34
    points = []
    steps = 160
    for i in range(steps + 1):
        x = left + (right - left) * i / steps
        y = mid + math.sin(i / steps * math.pi * 6.0) * amp * (0.65 + 0.35 * math.sin(i / steps * math.pi))
        points.append((x, y))
    draw.line(points, fill=color, width=width, joint="curve")


def draw_icon_base(size: int, transparent_bg: bool = False, monochrome: bool = False) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0) if transparent_bg else (236, 247, 255, 255))
    draw = ImageDraw.Draw(img, "RGBA")
    pad = int(size * 0.09)
    if not transparent_bg:
        bg = gradient((size, size), (242, 250, 255), (198, 231, 255)).convert("RGBA")
        img.alpha_composite(bg)
    card = (pad, pad, size - pad, size - pad)
    if monochrome:
        draw.rounded_rectangle(card, radius=int(size * 0.22), fill=(0, 0, 0, 255))
        wave = (255, 255, 255, 255)
        accent = (255, 255, 255, 255)
    else:
        draw.rounded_rectangle(card, radius=int(size * 0.22), fill=(22, 102, 216, 255))
        draw.rounded_rectangle(
            (card[0] + int(size * 0.025), card[1] + int(size * 0.025), card[2] - int(size * 0.025), card[3] - int(size * 0.025)),
            radius=int(size * 0.2),
            outline=(126, 214, 255, 100),
            width=max(3, size // 80),
        )
        wave = (255, 255, 255, 245)
        accent = (255, 191, 78, 255)
    draw_wave(draw, (int(size * 0.22), int(size * 0.28), int(size * 0.78), int(size * 0.56)), wave, width=max(5, size // 34))
    bars = [0.26, 0.42, 0.34, 0.58, 0.76, 0.52, 0.67, 0.38]
    start_x = int(size * 0.25)
    bar_w = max(6, size // 42)
    gap = max(8, size // 36)
    base_y = int(size * 0.74)
    for idx, value in enumerate(bars):
        x = start_x + idx * (bar_w + gap)
        h = int(size * value * 0.34)
        color = accent if idx in {4, 6} else wave
        draw.rounded_rectangle((x, base_y - h, x + bar_w, base_y), radius=bar_w // 2, fill=color)
    draw.ellipse((int(size * 0.67), int(size * 0.64), int(size * 0.82), int(size * 0.79)), fill=(255, 255, 255, 255))
    draw.line((int(size * 0.707), int(size * 0.71), int(size * 0.74), int(size * 0.745), int(size * 0.785), int(size * 0.675)), fill=(22, 102, 216, 255), width=max(4, size // 52))
    return img


def make_icons() -> None:
    backup_dir = MOBILE_ASSETS / "original_expo_defaults"
    backup_dir.mkdir(exist_ok=True)
    for asset in MOBILE_ASSETS.glob("*.png"):
        target = backup_dir / asset.name
        if not target.exists():
            shutil.copy2(asset, target)

    play_icon = draw_icon_base(512)
    play_icon.save(ICON_DIR / "play_icon_512.png")

    draw_icon_base(1024).save(MOBILE_ASSETS / "icon.png")
    draw_icon_base(1024).save(MOBILE_ASSETS / "splash-icon.png")
    draw_icon_base(432, transparent_bg=True).save(MOBILE_ASSETS / "android-icon-foreground.png")
    gradient((432, 432), (230, 246, 255), (188, 225, 255)).save(MOBILE_ASSETS / "android-icon-background.png")
    draw_icon_base(432, transparent_bg=True, monochrome=True).save(MOBILE_ASSETS / "android-icon-monochrome.png")
    draw_icon_base(64).resize((48, 48), Image.Resampling.LANCZOS).save(MOBILE_ASSETS / "favicon.png")


def make_feature_graphic() -> None:
    if GENERATED_BG.exists():
        shutil.copy2(GENERATED_BG, SOURCE_DIR / "feature_background_imagegen.png")
        bg = Image.open(GENERATED_BG).convert("RGB")
    else:
        bg = gradient((1792, 1024), (239, 249, 255), (24, 84, 170))
    canvas = crop_cover(bg, (1024, 500)).convert("RGBA")
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay, "RGBA")
    for x in range(560):
        alpha = int(235 * (1 - x / 560))
        od.line((x, 0, x, 500), fill=(255, 255, 255, alpha))
    od.rectangle((0, 0, 1024, 500), fill=(5, 35, 95, 18))
    canvas.alpha_composite(overlay)
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rounded_rectangle((54, 56, 132, 134), radius=22, fill=(22, 102, 216, 255))
    draw_wave(draw, (69, 78, 117, 104), (255, 255, 255, 240), width=4)
    draw.text((54, 154), "VoiceTrace AI", font=FONT_BOLD(58), fill=(13, 28, 47, 255))
    draw.text((56, 226), "AI 영상·음성 업로드 전", font=FONT_BOLD(28), fill=(25, 57, 92, 255))
    draw.text((56, 264), "품질 리포트 앱", font=FONT_BOLD(28), fill=(25, 57, 92, 255))
    chip_y = 338
    chips = [("HNR", "#2468D8"), ("HF ratio", "#00A6D6"), ("Upload readiness", "#B76B00")]
    x = 56
    for label, color in chips:
        w = draw.textbbox((0, 0), label, font=FONT_BOLD(18))[2] + 38
        rgb = tuple(int(color[i : i + 2], 16) for i in (1, 3, 5))
        draw.rounded_rectangle((x, chip_y, x + w, chip_y + 42), radius=20, fill=rgb + (235,))
        draw.text((x + 19, chip_y + 10), label, font=FONT_BOLD(18), fill=(255, 255, 255, 255))
        x += w + 12
    draw.text((58, 438), "Creator Preflight Report", font=FONT_REG(18), fill=(74, 92, 112, 255))
    out = canvas.convert("RGB")
    out.save(FEATURE_DIR / "feature_graphic_1024x500.png")
    out.save(FEATURE_DIR / "feature_graphic_1024x500.jpg", quality=94)


def draw_phone_frame(draw: ImageDraw.ImageDraw) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = 128, 96, 952, 1824
    draw.rounded_rectangle((x0, y0, x1, y1), radius=64, fill=(17, 30, 46, 255))
    draw.rounded_rectangle((x0 + 18, y0 + 18, x1 - 18, y1 - 18), radius=50, fill=(245, 247, 251, 255))
    draw.rounded_rectangle((456, 120, 624, 154), radius=17, fill=(17, 30, 46, 255))
    return x0 + 38, y0 + 58, x1 - 38, y1 - 58


def draw_status_bar(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, _ = box
    draw.text((x0 + 18, y0 + 6), "9:41", font=FONT_BOLD(23), fill=(18, 26, 36, 255))
    draw.rounded_rectangle((x1 - 92, y0 + 12, x1 - 34, y0 + 33), radius=8, outline=(18, 26, 36, 255), width=2)
    draw.rectangle((x1 - 88, y0 + 16, x1 - 44, y0 + 29), fill=(18, 26, 36, 255))
    draw.rectangle((x1 - 30, y0 + 18, x1 - 26, y0 + 27), fill=(18, 26, 36, 255))


def draw_panel(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, title: str) -> int:
    draw.rounded_rectangle((x, y, x + w, y + h), radius=8, fill=(255, 255, 255, 255), outline=(217, 226, 236, 255), width=2)
    draw.text((x + 32, y + 26), title, font=FONT_BOLD(29), fill=(18, 26, 36, 255))
    return y + 82


def draw_metric_card(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, label: str, value: str, color=(18, 26, 36, 255)) -> None:
    draw.rounded_rectangle((x, y, x + w, y + 116), radius=8, fill=(255, 255, 255, 255), outline=(217, 226, 236, 255), width=2)
    draw.text((x + 18, y + 18), label, font=FONT_BOLD(17), fill=(107, 119, 133, 255))
    draw.text((x + 18, y + 54), value, font=FONT_BOLD(28), fill=color)


def draw_chart(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, color=(36, 104, 216, 255)) -> None:
    draw.rounded_rectangle((x, y, x + w, y + h), radius=8, fill=(255, 255, 255, 255), outline=(217, 226, 236, 255), width=2)
    vals = [0.84, 0.78, 0.88, 0.72, 0.81, 0.69, 0.86, 0.74]
    gap = 24
    bar_w = (w - 86 - gap * (len(vals) - 1)) // len(vals)
    base = y + h - 28
    for i, v in enumerate(vals):
        bx = x + 42 + i * (bar_w + gap)
        bh = int((h - 64) * v)
        draw.rounded_rectangle((bx, base - bh, bx + bar_w, base), radius=bar_w // 2, fill=color)


def draw_bullet(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, color=(36, 104, 216, 255)) -> int:
    draw.ellipse((x, y + 10, x + 12, y + 22), fill=color)
    lines = fit_text(draw, text, FONT_REG(24), 650)
    cy = y
    for line in lines:
        draw.text((x + 26, cy), line, font=FONT_REG(24), fill=(76, 91, 107, 255))
        cy += 34
    return cy + 8


def make_screenshot(title: str, subtitle: str, variant: str, output: Path) -> None:
    canvas = gradient((1080, 1920), (238, 248, 255), (232, 240, 249)).convert("RGBA")
    draw = ImageDraw.Draw(canvas, "RGBA")
    screen = draw_phone_frame(draw)
    x0, y0, x1, y1 = screen
    draw_status_bar(draw, screen)
    content_x = x0 + 34
    content_w = x1 - x0 - 68
    y = y0 + 70
    draw.text((content_x, y), "Creator Preflight Report", font=FONT_BOLD(21), fill=(36, 104, 216, 255))
    y += 34
    draw.text((content_x, y), "VoiceTrace AI", font=FONT_BOLD(52), fill=(18, 26, 36, 255))
    y += 70
    for line in fit_text(draw, subtitle, FONT_REG(24), content_w):
        draw.text((content_x, y), line, font=FONT_REG(24), fill=(95, 108, 123, 255))
        y += 34
    y += 16

    if variant == "input":
        py = draw_panel(draw, content_x, y, content_w, 466, "분석 입력")
        draw.text((content_x + 32, py), "FastAPI 서버 주소", font=FONT_BOLD(22), fill=(36, 52, 71, 255))
        draw.rounded_rectangle((content_x + 32, py + 40, content_x + content_w - 32, py + 96), radius=6, fill=(255, 255, 255, 255), outline=(217, 226, 236, 255), width=2)
        draw.text((content_x + 50, py + 54), "http://10.0.2.2:8000", font=FONT_REG(22), fill=(18, 26, 36, 255))
        draw.text((content_x + 32, py + 124), "오디오/비디오 파일", font=FONT_BOLD(22), fill=(36, 52, 71, 255))
        draw.rounded_rectangle((content_x + 32, py + 164, content_x + content_w - 32, py + 222), radius=6, outline=(36, 104, 216, 255), width=2)
        draw.text((content_x + 302, py + 179), "파일 선택", font=FONT_BOLD(23), fill=(36, 104, 216, 255))
        draw.rounded_rectangle((content_x + 32, py + 288, content_x + content_w - 32, py + 350), radius=6, fill=(36, 104, 216, 255))
        draw.text((content_x + 236, py + 305), "서버 분석 리포트 생성", font=FONT_BOLD(24), fill=(255, 255, 255, 255))
        y += 500
    elif variant == "selected":
        py = draw_panel(draw, content_x, y, content_w, 480, "파일 업로드")
        draw.rounded_rectangle((content_x + 32, py, content_x + content_w - 32, py + 92), radius=8, fill=(245, 247, 251, 255), outline=(217, 226, 236, 255), width=2)
        draw.text((content_x + 52, py + 18), "sample_voice_video.mp4", font=FONT_BOLD(24), fill=(18, 26, 36, 255))
        draw.text((content_x + 52, py + 54), "18.42MB · video/mp4", font=FONT_REG(20), fill=(95, 108, 123, 255))
        draw.rounded_rectangle((content_x + 32, py + 132, content_x + content_w - 32, py + 194), radius=6, fill=(36, 104, 216, 255))
        draw.text((content_x + 236, py + 149), "서버 분석 리포트 생성", font=FONT_BOLD(24), fill=(255, 255, 255, 255))
        draw.text((content_x + 32, py + 230), "서버로 파일을 업로드하고 음성 특징을 계산합니다.", font=FONT_REG(22), fill=(95, 108, 123, 255))
        draw_chart(draw, content_x + 32, py + 286, content_w - 64, 142, (36, 104, 216, 255))
        y += 510
    elif variant == "result":
        py = draw_panel(draw, content_x, y, content_w, 754, "분석 결과")
        card_w = (content_w - 64 - 20) // 3
        draw_metric_card(draw, content_x + 32, py, card_w, "HNR", "15.2 dB")
        draw_metric_card(draw, content_x + 32 + card_w + 10, py, card_w, "HF ratio", "0.27")
        draw_metric_card(draw, content_x + 32 + (card_w + 10) * 2, py, card_w, "Readiness", "82/100", (36, 104, 216, 255))
        draw_chart(draw, content_x + 32, py + 144, content_w - 64, 214, (36, 104, 216, 255))
        draw.rounded_rectangle((content_x + 32, py + 388, content_x + content_w - 32, py + 548), radius=8, fill=(245, 247, 251, 255), outline=(217, 226, 236, 255), width=2)
        draw.text((content_x + 56, py + 414), "양호", font=FONT_BOLD(28), fill=(18, 26, 36, 255))
        desc = "업로드 전 점검 기준에 비교적 안정적으로 들어옵니다. 최종 음량과 영상 싱크만 확인하면 됩니다."
        ly = py + 458
        for line in fit_text(draw, desc, FONT_REG(22), content_w - 112):
            draw.text((content_x + 56, ly), line, font=FONT_REG(22), fill=(76, 91, 107, 255))
            ly += 31
        draw.text((content_x + 32, py + 588), "개선 제안", font=FONT_BOLD(24), fill=(18, 26, 36, 255))
        by = py + 630
        by = draw_bullet(draw, content_x + 34, by, "최종 업로드 전 전체 영상 싱크와 음량 확인")
        draw_bullet(draw, content_x + 34, by, "리포트 수치를 제작 로그에 저장")
        y += 786
    else:
        py = draw_panel(draw, content_x, y, content_w, 620, "제품 설계 메모")
        items = [
            "AI 생성 여부를 단정하지 않고 제작 품질 리포트로 제공",
            "HNR, HF ratio, 클리핑, 무음 비율 기반 품질 신호 계산",
            "업로드 파일은 분석 후 임시 처리·삭제 정책을 적용",
            "Google Play 제출용 AAB와 내부 테스트 APK 빌드 완료",
        ]
        by = py
        for item in items:
            by = draw_bullet(draw, content_x + 34, by, item)
        draw.rounded_rectangle((content_x + 32, by + 22, content_x + content_w - 32, by + 146), radius=8, fill=(238, 244, 255, 255), outline=(200, 216, 244, 255), width=2)
        note = "HNR/HF ratio는 AI 생성의 법적 증거가 아니라 업로드 전 품질 개선을 위한 참고 지표입니다."
        ly = by + 46
        for line in fit_text(draw, note, FONT_REG(22), content_w - 112):
            draw.text((content_x + 56, ly), line, font=FONT_REG(22), fill=(64, 81, 99, 255))
            ly += 31
        y += 650

    draw.rounded_rectangle((146, 1810, 934, 1872), radius=28, fill=(255, 255, 255, 180))
    draw.text((186, 1826), title, font=FONT_BOLD(23), fill=(25, 57, 92, 255))
    canvas.convert("RGB").save(output)


def make_screenshots() -> None:
    subtitle = "생성형 영상 속 인물 음성의 자연스러움, 잡음, 고주파 거칠음을 점검하는 제작자용 품질 리포트 앱"
    make_screenshot("1. 서버 주소와 파일을 선택하는 입력 화면", subtitle, "input", SCREENSHOT_DIR / "01_input_1080x1920.png")
    make_screenshot("2. 오디오·비디오 파일 업로드 흐름", subtitle, "selected", SCREENSHOT_DIR / "02_upload_1080x1920.png")
    make_screenshot("3. HNR·HF ratio·업로드 준비도 결과", subtitle, "result", SCREENSHOT_DIR / "03_report_1080x1920.png")
    make_screenshot("4. 제작자용 품질 리포트와 한계 문구", subtitle, "note", SCREENSHOT_DIR / "04_caveat_1080x1920.png")


def write_manifest() -> None:
    manifest = ROOT / "STORE_ASSETS_MANIFEST.md"
    manifest.write_text(
        "\n".join(
            [
                "# VoiceTrace AI Store Assets Manifest",
                "",
                "## Google Play 규격 파일",
                "",
                "- `icons/play_icon_512.png`: 512x512 PNG 앱 아이콘",
                "- `feature_graphic/feature_graphic_1024x500.png`: 1024x500 PNG feature graphic",
                "- `feature_graphic/feature_graphic_1024x500.jpg`: 1024x500 JPG feature graphic 백업",
                "- `screenshots_phone/01_input_1080x1920.png`: 휴대폰 스크린샷 1",
                "- `screenshots_phone/02_upload_1080x1920.png`: 휴대폰 스크린샷 2",
                "- `screenshots_phone/03_report_1080x1920.png`: 휴대폰 스크린샷 3",
                "- `screenshots_phone/04_caveat_1080x1920.png`: 휴대폰 스크린샷 4",
                "",
                "## 생성 방식",
                "",
                "- Feature graphic 배경은 Codex `imagegen` built-in tool로 생성한 이미지를 사용했다.",
                "- 텍스트, 아이콘, 스크린샷은 Google Play 규격에 맞게 로컬 렌더링했다.",
                "- 현재 연결된 Android 기기/에뮬레이터가 없어 `adb screencap` 실기기 촬영은 수행하지 못했다.",
                "",
                "## 앱 자산 반영",
                "",
                "- Expo 기본 아이콘은 `voicetrace-mobile/assets/original_expo_defaults/`에 백업했다.",
                "- `assets/icon.png`, `splash-icon.png`, Android adaptive icon 자산을 VoiceTrace AI 브랜드 아이콘으로 교체했다.",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    make_icons()
    make_feature_graphic()
    make_screenshots()
    write_manifest()
    print(f"generated={ROOT}")


if __name__ == "__main__":
    main()
