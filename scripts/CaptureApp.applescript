-- CaptureApp — RileyContext Quick Capture
-- Dock-ready app with tag support, autosave, and duplicate detection
-- Saves to: CONTEXT_HUB/captures/inbox/CaptureApp/

use AppleScript version "2.4"
use scripting additions
use framework "Foundation"
use framework "AppKit"

property mainWindow : missing value
property tagField : missing value
property textView : missing value
property statusLabel : missing value
property wordCountLabel : missing value
property captureBtn : missing value
property autosaveTimer : missing value
property captureBasePath : missing value
property lastSavedHash : ""
property currentSavePath : ""

on run
	set captureBasePath to (POSIX path of (path to home folder)) & "dev/RileyContext/CONTEXT_HUB/captures/inbox/CaptureApp/"
	do shell script "mkdir -p " & quoted form of captureBasePath
	my createWindow()
	set autosaveTimer to current application's NSTimer's scheduledTimerWithTimeInterval:3 target:me selector:"autosave:" userInfo:(missing value) repeats:true
end run

on makeLabel(labelText, x, y, w, h)
	set ca to current application
	set tf to ca's NSTextField's alloc()'s initWithFrame:(ca's NSMakeRect(x, y, w, h))
	tf's setStringValue:labelText
	tf's setBordered:false
	tf's setEditable:false
	tf's setDrawsBackground:false
	tf's setSelectable:false
	tf's setFont:(ca's NSFont's systemFontOfSize:11)
	tf's setTextColor:(ca's NSColor's secondaryLabelColor())
	return tf
end makeLabel

on createWindow()
	set ca to current application

	-- Window style mask: titled + closable + resizable + miniaturizable
	set winMask to 15
	set mainWindow to ca's NSWindow's alloc()'s initWithContentRect:(ca's NSMakeRect(0, 0, 520, 500)) styleMask:winMask backing:2 defer:false
	mainWindow's setTitle:"CaptureApp"
	mainWindow's setMinSize:{420, 400}
	mainWindow's setReleasedWhenClosed:false

	set cv to mainWindow's contentView()
	set w to 520
	set h to 500

	-- Tag label
	set tagLabel to my makeLabel("Tags (optional — #cfa #idea #todo)", 16, h - 30, w - 32, 18)
	cv's addSubview:tagLabel

	-- Tag input field
	set tagField to ca's NSTextField's alloc()'s initWithFrame:(ca's NSMakeRect(16, h - 60, w - 32, 26))
	tagField's setPlaceholderString:"#tag1 #tag2"
	tagField's setFont:(ca's NSFont's systemFontOfSize:13)
	tagField's setBordered:true
	tagField's setBezeled:true
	cv's addSubview:tagField

	-- Content label
	set contentLabel to my makeLabel("Capture content (text, URLs, HTML, notes)", 16, h - 85, w - 32, 18)
	cv's addSubview:contentLabel

	-- Scroll view + text view for content
	set scrollView to ca's NSScrollView's alloc()'s initWithFrame:(ca's NSMakeRect(16, 70, w - 32, h - 100))
	scrollView's setHasVerticalScroller:true
	scrollView's setBorderType:3
	-- autoresize: width + height sizable
	scrollView's setAutoresizingMask:18

	set textView to ca's NSTextView's alloc()'s initWithFrame:(ca's NSMakeRect(0, 0, w - 36, h - 104))
	textView's setMinSize:{100, 50}
	textView's setMaxSize:{100000, 100000}
	textView's setVerticallyResizable:true
	textView's setHorizontallyResizable:false
	textView's textContainer()'s setWidthTracksTextView:true
	textView's setRichText:false
	textView's setAllowsUndo:true
	textView's setFont:(ca's NSFont's userFixedPitchFontOfSize:13)
	textView's setAutomaticQuoteSubstitutionEnabled:false
	textView's setAutomaticDashSubstitutionEnabled:false

	scrollView's setDocumentView:textView
	cv's addSubview:scrollView

	-- Status label (bottom left)
	set statusLabel to my makeLabel("", 16, 40, 250, 16)
	statusLabel's setFont:(ca's NSFont's systemFontOfSize:10)
	statusLabel's setTextColor:(ca's NSColor's tertiaryLabelColor())
	cv's addSubview:statusLabel

	-- Word count label
	set wordCountLabel to my makeLabel("", 16, 22, 250, 16)
	wordCountLabel's setFont:(ca's NSFont's systemFontOfSize:10)
	wordCountLabel's setTextColor:(ca's NSColor's tertiaryLabelColor())
	cv's addSubview:wordCountLabel

	-- Paste Clipboard button
	set pasteBtn to ca's NSButton's alloc()'s initWithFrame:(ca's NSMakeRect(w - 300, 16, 110, 32))
	pasteBtn's setTitle:"Paste Clipboard"
	pasteBtn's setBezelStyle:1
	pasteBtn's setTarget:me
	pasteBtn's setAction:"pasteClipboard:"
	-- autoresize: min X margin
	pasteBtn's setAutoresizingMask:4
	cv's addSubview:pasteBtn

	-- Cancel button
	set cancelBtn to ca's NSButton's alloc()'s initWithFrame:(ca's NSMakeRect(w - 180, 16, 75, 32))
	cancelBtn's setTitle:"Cancel"
	cancelBtn's setBezelStyle:1
	cancelBtn's setTarget:me
	cancelBtn's setAction:"cancelCapture:"
	cancelBtn's setAutoresizingMask:4
	cv's addSubview:cancelBtn

	-- Capture button (Return key shortcut)
	set captureBtn to ca's NSButton's alloc()'s initWithFrame:(ca's NSMakeRect(w - 100, 16, 85, 32))
	captureBtn's setTitle:"Capture"
	captureBtn's setBezelStyle:1
	captureBtn's setTarget:me
	captureBtn's setAction:"doCapture:"
	captureBtn's setKeyEquivalent:(character id 13)
	captureBtn's setAutoresizingMask:4
	cv's addSubview:captureBtn

	mainWindow's |center|()
	mainWindow's makeKeyAndOrderFront:me
	ca's NSApp's activateIgnoringOtherApps:true
