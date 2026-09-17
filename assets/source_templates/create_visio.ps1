$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$out = Join-Path $projectRoot 'paper\figures'
$spec = Get-Content -Raw -LiteralPath (Join-Path $out 'overview_shapes.json') | ConvertFrom-Json
function ColorFormula([string]$hex) {
    $h = $hex.TrimStart('#')
    return 'RGB({0},{1},{2})' -f [Convert]::ToInt32($h.Substring(0,2),16),[Convert]::ToInt32($h.Substring(2,2),16),[Convert]::ToInt32($h.Substring(4,2),16)
}
$app = $null
$doc = $null
try {
    $app = New-Object -ComObject Visio.Application
    Write-Output 'Visio instance created'
    $app.Visible = $false
    $app.AlertResponse = 7
    $app.ScreenUpdating = $false
    $doc = $app.Documents.Add('')
    Write-Output 'Document created'
    $page = $app.ActivePage
    $page.Name = 'FAR overview'
    $page.PageSheet.CellsU('PageWidth').ResultIU = $spec.width
    $page.PageSheet.CellsU('PageHeight').ResultIU = $spec.height
    foreach ($cell in 'PageLeftMargin','PageRightMargin','PageTopMargin','PageBottomMargin') { $page.PageSheet.CellsU($cell).ResultIU = 0 }
    $shapeCount = 0
    foreach ($item in $spec.shapes) {
        if ($item.kind -eq 'line') {
            $s = $page.DrawLine($item.x,$item.y,$item.x2,$item.y2)
            $s.CellsU('LineColor').FormulaU = ColorFormula $item.color
            $weight = if ($null -ne $item.weight) { $item.weight } else { 1.3 }
            $s.CellsU('LineWeight').FormulaU = "$weight pt"
            if ($item.arrow) { $s.CellsU('EndArrow').FormulaU = '4' }
            if ($item.dash) { $s.CellsU('LinePattern').FormulaU = '2' }
        } elseif ($item.kind -eq 'poly') {
            [double[]]$coords = @($item.points | ForEach-Object { $_[0]; $_[1] })
            $s = $page.DrawPolyline($coords,0)
            $s.CellsU('LinePattern').FormulaU = '0'
            $s.CellsU('FillForegnd').FormulaU = ColorFormula $item.fill
            if ($item.stroke) {
                $s.CellsU('LinePattern').FormulaU = '1'
                $s.CellsU('LineColor').FormulaU = ColorFormula $item.line
                $s.CellsU('LineWeight').FormulaU = '1.0 pt'
            }
            if ($null -ne $item.transparency) { $s.CellsU('FillForegndTrans').ResultIU = $item.transparency }
        } else {
            if ($item.kind -eq 'ellipse') {
                $s = $page.DrawOval($item.x,$item.y,$item.x+$item.w,$item.y+$item.h)
            } else {
                $s = $page.DrawRectangle($item.x,$item.y,$item.x+$item.w,$item.y+$item.h)
            }
            if ($item.kind -eq 'text') {
                $s.CellsU('LinePattern').FormulaU = '0'
                $s.CellsU('FillPattern').FormulaU = '0'
            } else {
                $s.CellsU('LineColor').FormulaU = ColorFormula $item.line
                $s.CellsU('FillForegnd').FormulaU = ColorFormula $item.fill
                $s.CellsU('LineWeight').FormulaU = '0.8 pt'
            }
            $s.Text = $item.text
            $s.CellsU('Char.Font').FormulaU = 'FONT("Times New Roman")'
            $s.CellsU('Char.Size').FormulaU = "$($item.size) pt"
            $s.CellsU('Char.Style').FormulaU = $(if ($item.bold) { '1' } else { '0' })
            $s.CellsU('Char.Color').FormulaU = ColorFormula $item.color
            $s.CellsU('Para.HorzAlign').FormulaU = [string]$item.align
            $s.CellsU('VerticalAlign').FormulaU = '1'
            foreach ($cell in 'LeftMargin','RightMargin','TopMargin','BottomMargin') { $s.CellsU($cell).ResultIU = 0.015 }
        }
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($s)
        $shapeCount++
        if ($shapeCount % 20 -eq 0) { Write-Output "Drawn $shapeCount shapes" }
    }
    $doc.SaveAs((Join-Path $out 'overview.vsdx'))
    Write-Output 'Saved editable document'
    $page.Export((Join-Path $out 'overview.svg'))
    $doc.ExportAsFixedFormat(1,(Join-Path $out 'overview.pdf'),1,0,1,1,$false,$true,$true,$true,$false)
    Write-Output "Native editable shapes: $($page.Shapes.Count)"
} finally {
    if ($doc) { $doc.Close() }
    if ($app) { $app.Quit() }
}
& python -X utf8 (Join-Path $PSScriptRoot 'export_overview_panels.py')
if ($LASTEXITCODE -ne 0) { throw 'Individual panel export failed' }
