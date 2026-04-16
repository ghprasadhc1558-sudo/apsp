# Organizational Structure JSON Format

## How to add officers structure to battalions

### Format Example (as used in 2nd Battalion):

```json
{
  "additional_commandant": {
    "name": "V.Nagendra Rao",
    "groups": []
  },
  "assistant_commandants": [
    {
      "name": "D.Venkataramana",
      "companies": [
        {"company": "C Company", "incharge": "L.Srinivasa Reddy, RI"}
      ]
    },
    {
      "name": "P. Ravi Kiran",
      "companies": [
        {"company": "K Company", "incharge": "L.Srinivasa Reddy, RI"}
      ]
    },
    {
      "name": "V.Keshava Reddy",
      "companies": [
        {"company": "E Company", "incharge": "T.Rama Rao, RI"},
        {"company": "F Company", "incharge": "G.V.Saini Reddy, RI"},
        {"company": "D/SDRF Company", "incharge": "S.Praveen Kumar, RI"}
      ]
    }
  ],
  "groups": [
    {"head": "Quarter Master Office", "group": "Quarter Master Office", "incharge": "M.C.Shaikshavali, RI"},
    {"head": "", "group": "Head Quarters Office", "incharge": "K.Siva Sankar Rao, RI"},
    {"head": "", "group": "Motor Transport Office", "incharge": "P.Samba Siva Rao, RI"},
    {"head": "ADDITIONAL COMMANDANT", "group": "Band", "incharge": "J.Obulesi., RSI"}
  ]
}
```

### Structure Explanation:

1. **additional_commandant**: (Optional)
   - `name`: Name of Additional Commandant
   - `groups`: Array of groups they manage (can be empty)

2. **assistant_commandants**: Array of assistant commandants
   - Each has:
     - `name`: Officer name
     - `companies`: Array of companies they manage
       - `company`: Company name (e.g., "C Company", "K Company")
       - `incharge`: Company incharge name with rank

3. **groups**: Array of organizational groups
   - `head`: Group head label (can be empty string if same as above)
   - `group`: Group name (Quarter Master Office, Band, Training, etc.)
   - `incharge`: Officer in charge with rank

### How to Add in Admin Dashboard:

1. Login to admin dashboard
2. Go to "Battalions" section
3. Select battalion from dropdown
4. Scroll to "Organizational Structure (JSON Format)" textarea
5. Paste the JSON structure (copy from 2nd Battalion as template)
6. Modify names and details as needed
7. Click "Save Battalion Info"

### Tips:

- Keep JSON format valid (use quotes, commas correctly)
- Leave `head` field empty ("") if same row continues from above
- Add all companies under each assistant commandant
- Groups section shows headquarters offices, band, training, etc.

### View on Website:

Visit: `http://127.0.0.1:5000/battalion/2` to see the formatted organizational structure display.
