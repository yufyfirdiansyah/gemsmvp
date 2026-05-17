/**
 * TAPG Trading Terminal API
 * Deploy as Web App (Execute as: Me, Access: Anyone)
 */
function doGet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Data");

  if (!sheet) {
    return ContentService.createTextOutput(JSON.stringify({ error: "Sheet named 'Data' not found" }))
      .setMimeType(ContentService.MimeType.JSON);
  }

  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  const data = sheet.getRange(2, 1, 1, sheet.getLastColumn()).getValues()[0];

  const result = {};
  for (let i = 0; i < headers.length; i++) {
    result[headers[i]] = data[i] === "" ? 0 : data[i];
  }

  return ContentService.createTextOutput(JSON.stringify(result))
    .setMimeType(ContentService.MimeType.JSON);
}
