# pip install .
# python setup.py sdist bdist

Write-Host "Running test suite..."
python -m pytest -q
if ($LASTEXITCODE -ne 0) {
    Write-Error "Pytest failed. Aborting build."
    exit 1
}

$initFile = "org_analyze/__init__.py"
$versionLine = Select-String -Path $initFile -Pattern '__version__\s*=\s*["'']([\d\.]+)["'']'
if ($versionLine) {
    $version = $versionLine.Matches[0].Groups[1].Value
    Write-Host "Version: ${version}"
}

Write-Host "Building the package..."
python -m build

Write-Host "Installing the built package..."
pip install --force-reinstall "dist/org_analyze-${version}-py3-none-any.whl"
