$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot
try {
	npm install
	npm --prefix .\backend install
	npm --prefix .\frontend install
	npm run dev
}
finally {
	Pop-Location
}
