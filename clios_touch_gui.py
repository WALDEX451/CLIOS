import os
import time
import socket
import psutil
from PIL import Image, ImageDraw, ImageFont


FRAMEBUFFER = "/dev/fb1"
WIDTH = 480
HEIGHT = 320


def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "offline"


def write_framebuffer(image):
    image = image.convert("RGB")
    pixels = image.load()

    data = bytearray()

    for y in range(HEIGHT):
        for x in range(WIDTH):
            r, g, b = pixels[x, y]

            # RGB888 naar RGB565
            rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

            # little endian
            data.append(rgb565 & 0xFF)
            data.append((rgb565 >> 8) & 0xFF)

    with open(FRAMEBUFFER, "wb") as fb:
        fb.write(data)


def draw_gui():
    image = Image.new("RGB", (WIDTH, HEIGHT), (5, 8, 18))
    draw = ImageDraw.Draw(image)

    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
        normal_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except Exception:
        title_font = None
        normal_font = None
        small_font = None

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    ip = get_ip()
    now = time.strftime("%H:%M:%S")

    draw.rectangle((0, 0, WIDTH, 58), fill=(0, 40, 90))
    draw.text((18, 10), "CLIOS TOUCH", fill=(255, 255, 255), font=title_font)

    draw.text((20, 80), f"STATUS: ONLINE", fill=(0, 255, 140), font=normal_font)
    draw.text((20, 115), f"IP: {ip}", fill=(230, 230, 230), font=normal_font)
    draw.text((20, 150), f"CPU: {cpu}%", fill=(230, 230, 230), font=normal_font)
    draw.text((20, 185), f"RAM: {ram}%", fill=(230, 230, 230), font=normal_font)
    draw.text((20, 220), f"DISK: {disk}%", fill=(230, 230, 230), font=normal_font)

    draw.rectangle((20, 265, 460, 305), outline=(0, 180, 255), width=2)
    draw.text((35, 273), f"MISSION READY  |  {now}", fill=(0, 180, 255), font=small_font)

    return image


def main():
    if not os.path.exists(FRAMEBUFFER):
        print(f"[CLIOS TOUCH ERROR] {FRAMEBUFFER} bestaat niet.")
        print("Check met: ls /dev/fb*")
        return

    print("[CLIOS TOUCH] Mini GUI gestart op", FRAMEBUFFER)

    while True:
        image = draw_gui()
        write_framebuffer(image)
        time.sleep(1)


if __name__ == "__main__":
    main()
