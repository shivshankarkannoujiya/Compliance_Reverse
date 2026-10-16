# Figure manifest for the Incidents recording (meeting 20260811_135933).
# id, timestamp, workbook, tab, caption, crop[, redaction]  (crop: 'xl' = Excel window, 'top' = formula bar + header rows, 'full', 'explorer')
WB = "Incident Management.xlsm"
FIGS = [
("rec",  "00:00:20", "Teams recording", "(camera)", "Recording starts on camera; operator explains this video covers the compliance update for incidents", "full"),
("exp",  "00:00:58", "File Explorer", "Performance Dashboards and Data › User input", "The User input folder: 12 sibling input tools (Audit, Contract, Estates, Hand Hygiene/IPC Audits, Incident, Medical Devices, Policy & Procedure, RTT Data, Sickness/Leave/Vacancy, Survey, Staff Management) plus the lock file ~$Incident Management (13:56), showing the workbook is already open", "explorer"),
("req",  "00:01:31", WB, "Requirements", "requirements_Table A:G: one name (Provide Wellbeing) × 10 incident compliance types, all Required TRUE, Core, Active TRUE; tab bar Manage Compliance · Requirements · Compliance Timeframes · Estates · Health and Safety · Safeguarding …", "xl"),
("reqF", "00:02:31", WB, "Requirements", "Formula bar, F3 Unique Lookup: =CONCAT([@Name],\"-\",[@[Compliance Type]])", "top"),
("reqG", "00:02:47", WB, "Requirements", "G5 Active holds a typed constant TRUE (not a lookup to a Names table, which this workbook does not have)", "top"),
("ct1",  "00:03:12", WB, "Compliance Timeframes", "Compliance_Timeframe_Table A:I: Every x months = 0.5 for all 10 types, Core, Group 1 Operational, Group 2 Incidents, Unique Lookup “Operational-Incidents-”, Missing TRUE for every row", "xl"),
("ctB",  "00:03:20", WB, "Compliance Timeframes", "Formula bar, B2 Every x months = 0.5 (“Matt set it for twice a month; we only look at this every month”)", "top"),
("ctH",  "00:03:48", WB, "Compliance Timeframes", "Formula bar, H4 Unique Lookup: =CONCAT([@[Compliance Group 1]],\"-\",[@[Compliance Group 2]],\"-\",[@[Compliance Group 3]]): trailing dash because Group 3 is blank", "top"),
("ctI",  "00:03:52", WB, "Compliance Timeframes", "Formula bar, I2 Missing: =XLOOKUP(CONCAT(add_Requirements_Name,\"-\",[@[Compliance Type]]),[Unique Lookup],[Unique Lookup],\"\")=\"\": looks in its own table’s Unique Lookup, so it is TRUE for every row", "top"),
("ctT",  "00:04:04", WB, "Compliance Timeframes", "Thresholds J:N selected: Threshold 1–4 = 1, Threshold 5 = 0.99 (“100% shows green, anything less shows red”)", "xl"),
("tabs", "00:04:36", WB, "(tab bar)", "Tab bar scrolled: … Health and Safety · Safeguarding · IG · Clinical · SPC · Miscellaneous · Groupings Pivot · Harm Pivot · Datix … (none of these opened)", "xl"),
("dxN",  "00:04:45", WB, "Datix", "On first opening, the Datix sheet is scrolled to a later row: ID 13073, incident 07/04/2026, reported 08/06/2026, so the table holds incidents from 2023 to 2026. Name and Description are blurred in this report (patient and staff information)", "xl", "redact_narrow"),
("dx1",  "00:04:47", WB, "Datix", "Datix table A:J: ID, Name (blank), Incident date, Reported, Category, Sub category, Description (free text), Severity, Other service – Division, Other Service – Service. Ribbon shows a Query tab: this table is a Power Query output. Name and Description blurred in this report", "xl", "redact_wide"),
("dx2",  "00:04:53", WB, "Datix", "Datix table N:T: Organisation Type, Q&S Incident Review Panel (Y/N, date), Approval status (green = “Incident Approved & Record Closed”), and the calculated columns Grouping, In last 7 months, In set timeframe", "xl"),
("dx3",  "00:05:30", WB, "Datix", "While the operator describes going into Datix, opening the dashboard and exporting, the shared screen does not change: the Datix browser window was dragged off the shared screen (05:14). Name and Description blurred in this report", "xl", "redact_wide"),
("dxR",  "00:06:24", WB, "Datix", "Formula bar, R2 Grouping: =XLOOKUP([@Category],datix_Category_Table[Datix reference],datix_Category_Table[Category],\"\"); row 2 results: Grouping = Information Governance, In last 7 months = FALSE, In set timeframe = #REF!", "xl"),
("refz", "00:06:24", WB, "Datix", "Close-up of row 2: Grouping = Information Governance (correct), In last 7 months = FALSE, In set timeframe = #REF!", "refzoom"),
("cat1", "00:06:37", WB, "Datix Category", "datix_Category_Table rows 2–24: Datix reference (category) → dashboard Category (Information Governance, Health and Safety, Clinical, Estates, Safeguarding)", "xl"),
("cat2", "00:06:44", WB, "Datix Category", "Rows 10–26 (25 mappings in total); tab bar shows All Notes · Clinical Notes · Information Governance Notes · Health and Safety Notes · Estates Notes · Sa…", "xl"),
("dxT",  "00:06:53", WB, "Datix", "Formula bar, T2 In set timeframe: =IF([@Reported]<>\"\",OR((TODAY()-[@Reported])<=SWITCH([@Description],\"No Harm\",42,\"Low Harm\",42,\"Moderate Harm\",42,\"Severe Harm\",90,\"Fatal\",365,IF(#REF!=\"Yes\",90,42)),[@[Approval status]]<>\"Incident Approved & Record Closed\"),\"\"): result #REF!", "xl"),
("end",  "00:07:12", WB, "Datix", "Last frame: recording paused by the operator before the #REF! is fixed and before any refresh or publish step", "xl"),
]
