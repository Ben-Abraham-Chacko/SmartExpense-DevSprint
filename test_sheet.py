import gspread

# Connect to the "Robot Butler" credentials
gc = gspread.service_account(filename='creds.json')

# Open the sheet you shared with it
sh = gc.open("My Expenses")

# Select the first tab (Sheet1)
worksheet = sh.get_worksheet(0)

# Write to a cell
worksheet.update_acell('A1', 'Jeeves is online and ready for the hackathon!')

print("Master, check your Google Sheet! If you see the message in cell A1, we have succeeded.")
