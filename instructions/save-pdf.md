SAVE PDF (version 1)
Written for: sheets-spec version 4

The one way to put a PDF that a tools/ script made into a Google Drive folder. daily-delivery-list and weekly-master-list both use it. Do it exactly this way every time; never improvise another way.

Why this way: Google Drive converts an uploaded PDF into a Google Doc unless conversion is turned off. That is what left empty "Master list" Docs in Drive on Oct 17 and 18. With conversion off, the file stays a real PDF, as Friday's delivery list did on Oct 15.

THE CALL
Google Drive create_file (mcp__Google-Drive__create_file), with exactly these parameters:
- title: the script's "file_name"
- parentId: the target folder's ID (find the folder by name inside the Ops folder, as the calling doc says)
- contentMimeType: "application/pdf"
- disableConversionToGoogleType: true
- base64Content: the whole contents of the script's "base64_file" (one line of base64). Read it with `cat [base64_file]` and pass it exactly, every character, however long (10,000 to 40,000 characters is normal). Never shorten, retype, rewrap or summarize it, and never decide it is too long.
Never use textContent, the deprecated "content" or "mimeType" parameters, or a Google type (application/vnd.google-apps...). Never make a second file if one call fails: check first (below).

CHECK
- The reply must show the new file's ID and a MIME type of application/pdf. If it shows a Google Doc type, or no file was made: record an ALERT Problem "PDF save failed: [what the reply said]", leave anything that was made (never delete), and use the calling doc's fallback.
- If the reply (or a Drive search for the file) shows its size, it must equal the script's "bytes". A different size means the copy was damaged: ALERT Problem "PDF damaged in upload: [size] vs [bytes]", leave it, and use the fallback.
- Link = https://drive.google.com/file/d/[file ID]/view

SHARING
The Drive tool can only share by email, so link sharing comes from the folder: Shane sets the Delivery Lists and Master Lists folders to "anyone with the link can view". Don't try to change sharing.
