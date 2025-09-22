param(
    [string]$Name = "rl-labs-nao"
)

$venvPath = Join-Path -Path (Resolve-Path ..) -ChildPath ".venv/$Name"
if (-Not (Test-Path $venvPath)) {
    python -m venv $venvPath
}

$activatePath = Join-Path $venvPath "Scripts/Activate.ps1"
& $activatePath
pip install --upgrade pip
pip install -r ../requirements.txt
python -m ipykernel install --user --name $Name --display-name "RL Labs (py311)"
Write-Host "Environment '$Name' ready. Activate with: `n. $activatePath"
