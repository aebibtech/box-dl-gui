Set-Location $PSScriptRoot
& venv/Scripts/Activate.ps1

$global:out = ''
$global:subfol = ''
function Write-Out {
    Write-Output "Download Path:" $global:subfol
}

function clo {
    Clear-Host
    Write-Out
}

function dl {
    if($null -eq $args[0]) {
        Write-Host "dl - Download Command"
        Write-Host
        Write-Host
        Write-Host "Usage:"
        Write-Host "    dl <box.com url>"
        Write-Host "    example: dl https://app.box.com/s/r559z7glalffa4mksm6v0rhgsve1fiyu"
        Write-Host
        Write-Host
    } else {
        python.exe .\main.py $args[0] --driver-path 'C:/ProgramData/chocolatey/lib/chromedriver/tools/chromedriver.exe' --out $global:subfol
    }
}

function Set-SubFol {
    $e = '/'
    if(-not $args[0]) {
        $e = ''
    }
    $global:subfol = ($global:out) + "/" + $args[0] + $e
    Clear-Host
    Write-Host $global:subfol
}

Set-Alias -Name sf -Value Set-SubFol

$BOXDLPATH = ''

if(-not (Test-Path ~\boxdlpath.txt)) {
    Write-Warning "Please use forward slashes."
    $BOXDLPATH = Read-Host -Prompt "Main folder for Box downloads"
    
    if($BOXDLPATH -eq '') {
        Write-Host
        Write-Error "No path specified. Aborting."
        Write-Host
        exit
    }

    if(Test-Path $BOXDLPATH.Replace('/', '\')) {
        New-Item ~\boxdlpath.txt
        if($BOXDLPATH.EndsWith("/")) {
          $global:out = $BOXDLPATH.Remove($BOXDLPATH.Length - 1)
          Set-Content -Path ~\boxdlpath.txt -Value $global:out
        } else {
            Set-Content -Path ~\boxdlpath.txt -Value $BOXDLPATH
            $global:out = $BOXDLPATH
        }
    } else {
        Write-Host
        Write-Error "Path not found. Aborting."
        Write-Host
        exit
    }
} else {
    $global:out = Get-Content -Path ~\boxdlpath.txt
}

$sub = Read-Host -Prompt "Subfolder"
Set-SubFol $sub

