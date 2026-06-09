from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1200, 'height': 800})
    page.goto('http://localhost:9999/index.html', wait_until='networkidle')
    
    print("✅ ページ読み込み成功")
    print(f"   タイトル: {page.title()}")
    
    # アフィリエイトリンク確認
    html = page.content()
    a8_links = html.count('px.a8.net')
    print(f"✅ A8.netリンク: {a8_links}件")
    
    # 主要要素
    if '💳 診断スタート' in html:
        print(f"✅ 診断開始ボタン: あり")
    
    # FAQページスキーマ
    if 'FAQPage' in html:
        print(f"✅ FAQPageスキーマ: あり")
    
    # スクリーンショット
    page.screenshot(path='/tmp/point-opt-desk.png')
    
    # モバイル
    page_m = browser.new_page(viewport={'width': 375, 'height': 667})
    page_m.goto('http://localhost:9999/index.html')
    page_m.screenshot(path='/tmp/point-opt-mobile.png')
    
    print(f"✅ スクリーンショット保存: /tmp/point-opt-*.png")
    
    browser.close()
