#!/usr/bin/env python3
"""Scrape JOMOO smart toilet products from ejomoo.com"""

import re
import os
import json
import time
import urllib.request
import urllib.error
import http.cookiejar
from pathlib import Path

BASE_URL = "https://www.ejomoo.com"
OUTPUT_DIR = Path("/root/.openclaw/workspace/jomoo-products/products")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.5",
    "Referer": "https://www.ejomoo.com/",
}

# All product URLs collected from 4 pages
PRODUCTS = [
    # Page 1
    {"url": "/item/ZS860.htm", "model": "ZS860", "list_title": "JOMOO九牧 净界ultra香薰除臭自动翻盖除菌自清洁魔力泡全功能智能马桶ZS860", "price": "¥5129.0"},
    {"url": "/item/ZS800J.htm", "model": "ZS800J", "list_title": "JOMOO九牧 净界pro免触魔力泡除菌自清洁智能马桶ZS800J", "price": "¥4518.0"},
    {"url": "/item/ZS800I.htm", "model": "ZS800I", "list_title": "JOMOO九牧 净界air全域除菌自动翻盖NFC智控智能马桶ZS800I", "price": "¥4400.0"},
    {"url": "/item/ZS780.htm", "model": "ZS780", "list_title": "JOMOO九牧 智能互联除菌自动翻盖魔力泡九牧全家桶智能马桶ZS780", "price": "¥3878.0"},
    {"url": "/item/ZS700P.htm", "model": "ZS700P", "list_title": "JOMOO九牧 全水路除菌旋风魔力泡脚感翻圈轻音智能马桶ZS700P", "price": "¥3528.0"},
    {"url": "/item/ZS711J.htm", "model": "ZS711J", "list_title": "JOMOO九牧 NFC智控脚感开盖魔力泡隔臭除菌无极坑距调节智能马桶ZS711J", "price": "¥3640.0"},
    {"url": "/item/ZS780P.htm", "model": "ZS780P", "list_title": "JOMOO九牧 无极Pro自动翻盖NFC智控魔力泡自清洁卧室静音冲智能马桶ZS780P", "price": "¥3878.0"},
    {"url": "/item/ZS520IS2.htm", "model": "ZS520I-S2", "list_title": "JOMOO九牧 净味桶铂金除臭免触脚感冲水水包水静音冲智能马桶ZS520I-S2", "price": "¥2389.0"},
    # Page 2
    {"url": "/item/ZS680U.htm", "model": "ZS680U", "list_title": "JOMOO九牧 无水压静音冲全水路除菌魔力泡免触脚感翻盖智能马桶ZS680U", "price": "¥3340.0"},
    {"url": "/item/ZS690P.htm", "model": "ZS690P", "list_title": "JOMOO九牧 脚感免触NFC智控静音冲无极坑距调节智能马桶ZS690P", "price": "¥3040.0"},
    {"url": "/item/ZS680I.htm", "model": "ZS680I", "list_title": "JOMOO九牧 旋风魔力泡无棱易洁NFC智控脚感静音冲智能马桶ZS680I", "price": "¥2689.0"},
    {"url": "/item/ZS710J.htm", "model": "ZS710J", "list_title": "JOMOO九牧 NFC智控全水路除菌脚感翻盖智能马桶ZS710J", "price": "¥3640.0"},
    {"url": "/item/ZS690I.htm", "model": "ZS690I", "list_title": "JOMOO九牧 无水压静音冲脚感免触无棱易洁除臭智能马桶ZS690I", "price": "¥2740.0"},
    {"url": "/item/ZS680.htm", "model": "ZS680", "list_title": "JOMOO九牧 零水压限制魔力泡防护除臭抗菌激光脚感智能马桶ZS680", "price": "¥2689.0"},
    {"url": "/item/ZS760J-S1.htm", "model": "ZS760J", "list_title": "JOMOO九牧 卧室洗静音冲脚感冲刷除臭抗菌无棱内壁智能马桶ZS760J", "price": "¥2840.0"},
    {"url": "/item/ZS300P.htm", "model": "ZS300P", "list_title": "JOMOO九牧 无水压限制智慧大小冲抗菌除臭内置水箱智能马桶ZS300P", "price": "¥1989.0"},
    # Page 3 - smart toilets only (skip accessories)
    {"url": "/item/ZD8920-SA-CJM400.htm", "model": "ZD8920", "list_title": "九牧 i90智能免触自动翻盖魔力泡3重防护净力冲3.0智能马桶ZD8920", "price": "¥13349.0"},
    {"url": "/item/ZD8611.htm", "model": "ZD8611", "list_title": "JOMOO九牧 ZD8611 P50壁挂式紫外线杀菌智能坐便器", "price": "¥11349.0"},
    # Page 3 - accessories
    {"url": "/item/ZS021.htm", "model": "ZS021", "list_title": "JOMOO九牧 脉冲强洗抗菌恒温座圈智能盖板 ZS021", "price": "¥940.0", "category": "accessory"},
    {"url": "/item/13D900-2065.htm", "model": "13D900-2065", "list_title": "JOMOO九牧 高精滤内置阻垢式智能马桶滤芯13D900-2065", "price": "¥34.0", "category": "accessory"},
    {"url": "/item/KD903-1073.htm", "model": "KD903-1073", "list_title": "九牧 智能马桶滤芯阻垢式双重防护过滤芯KD903-1073", "price": "¥198.0", "category": "accessory"},
    {"url": "/item/13D900.htm", "model": "13D900", "list_title": "JOMOO九牧 智能马桶发泡剂 防溅防臭防粘杀菌4重魔力泡13D900", "price": "¥22.0", "category": "accessory"},
    {"url": "/item/74120.htm", "model": "74120", "list_title": "JOMOO九牧 独立快装增压劲冲马桶伴侣喷枪花洒74120", "price": "¥141.0", "category": "accessory"},
    {"url": "/item/X74107.htm", "model": "X74107", "list_title": "JOMOO九牧 加厚黄铜防爆双控双出智能马桶伴侣喷枪角阀X74107", "price": "¥222.0", "category": "accessory"},
    # Page 4
    {"url": "/item/ZS860-1.htm", "model": "ZS860-1", "list_title": "JOMOO九牧 净界ultra自动翻盖除菌香薰除臭自清洁魔力泡全功能智能马桶ZS860", "price": "¥5763.0"},
]

