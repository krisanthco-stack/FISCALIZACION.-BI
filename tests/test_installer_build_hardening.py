from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


def test_windows_batch_does_not_announce_stale_26_artifacts():
    batch = read('desktop/BUILD_WINDOWS.cmd')
    assert 'Setup-26.0.0.exe' not in batch
    assert 'Portable-26.0.0.exe' not in batch
    assert 'Fiscalizacion-L26-Setup-*.exe' in batch
    assert 'Fiscalizacion-L26-Portable-*.exe' in batch


def test_windows_builds_retry_transient_npm_network_failures():
    local = read('desktop/BUILD_WINDOWS.cmd').lower()
    workflow = read('.github/workflows/windows.yml').lower()
    release = read('.github/workflows/release.yml').lower()
    for text in (local, workflow, release):
        assert 'fetch-retries' in text
        assert 'fetch-retry-mintimeout' in text
        assert 'fetch-retry-maxtimeout' in text


def test_pdf_vendor_download_retries_each_source():
    vendor = read('scripts/vendor_pdfjs.py')
    assert 'DOWNLOAD_ATTEMPTS = 3' in vendor
    assert 'for attempt in range(1, DOWNLOAD_ATTEMPTS + 1)' in vendor
