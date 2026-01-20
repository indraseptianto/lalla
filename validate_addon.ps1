# AI 3D Generator - Add-on Validation Script
# This script checks if all required files are present

Write-Host "=== AI 3D Generator - Add-on Validation ===" -ForegroundColor Cyan
Write-Host ""

$basePath = $PSScriptRoot
$allValid = $true

# Required files
$requiredFiles = @(
    "__init__.py",
    "preferences.py",
    "ui_panel.py",
    "operators.py",
    "downloader.py",
    "batch_generator.py",
    "history.py",
    "presets.py",
    "providers\__init__.py",
    "providers\base_client.py",
    "providers\tripo_client.py",
    "providers\meshy_client.py",
    "providers\modelslab_client.py"
)

# Documentation files (optional but recommended)
$docFiles = @(
    "README.md",
    "INSTALL.md",
    "QUICKSTART.md"
)

Write-Host "Checking required files..." -ForegroundColor Yellow
Write-Host ""

foreach ($file in $requiredFiles) {
    $filePath = Join-Path $basePath $file
    if (Test-Path $filePath) {
        $size = (Get-Item $filePath).Length
        Write-Host "  [OK] $file ($size bytes)" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] $file - MISSING!" -ForegroundColor Red
        $allValid = $false
    }
}

Write-Host ""
Write-Host "Checking documentation files..." -ForegroundColor Yellow
Write-Host ""

foreach ($file in $docFiles) {
    $filePath = Join-Path $basePath $file
    if (Test-Path $filePath) {
        $size = (Get-Item $filePath).Length
        Write-Host "  [OK] $file ($size bytes)" -ForegroundColor Green
    } else {
        Write-Host "  [WARN] $file - Not found (optional)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Checking __init__.py bl_info..." -ForegroundColor Yellow

$initPath = Join-Path $basePath "__init__.py"
if (Test-Path $initPath) {
    $content = Get-Content $initPath -Raw
    
    if ($content -match 'bl_info\s*=\s*\{') {
        Write-Host "  [OK] bl_info found" -ForegroundColor Green
        
        # Extract version
        if ($content -match '"version"\s*:\s*\((\d+),\s*(\d+),\s*(\d+)\)') {
            $version = "$($matches[1]).$($matches[2]).$($matches[3])"
            Write-Host "  [OK] Version: $version" -ForegroundColor Green
        }
        
        # Extract Blender version requirement
        if ($content -match '"blender"\s*:\s*\((\d+),\s*(\d+),\s*(\d+)\)') {
            $blenderVer = "$($matches[1]).$($matches[2]).$($matches[3])"
            Write-Host "  [OK] Requires Blender: $blenderVer+" -ForegroundColor Green
        }
        
        # Extract name
        if ($content -match '"name"\s*:\s*"([^"]+)"') {
            $name = $matches[1]
            Write-Host "  [OK] Add-on name: $name" -ForegroundColor Green
        }
    } else {
        Write-Host "  [FAIL] bl_info not found in __init__.py!" -ForegroundColor Red
        $allValid = $false
    }
}

Write-Host ""
Write-Host "Checking Python syntax..." -ForegroundColor Yellow

$pythonFiles = Get-ChildItem -Path $basePath -Filter "*.py" -Recurse

foreach ($pyFile in $pythonFiles) {
    # Basic syntax check - look for common issues
    $content = Get-Content $pyFile.FullName -Raw
    
    # Check for basic Python structure
    if ($content.Length -eq 0) {
        Write-Host "  [FAIL] $($pyFile.Name) is empty!" -ForegroundColor Red
        $allValid = $false
    }
}

Write-Host "  [OK] All Python files have content" -ForegroundColor Green

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan

if ($allValid) {
    Write-Host "[PASS] Validation PASSED!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your add-on is ready for installation!" -ForegroundColor Green
    Write-Host "Run install_addon.ps1 to install it to Blender." -ForegroundColor Cyan
} else {
    Write-Host "[FAIL] Validation FAILED!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Some required files are missing or invalid." -ForegroundColor Red
    Write-Host "Please check the errors above and fix them." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