# Vietnamese translations for common features
FEATURE_VI = {
    "智能马桶": "Bồn cầu thông minh",
    "智能坐便器": "Bệ xí thông minh",
    "智能盖板": "Nắp bồn cầu thông minh",
    "自动翻盖": "Tự động mở nắp",
    "免触": "Không chạm",
    "脚感": "Cảm biến chân",
    "NFC智控": "Điều khiển thông minh NFC",
    "魔力泡": "Bọt ma thuật (Magic Foam)",
    "除菌": "Diệt khuẩn",
    "除臭": "Khử mùi",
    "自清洁": "Tự làm sạch",
    "香薰": "Hương thơm",
    "香氛": "Hương thơm",
    "静音冲": "Xả êm",
    "轻音冲": "Xả siêu êm",
    "全水路": "Toàn bộ đường nước",
    "水路除菌": "Diệt khuẩn đường nước",
    "无水压": "Không cần áp lực nước",
    "零水压限制": "Không giới hạn áp lực nước",
    "魔力泡": "Bọt ma thuật",
    "旋风": "Xoáy",
    "无棱易洁": "Không góc cạnh, dễ vệ sinh",
    "抗菌": "Kháng khuẩn",
    "恒温": "Duyệt nhiệt độ",
    "座圈": "Bệ ngồi",
    "脉冲": "Xung",
    "强洗": "Rửa mạnh",
    "壁挂式": "Gắn tường",
    "紫外线杀菌": "Diệt khuẩn bằng tia UV",
    "烘干": "Sấy khô",
    "移动烘干": "Sấy khô di động",
    "全域除菌": "Diệt khuẩn toàn diện",
    "净界": "Giới hạn sạch",
    "pro": "Pro",
    "ultra": "Ultra",
    "air": "Air",
    "i90": "i90",
    "P50": "P50",
    "净味桶": "Thùng khử mùi",
    "铂金除臭": "Khử mùi bạch kim",
    "水包水": "Nước bao nước",
    "卧室洗": "Rửa phòng ngủ",
    "智慧大小冲": "Xả thông minh lớn/nhỏ",
    "内置水箱": "Bể nước tích hợp",
    "激光": "Laser",
    "无极坑距调节": "Điều chỉnh khoảng cách không giới hạn",
    "智能互联": "Kết nối thông minh",
    "全家桶": "Bộ đầy đủ",
    "滤芯": "Lõi lọc",
    "发泡剂": "Chất tạo bọt",
    "喷枪": "Súng phun",
    "角阀": "Van góc",
}


