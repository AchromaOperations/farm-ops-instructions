SAVE PDF (version 4)
Written for: sheets-spec version 4

The one way to put a PDF that a tools/ script made into a Google Drive folder. daily-delivery-list and weekly-master-list both use it. Do it exactly this way every time; never improvise another way. This file is only for PDFs: list Google Docs (invoice and read-back lists, the delivery list's fallback Doc) are made with textContent as save-doc.md says, never with base64.

Why this way: Google Drive converts an uploaded PDF into a Google Doc unless conversion is turned off. That is what left empty "Master list" Docs in Drive on Oct 17 and 18. With conversion off, the file stays a real PDF, as Friday's delivery list did on Oct 15.

THE CALL
Google Drive create_file (mcp__Google-Drive__create_file), with exactly these parameters:
- title: the script's "file_name"
- parentId: the target folder's ID (find the folder by name inside the Ops folder, as the calling doc says)
- contentMimeType: "application/pdf"
- disableConversionToGoogleType: true
- base64Content: the whole contents of the script's "base64_file" (one line of base64). Read it with `cat [base64_file]` and pass it exactly, every character, however long (10,000 to 40,000 characters is normal). Never shorten, retype, rewrap or summarize it, and never decide it is too long.
For a PDF, never use textContent, the deprecated "content" or "mimeType" parameters, or a Google type (application/vnd.google-apps...). At most two tries in all: check each one first (below).

CHECK
- The reply must show the new file's ID and a MIME type of application/pdf.
- If the reply (or a Drive search for the file) shows its size, it must equal the script's "bytes". A different size means the copy was damaged.
- One more try if the first one failed: the call errored (for example Drive said the base64 isn't valid, as on Nov 1), no file was made, it's a Google Doc type, or the size is wrong. These mostly come from one wrong character in the long copy, so a fresh copy often works. If the script's JSON has "no_links" (the delivery list without its map and phone links, shorter to copy), the second try uploads that one: its "base64_file", and its "bytes" for the size check. Otherwise it's the same base64_file again. Run `cat` on that base64_file fresh and make the call again exactly as THE CALL says, passing it exactly. If the first try made a file, leave it (never delete) and title the new one "[file_name without .pdf] (2).pdf". Check it the same way. If it passes, add "PDF saved on the second try" (and "without links" if it was the no_links copy) to Steps run; that's a note, not an ALERT.
- If the second try fails too: record an ALERT Problem "PDF save failed twice: [what each reply said]" (for a wrong size, "[size] vs [bytes]"), leave anything that was made, and use the calling doc's fallback.
- Link = https://drive.google.com/file/d/[file ID]/view (the try that passed).

SHARING
The Drive tool can only share by email, so link sharing comes from the folder: Shane sets the Delivery Lists and Master Lists folders to "anyone with the link can view". Don't try to change sharing.
