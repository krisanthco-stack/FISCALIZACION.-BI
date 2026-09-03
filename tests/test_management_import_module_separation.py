from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text(encoding='utf-8')


def test_management_has_separate_excel_import_control():
    assert 'id="managementExcelImport"' in HTML
    assert 'Cargar Excel' in HTML
    assert 'accept=".xlsx,.csv' in HTML


def test_management_excel_import_targets_management_module():
    assert "importExcelFile(f,'management')" in HTML or 'importExcelFile(f,\'management\')' in HTML
    assert "function applyImportDestination(c,destination='tramites')" in HTML


def test_tramites_import_rejects_management_zip_instead_of_absorbing_it():
    assert 'Este ZIP pertenece a Gestión' in HTML
    assert 'ZIP recuperado en Trámites' not in HTML
    assert 'puede cargarse desde Trámites' not in HTML


def test_management_package_forces_restored_cases_to_management():
    # Importing a management ZIP must explicitly apply the management destination,
    # even for old records whose workflow metadata is incomplete.
    segment = HTML[HTML.index('async function importManagementPackage(file)'):HTML.index('function bindPackageControls()')]
    assert "applyImportDestination(record,'management')" in segment


def test_official_desktop_distribution_does_not_define_linux_targets():
    package = (ROOT / 'desktop/package.json').read_text(encoding='utf-8').lower()
    release = (ROOT / '.github/workflows/release.yml').read_text(encoding='utf-8').lower()
    assert 'appimage' not in package
    assert '"linux"' not in package
    assert 'release-linux' not in release
    assert '\n  linux:' not in release