def fetch_page(url, retries=3):
    """Fetch a page with retries"""
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            resp = opener.open(req, timeout=15)
            return resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            print(f"  Retry {attempt+1}/{retries} for {url}: {e}")
            time.sleep(2)
    return None


def extract_detail_images(html):
    """Extract detail images from the JavaScript embedded HTML"""
    images = []
    # Find the desImg variable content
    des_match = re.search(r"var desImg = '(.*?)';", html, re.DOTALL)
    if des_match:
        des_html = des_match.group(1)
        imgs = re.findall(r'(?:src|data-original)="(http://img-store\.jomoo\.com[^"]+)"', des_html)
        images.extend(imgs)

    # Also find templateImg
    tpl_match = re.search(r"var templateImg = '(.*?)';", html, re.DOTALL)
    if tpl_match and tpl_match.group(1).strip():
        tpl_html = tpl_match.group(1)
        imgs = re.findall(r'(?:src|data-original)="(http://img-store\.jomoo\.com[^"]+)"', tpl_html)
        images.extend(imgs)

    # Find afterImg
    after_match = re.search(r"var afterImg = '(.*?)';", html, re.DOTALL)
    if after_match:
        after_html = after_match.group(1)
        imgs = re.findall(r'(?:src|data-original)="(http://img-store\.jomoo\.com[^"]+)"', after_html)
        images.extend(imgs)

    return list(dict.fromkeys(images))  # dedupe preserving order


def extract_gallery_images(html):
    """Extract gallery/thumbnail images"""
    imgs = re.findall(r'img-store\.jomoo\.com//?dev1/[^\s"<>\']+\.fid', html)
    return list(dict.fromkeys([f"http://{u}" for u in imgs]))


def extract_title(html):
    """Extract product title from page"""
    m = re.search(r'<h1[^>]*class="[^"]*y_title[^"]*"[^>]*>(.*?)</h1>', html, re.DOTALL)
    if m:
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    m = re.search(r'<title>(.*?)</title>', html)
    if m:
        t = m.group(1).strip()
        # Remove site name suffix
        t = re.sub(r'[-_|].*九牧.*$', '', t).strip()
        return t
    return ""


def extract_price(html):
    """Extract price from page"""
    prices = re.findall(r'￥([\d,.]+)', html)
    if prices:
        return prices[0]
    return ""


def extract_specs(html):
    """Extract product specifications"""
    specs = {}
    # Try to find spec parameter area
    spec_section = re.search(r'id="y_parabox"(.*?)</div>\s*<!--', html, re.DOTALL)
    if spec_section:
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', spec_section.group(1), re.DOTALL)
        for row in rows:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
            if len(cells) >= 2:
                key = re.sub(r'<[^>]+>', '', cells[0]).strip()
                val = re.sub(r'<[^>]+>', '', cells[1]).strip()
                if key and val:
                    specs[key] = val

    # Also try extracting from the product info area on the left
    info_area = re.search(r'y_itembox(.*?)y_rightbox', html, re.DOTALL)
    if info_area:
        text = info_area.group(1)
        # Look for patterns like 坑距: 305
        kv_pairs = re.findall(r'([\u4e00-\u9fff]+)\s*[：:]\s*([^\s<]+)', text)
        for k, v in kv_pairs:
            if len(k) > 1 and len(v) < 50:
                specs[k] = v

    return specs


