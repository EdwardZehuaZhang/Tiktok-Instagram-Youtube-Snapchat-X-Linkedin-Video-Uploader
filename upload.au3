; Wait for the Open dialog to become active
WinWaitActive("Open")

; Focus the edit control where the file path is to be entered
ControlFocus("Open", "", "Edit1")

; Set the file path in the edit control
ControlSetText("Open", "", "Edit1", "D:\\Your Path\\Your Path\\Your Path.mp4")

; Click the Open button to confirm the selection
ControlClick("Open", "", "Button1")
