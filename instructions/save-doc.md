SAVE LIST DOC (version 2)
Written for: sheets-spec version 4

The one way to make a list Google Doc: invoice lists (invoicing), read-back lists (confirm-orders) and the delivery list's fallback Doc (daily-delivery-list). Do it exactly this way every time; never improvise another way. PDFs are different: they use save-pdf.md.

Why this way: on Oct 23 a run couldn't make Thursday's invoice list Doc because it thought the Drive tool needed base64 (that's only for PDFs). With no Doc, nothing after it happened, and Thursday's invoices stalled. Plain text with conversion left on made the same Doc correctly later that day.

THE CALL
Google Drive create_file (mcp__Google-Drive__create_file), with exactly these parameters:
- title: the doc name the calling doc gives
- parentId: the target folder's ID (find the folder by name inside the Ops folder, as the calling doc says)
- contentMimeType: "text/plain" (or "text/html" only when the calling doc gives you an HTML file, as daily-delivery-list's fallback does)
- textContent: the list text (or the HTML file's contents), exactly, every line
Leave out disableConversionToGoogleType: conversion stays on, so Drive makes it a Google Doc. Never use base64Content, the deprecated "content" or "mimeType" parameters, or any other tool for a list Doc. Never make a second file if one call fails: check first (below).

CHECK
- The reply must show the new file's ID.
- A quota error (the reply says "Resource has been exhausted", "quota", "rate limit" or 429, as a read-back list's did on Oct 30) often passes a moment later. Search the target folder for a file with exactly this title made in the last 10 minutes (an older one with the same title is a different list). If one is there, the call worked after all: use that file's ID. If not, make the same call once more, unchanged. If the search itself fails, don't make the call again.
- Any other error, a reply with no file ID that isn't a first quota error, a second quota error, or a quota error whose search failed: record an ALERT Problem "List doc not made: [doc name]: [what the reply said]". Don't try another way. Go on with the calling doc's fallback: the work never stops because a Doc failed.
- Link = https://docs.google.com/document/d/[file ID]/edit

A DOC CAN'T BE CHANGED
The Drive tool can't edit a Doc's text once it's made. If the calling doc says to rebuild a Doc, or a Doc with the same name is already in that folder, make a new one named "[doc name] (2)" (then "(3)", and so on) and use the new one's link. Never delete, rename or edit the old one.