def translate_title_to_vietnamese(title, model):
    """Create a Vietnamese product name based on Chinese title"""
    vi_name = f"JOMOO {model}"
    vi_desc = []

    # Extract key features and translate
    for cn, vi in sorted(FEATURE_VI.items(), key=lambda x: -len(x[0])):
        if cn in title:
            vi_desc.append(vi)

    return vi_name, vi_desc


def create_vietnamese_description(product, detail_images, specs, price):
    """Create Vietnamese product description markdown"""
    model = product["model"]
    title = product["list_title"]
    vi_name, vi_features = translate_title_to_vietnamese(title, model)

    lines = []
    lines.append(f"# {vi_name}")
    lines.append("")
    lines.append(f"**Tên gốc (Tiếng Trung):** {title}")
    lines.append("")
    if price:
        lines.append(f"**Giá tham khảo:** ¥{price} (NDT)")
        lines.append("")
    lines.append(f"**Link sản phẩm:** {BASE_URL}{product['url']}")
    lines.append("")
    lines.append("## Tính năng chính")
    lines.append("")
    for feat in vi_features:
        lines.append(f"- {feat}")
    lines.append("")

    if specs:
        lines.append("## Thông số kỹ thuật")
        lines.append("")
        lines.append("| Thông số | Giá trị |")
        lines.append("|---|---|")
        for k, v in specs.items():
            lines.append(f"| {k} | {v} |")
        lines.append("")

    lines.append("## Hình ảnh sản phẩm")
    lines.append("")
    if detail_images:
        for i, img in enumerate(detail_images, 1):
            fname = img.split("/")[-1]
            lines.append(f"![Ảnh {i}](images/{fname})")
            lines.append("")
    else:
        lines.append("_(Không có hình ảnh chi tiết)_")
        lines.append("")

    lines.append("---")
    lines.append(f"_Dữ liệu được cào từ ejomoo.com - {time.strftime('%Y-%m-%d')}_")

    return "\n".join(lines)


def download_image(url, filepath, retries=3):
    """Download an image file"""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": HEADERS["User-Agent"],
                "Referer": "https://www.ejomoo.com/",
            })
            resp = urllib.request.urlopen(req, timeout=15)
            data = resp.read()
            with open(filepath, "wb") as f:
                f.write(data)
            return True
        except Exception as e:
            print(f"    Retry {attempt+1}/{retries} for image: {e}")
            time.sleep(1)
    return False


