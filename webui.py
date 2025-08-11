from dotenv import load_dotenv
load_dotenv()
import argparse

# Monkeypatch playwright to always use patchright
try:
    # Import both libraries
    import patchright.async_api as patchright_api
    import playwright.async_api as playwright_api
    
    # Store originals
    original_patchright = patchright_api.async_playwright
    original_playwright = playwright_api.async_playwright
    
    def force_patchright():
        print("🕶️ PATCHRIGHT HERE!!!!! Playwright call hijacked!")
        return original_patchright()
    
    # Force ALL playwright calls to use patchright
    playwright_api.async_playwright = force_patchright
    
    # Also patch any browser-use imports
    def patch_browser_use():
        try:
            from browser_use.browser import types as browser_types
            browser_types.async_playwright = force_patchright
            print("✅ Successfully patched browser_use.browser.types")
        except ImportError:
            pass
    
    patch_browser_use()
    
    print("✅ Successfully hijacked all playwright calls to patchright")
    
except ImportError as e:
    print(f"⚠️ Failed to setup playwright hijack: {e}")

from src.webui.interface import theme_map, create_ui


def main():
    parser = argparse.ArgumentParser(description="Gradio WebUI for Browser Agent")
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="IP address to bind to")
    parser.add_argument("--port", type=int, default=7788, help="Port to listen on")
    parser.add_argument("--theme", type=str, default="Ocean", choices=theme_map.keys(), help="Theme to use for the UI")
    args = parser.parse_args()

    demo = create_ui(theme_name=args.theme)
    demo.queue().launch(server_name=args.ip, server_port=args.port)


if __name__ == '__main__':
    main()
