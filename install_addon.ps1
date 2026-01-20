# AI 3D Generator - Quick Installation Script
# This script helps you install the add-on to Blender

Write-Host "=== AI 3D Generator - Blender Add-on Installer ===" -ForegroundColor Cyan
Write-Host ""

# Find Blender installation
$blenderPaths = @(
    "$env:ProgramFiles\Blender Foundation",
    "${env:ProgramFiles(x86)}\Blender Foundation",
    "$env:LOCALAPPDATA\Programs\Blender Foundation"
)

$blenderFound = $false
$blenderVersion = ""

foreach ($path in $blenderPaths) {
    if (Test-Path $path) {
        Write-Host "Found Blender installation at: $path" -ForegroundColor Green
        $blenderFound = $true
        
        # Find version folders
        $versionFolders = Get-ChildItem -Path $path -Directory | Where-Object { $_.Name -match "Blender" }
        
        if ($versionFolders) {
            Write-Host "Available Blender versions:" -ForegroundColor Yellow
            foreach ($folder in $versionFolders) {
                Write-Host "  - $($folder.Name)" -ForegroundColor Yellow
            }
            $blenderVersion = $versionFolders[0].Name
        }
        break
    }
}

if (-not $blenderFound) {
    Write-Host "Blender installation not found in common locations." -ForegroundColor Red
    Write-Host "Please install Blender 3.0+ from: https://www.blender.org/download/" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Or manually copy the 'ai_3d_generator' folder to your Blender add-ons directory:" -ForegroundColor Yellow
    Write-Host "  %appdata%\Blender Foundation\Blender\[Version]\scripts\addons\" -ForegroundColor Cyan
    exit
}

# Find add-ons directory
$addonsPath = "$env:APPDATA\Blender Foundation\Blender"

if (Test-Path $addonsPath) {
    # Find the latest Blender version folder
    $versionDirs = Get-ChildItem -Path $addonsPath -Directory | Sort-Object Name -Descending
    
    if ($versionDirs.Count -gt 0) {
        $latestVersion = $versionDirs[0].Name
        $targetAddonsPath = "$addonsPath\$latestVersion\scripts\addons"
        
        Write-Host ""
        Write-Host "Target add-ons directory: $targetAddonsPath" -ForegroundColor Cyan
        
        # Create addons directory if it doesn't exist
        if (-not (Test-Path $targetAddonsPath)) {
            Write-Host "Creating add-ons directory..." -ForegroundColor Yellow
            New-Item -ItemType Directory -Path $targetAddonsPath -Force | Out-Null
        }
        
        # Copy add-on
        $sourcePath = $PSScriptRoot
        $destinationPath = "$targetAddonsPath\ai_3d_generator"
        
        Write-Host ""
        Write-Host "Installing add-on..." -ForegroundColor Yellow
        Write-Host "  From: $sourcePath" -ForegroundColor Gray
        Write-Host "  To:   $destinationPath" -ForegroundColor Gray
        
        # Check if add-on already exists
        if (Test-Path $destinationPath) {
            Write-Host ""
            Write-Host "Add-on already exists at destination!" -ForegroundColor Yellow
            $overwrite = Read-Host "Do you want to overwrite it? (y/n)"
            
            if ($overwrite -ne "y") {
                Write-Host "Installation cancelled." -ForegroundColor Red
                exit
            }
            
            Write-Host "Removing old version..." -ForegroundColor Yellow
            Remove-Item -Path $destinationPath -Recurse -Force
        }
        
        # Copy files
        Copy-Item -Path $sourcePath -Destination $destinationPath -Recurse -Force
        
        Write-Host ""
        Write-Host "✓ Add-on installed successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Cyan
        Write-Host "  1. Open Blender" -ForegroundColor White
        Write-Host "  2. Go to Edit → Preferences → Add-ons" -ForegroundColor White
        Write-Host "  3. Search for 'AI 3D Generator'" -ForegroundColor White
        Write-Host "  4. Enable the add-on by checking the checkbox" -ForegroundColor White
        Write-Host "  5. Press 'N' in 3D View to see the panel" -ForegroundColor White
        Write-Host ""
        Write-Host "For detailed instructions, see: INSTALL.md" -ForegroundColor Gray
        
    } else {
        Write-Host "No Blender version folders found in AppData." -ForegroundColor Red
        Write-Host "Please run Blender at least once before installing add-ons." -ForegroundColor Yellow
    }
} else {
    Write-Host "Blender AppData directory not found." -ForegroundColor Red
    Write-Host "Please run Blender at least once to create the necessary directories." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