def scrape_product(product):
    """Scrape a single product"""
    model = product["model"]
    url = BASE_URL + product["url"]
    category = product.get("category", "smart_toilet")

    print(f"\n{'='*60}")
    print(f"Scraping: {model} - {url}")

    html = fetch_page(url)
    if not html:
        print(f"  FAILED to fetch {url}")
        return None

    # Extract data
    title = extract_title(html) or product["list_title"]
    price = extract_price(html) or product.get("price", "").replace("¥", "")
    detail_images = extract_detail_images(html)
    gallery_images = extract_gallery_images(html)
    specs = extract_specs(html)

    # Combine gallery + detail images, dedupe
    all_images = list(dict.fromkeys(gallery_images + detail_images))

    print(f"  Title: {title[:50]}...")
    print(f"  Price: ¥{price}")
    print(f"  Gallery images: {len(gallery_images)}")
    print(f"  Detail images: {len(detail_images)}")
    print(f"  Total unique images: {len(all_images)}")
    print(f"  Specs: {len(specs)}")

    # Create directory structure
    if category == "accessory":
        product_dir = OUTPUT_DIR / "phu-kien" / model
    else:
        product_dir = OUTPUT_DIR / model

    images_dir = product_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    # Download images
    downloaded = 0
    for i, img_url in enumerate(all_images):
        fname = img_url.split("/")[-1]
        fpath = images_dir / fname
        if fpath.exists():
            downloaded += 1
            continue
        print(f"  Downloading image {i+1}/{len(all_images)}: {fname}")
        if download_image(img_url, fpath):
            downloaded += 1
        time.sleep(0.3)  # rate limit

    print(f"  Downloaded: {downloaded}/{len(all_images)} images")

    # Create Vietnamese description
    product_data = {**product, "list_title": title}
    desc = create_vietnamese_description(product_data, detail_images, specs, price)
    with open(product_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(desc)

    # Save raw data as JSON
    raw_data = {
        "model": model,
        "title": title,
        "price": price,
        "url": url,
        "category": category,
        "specs": specs,
        "gallery_images": gallery_images,
        "detail_images": detail_images,
        "all_images": all_images,
        "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open(product_dir / "product_data.json", "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)

    return raw_data


def main():
    print("JOMOO Smart Toilet Scraper")
    print(f"Total products to scrape: {len(PRODUCTS)}")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    for i, product in enumerate(PRODUCTS):
        print(f"\n[{i+1}/{len(PRODUCTS)}]", end="")
        result = scrape_product(product)
        if result:
            results.append(result)
        time.sleep(1)  # polite delay between products

    # Create index README
    smart_toilets = [r for r in results if r["category"] == "smart_toilet"]
    accessories = [r for r in results if r["category"] == "accessory"]

    index_lines = []
    index_lines.append("# JOMOO Sản phẩm Bồn cầu Thông minh - Bộ sưu tập")
    index_lines.append("")
    index_lines.append(f"_Cào ngày: {time.strftime('%Y-%m-%d')}_")
    index_lines.append(f"_Nguồn: [ejomoo.com](https://www.ejomoo.com/items/zhineng.htm)_")
    index_lines.append("")
    index_lines.append(f"**Tổng cộng:** {len(results)} sản phẩm")
    index_lines.append(f"- Bồn cầu thông minh: {len(smart_toilets)}")
    index_lines.append(f"- Phụ kiện: {len(accessories)}")
    index_lines.append("")
    index_lines.append("## 🚽 Bồn cầu Thông minh")
    index_lines.append("")
    index_lines.append("| STT | Model | Tên sản phẩm | Giá (¥) | Link |")
    index_lines.append("|-----|-------|-------------|---------|------|")
    for i, r in enumerate(smart_toilets, 1):
        index_lines.append(f"| {i} | {r['model']} | {r['title'][:40]}... | ¥{r['price']} | [Xem]({r['url']}) |")
    index_lines.append("")
    index_lines.append("## 🔧 Phụ kiện")
    index_lines.append("")
    for i, r in enumerate(accessories, 1):
        index_lines.append(f"- **{r['model']}** - {r['title'][:50]} (¥{r['price']})")
    index_lines.append("")
    index_lines.append("## Cấu trúc thư mục")
    index_lines.append("")
    index_lines.append("```")
    index_lines.append("products/")
    for r in sorted(results, key=lambda x: (x["category"], x["model"])):
        if r["category"] == "accessory":
            index_lines.append(f"  phu-kien/{r['model']}/")
        else:
            index_lines.append(f"  {r['model']}/")
        index_lines.append(f"    images/     # Hình ảnh sản phẩm")
        index_lines.append(f"    README.md   # Mô tả tiếng Việt")
        index_lines.append(f"    product_data.json  # Dữ liệu thô")
    index_lines.append("```")

    with open(OUTPUT_DIR.parent / "README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(index_lines))

    print(f"\n{'='*60}")
    print(f"DONE! Scraped {len(results)}/{len(PRODUCTS)} products")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
