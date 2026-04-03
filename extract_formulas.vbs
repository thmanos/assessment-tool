Sub ExportFormulasFromRange()
    Dim ws As Worksheet
    Dim formulaRange As Range
    Dim cell As Range
    Dim formulasText As String
    Dim filePath As String
    Dim fileNumber As Integer
    Dim sheetName As String
    Dim rangeAddress As String
    
    ' Prompt user for the sheet name
    sheetName = InputBox("Enter the name of the sheet to export formulas from:")
    
    ' Check if the sheet exists
    On Error Resume Next
    Set ws = ThisWorkbook.Sheets(sheetName)
    On Error GoTo 0
    
    If ws Is Nothing Then
        MsgBox "Sheet '" & sheetName & "' does not exist!", vbExclamation
        Exit Sub
    End If
    
    ' Prompt user for the range to export
    rangeAddress = InputBox("Enter the range to export (e.g., A1:B10):")
    
    ' Check if the specified range is valid
    On Error Resume Next
    Set formulaRange = ws.Range(rangeAddress)
    On Error GoTo 0
    
    If formulaRange Is Nothing Then
        MsgBox "Range '" & rangeAddress & "' is not valid!", vbExclamation
        Exit Sub
    End If

    ' Initialize the formulas text
    formulasText = ""

    ' Loop through each cell in the specified range and collect formulas
    For Each cell In formulaRange
        If cell.HasFormula Then
            ' Adjust column offset here; for example, 2 columns to the right
            additionalValue = cell.Offset(0, 2).Value
            excelField = cell.Offset(0, 3).Value
            formulasText = formulasText & cell.Address & ": " & cell.Formula & " | " & additionalValue & " | " & excelField & vbCrLf
        End If
    Next cell
    
    ' Check if any formulas were found
    If formulasText = "" Then
        MsgBox "No formulas found in the specified range.", vbInformation
        Exit Sub
    End If
    
    ' Prompt user for file path to save the text file
    filePath = Application.GetSaveAsFilename("Formulas.txt", "Text Files (*.txt), *.txt")
    
    ' Check if the user canceled the dialog
    If filePath = "False" Then Exit Sub
    
    ' Open the file for output
    fileNumber = FreeFile
    Open filePath For Output As #fileNumber
    
    ' Write the formulas to the file
    Print #fileNumber, formulasText
    
    ' Close the file
    Close #fileNumber
    
    ' Notify the user of completion
    MsgBox "Formulas exported successfully to " & filePath
End Sub