end createWindow

on pasteClipboard:(sender)
	try
		set clipText to the clipboard as text
		if clipText is not "" then
			set existingText to (textView's |string|()) as text
			if existingText is "" then
				textView's setString:clipText
			else
				textView's setString:(existingText & linefeed & clipText)
			end if
			my updateStatus("Pasted from clipboard")
		end if
	on error
		my updateStatus("No text on clipboard")
	end try
end pasteClipboard:

on autosave:(sender)
	set theContent to (textView's |string|()) as text
	if theContent is "" then
		my updateWordCount("")
		return
	end if

	my updateWordCount(theContent)

	set theTags to (tagField's stringValue()) as text
	set saveText to my buildSaveText(theContent, theTags)

	set currentHash to do shell script "printf %s " & quoted form of saveText & " | md5"
	if currentHash is lastSavedHash then return

	my saveToFile(saveText)
	set lastSavedHash to currentHash
	my updateStatus("Autosaved")
end autosave:

on doCapture:(sender)
	set theContent to (textView's |string|()) as text
	if theContent is "" then
		my updateStatus("Nothing to capture")
		return
	end if

	set theTags to (tagField's stringValue()) as text
	set saveText to my buildSaveText(theContent, theTags)

	my saveToFile(saveText)

	display notification "Captured!" with title "CaptureApp"
	my updateStatus("Captured! Ready for next.")

	textView's setString:""
	tagField's setStringValue:""
	set lastSavedHash to ""
	set currentSavePath to ""
end doCapture:

on cancelCapture:(sender)
	if autosaveTimer is not missing value then
		autosaveTimer's invalidate()
		set autosaveTimer to missing value
	end if
	current application's NSApp's terminate:me
end cancelCapture:

on buildSaveText(theContent, theTags)
	set theDate to do shell script "date '+%Y-%m-%d %H:%M:%S'"
	set header to "---" & linefeed & "captured: " & theDate & linefeed & "source: CaptureApp" & linefeed
	if theTags is not "" then
		set header to header & "tags: " & theTags & linefeed
	end if
	set header to header & "---" & linefeed & linefeed
	return header & theContent
end buildSaveText

on saveToFile(saveText)
	if currentSavePath is not "" then
		do shell script "printf %s " & quoted form of saveText & " > " & quoted form of currentSavePath
		return
	end if

	-- Check for duplicate content (strip header/timestamp, compare body only)
	-- Extract everything after the closing "---" marker
	set bodyText to saveText
	try
		set bodyText to do shell script "printf %s " & quoted form of saveText & " | sed -n '/^---$/,/^---$/d;p'"
	end try
	set newHash to do shell script "printf %s " & quoted form of bodyText & " | md5"
	try
		set existingFiles to do shell script "ls " & quoted form of captureBasePath & " 2>/dev/null"
		if existingFiles is not "" then
			repeat with f in paragraphs of existingFiles
				if f ends with ".txt" then
					set fPath to captureBasePath & f
					try
						set existingBody to do shell script "sed -n '/^---$/,/^---$/d;p' " & quoted form of fPath
						set existingHash to do shell script "printf %s " & quoted form of existingBody & " | md5"
						if existingHash is newHash then
							set currentSavePath to fPath
							return
						end if
					end try
				end if
			end repeat
		end if
	end try

	-- Generate unique filename
	set theDate to do shell script "date '+%Y-%m-%d-%H%M%S'"
	set fileName to "capture-" & theDate & ".txt"
	set currentSavePath to captureBasePath & fileName

	set counter to 1
	repeat while (do shell script "test -f " & quoted form of currentSavePath & " && echo yes || echo no") is "yes"
		set fileName to "capture-" & theDate & "-" & counter & ".txt"
		set currentSavePath to captureBasePath & fileName
		set counter to counter + 1
	end repeat

	do shell script "printf %s " & quoted form of saveText & " > " & quoted form of currentSavePath
end saveToFile

on updateStatus(msg)
	statusLabel's setStringValue:msg
end updateStatus

on updateWordCount(theContent)
	if theContent is "" then
		wordCountLabel's setStringValue:""
		return
	end if
	set wc to count of words of theContent
	set cc to count of characters of theContent
	wordCountLabel's setStringValue:((wc as text) & " words, " & (cc as text) & " chars")
end updateWordCount

on quit
	if autosaveTimer is not missing value then
		autosaveTimer's invalidate()
		set autosaveTimer to missing value
	end if
	continue quit
end quit
