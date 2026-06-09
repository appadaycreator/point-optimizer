import subprocess
import time
import json

# サーバ起動
subprocess.Popen(['python3', '-m', 'http.server', '8080'], 
                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(2)

# Playwright で検証
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Desktop view
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1200, 'height': 800})
    page.goto('http://localhost:8080/index.html', wait_until='networkidle')
    
    print("=== Point Optimizer 検証結果 ===\n")
    
    # ページタイトル確認
    title = page.title()
    print(f"✅ ページタイトル: {title}")
    
    # ページ内容確認
    content = page.content()
    
    # アフィリエイトリンク確認
    a8_count = content.count('px.a8.net')
    print(f"✅ A8.netアフィリエイトリンク数: {a8_count}件")
    
    # FAQ確認
    faq_count = content.count('<details')
    print(f"✅ FAQセクション: {faq_count}個")
    
    # 診断開始ボタン
    start_btn = page.query_selector('button:has-text("💳 診断スタート")')
    if start_btn:
        print(f"✅ 診断開始ボタン: 表示確認")
    
    # スクリーンショット
    page.screenshot(path='/tmp/point_opt_desktop.png')
    print(f"📸 デスクトップスクリーンショット保存")
    
    # モバイルビューで再確認
    page_mobile = browser.new_page(viewport={'width': 375, 'height': 667})
    page_mobile.goto('http://localhost:8080/index.html', wait_until='networkidle')
    page_mobile.screenshot(path='/tmp/point_opt_mobile.png')
    print(f"📱 モバイルスクリーンショット保存")
    
    # 診断フロー動作確認
    start_btn_mobile = page_mobile.query_selector('button')
    if start_btn_mobile:
        start_btn_mobile.click()
        time.sleep(1)
        
        # 質問表示確認
        q_text = page_mobile.query_selector('id=qText')
        if q_text:
            print(f"✅ 質問フロー: 正常に開始")
        
        # 選択肢表示確認
        choices = page_mobile.query_selector_all('.choice-btn')
        print(f"✅ 選択肢表示: {len(choices)}個")
    
    browser.close()
    print("\n✅ 検証完了")
