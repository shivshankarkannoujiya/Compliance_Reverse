# Figure manifest for the Complications recording (meeting 20260814_120551).
# id, timestamp, workbook, tab, caption, crop[, redaction]
WB = "Complications Report.xlsm"
CD = "Compliance Data.xlsm"
FIGS = [
("rec",  "00:00:10", "Teams recording", "(camera off)", "Recording starts with camera off: “this will be the last video… complications compliance”", "full"),
("cd0",  "00:00:37", WB, "Complications Details", "First shared screen: the complications log (Complications Details) at its last rows 527–528 (event 17/07/2026). NHS number and clinical Notes blurred in this report", "xl", "cd_left"),
("vbe",  "00:01:47", WB, "VBA editor", "Operator opens the VBA editor to look for macros: 18 sheet objects (Sheet1…Sheet18) and ThisWorkbook; the module shown is empty (“Oh no, it probably isn’t actually”)", "xl"),
("pq",   "00:02:12", WB, "Power Query editor", "Power Query editor: one query, All_Appts, the appointments extract that refreshes when the workbook opens", "xl"),
("apS",  "00:02:21", WB, "All_Appts Data Auto Load", "Formula bar, S6412 Notes: =IF([@Infection]>0,XLOOKUP(CONCAT([@[NHS number]],\"-\",TEXT([@[Appointment Date]],\"dd/mm/yyyy\")),Table5[Lookup 1],Table5[Notes],\"\"),\"\"). Appt Ref and Patient ID blurred", "xl", "ap"),
("apN",  "00:02:28", WB, "All_Appts Data Auto Load", "Formula bar, N2 Patient ID: =LEFT([@[Appt Ref 1]],SEARCH(\"-\",[@[Appt Ref 1]])-1)", "fb"),
("apO",  "00:02:34", WB, "All_Appts Data Auto Load", "Formula bar, O2 Next Appt Date: =IF([@[NHS number]]<>\"\",XLOOKUP([@[NHS number]],A3:A$30221,B3:B$30221,0),0): a hard-coded range that stops at row 30221", "fb"),
("apP",  "00:02:42", WB, "All_Appts Data Auto Load", "Formula bar, P2 Infection: five nested IFERROR(INDEX(All_Complications[Read code],MATCH(1,(NHS number match)*(Appointment Date <= Event date)*(Event date < Next Appt Date or 1000000),0)) tests, one per infection Read code, e.g. (Xa6nk) Postoperative wound infection. Appt Ref and Patient ID blurred", "xl", "ap"),
("apR",  "00:02:51", WB, "All_Appts Data Auto Load", "Formula bar, R2 VAS Failure: same INDEX/MATCH array pattern with Read code (61G1.) Vasectomy failure; Q2 Pain uses (SP2y2) Postoperative pain", "fb"),
("sys1", "00:03:27", WB, "Complications_from Sys1", "SystmOne export of complication Read codes: NHS number, Read code, Event date, Service offered, Event done by (rows 980–1003, Jan–Jun 2026). NHS numbers blurred", "xl", "sys1"),
("cd1",  "00:03:57", WB, "Complications Details", "The complications log scrolled right: Location, Clinician, Nurse, Antibiotics prescribed, Diagnosed By, Notes, Intra-operative/Post operative, Include in Statistics, Lookup 1 = CONCAT([@[NHS number]],\"-\",TEXT([@[Op Date]],\"dd/mm/yyyy\")); empty rows show “-00/01/1900”. Notes and Lookup 1 blurred", "xl", "cd_right"),
("pv1",  "00:04:12", WB, "Ops Site Clinician Pivot", "Pivot of Activity and Infections by site → clinician → year/month (2023–2026)", "xl"),
("pv2",  "00:04:46", WB, "All VAS Ops Pivot", "All VAS Ops Pivot: count of operations per clinician per month (one of four pivots refreshed after loading: All Ops, All VAS Ops, Infections, Pain)", "xl"),
("inf",  "00:05:14", WB, "Infection Rate", "Infection Rate grid: =IFERROR(IFERROR(GETPIVOTDATA(\"Infection\",'Infections Pivot'!$A$3,…,\"Clinician\",$A14,…),0)/IFERROR(GETPIVOTDATA(\"Service Level 2\",'All Ops Pivot'!$A$3,…),0),\"N/A\"): monthly rate per clinician; pink cells above threshold", "xl"),
("vfr",  "00:05:23", WB, "Vas Failure Rate", "Vas Failure Rate by clinician and year (2023–2026), Overall, Overall (minus Dr Saad), Running Rate 0.35% / 0.23%", "xl"),
("cr1",  "00:05:32", WB, "Compliance Report", "Compliance Report: monthly counts July–June (VAS Failures, Haematoma, Pain, Infection, Bleeding, Swelling, Granuloma), VAS Ops for Failures and Overall Ops, and monthly rates (=B22/B29); note “Use 12 months previous (i.e. failures take 12 months to wash through)”", "xl"),
("cr2",  "00:06:14", WB, "Compliance Report", "Standards (3/6/12-month average and 12-month spike limits per type) and the result block “at 09/04/26”: B13 = MAX(B31:M31) as the 12-month spike, Compliant/Non-compliant by comparison; monthly status columns Mar-25…Jun-26", "xl"),
("clin", "00:06:42", WB, "Clinician Overview", "Clinician Overview: a clinician picker (A2, e.g. Dr Alan Speers) drives Vas failure rates by year vs all clinicians, and monthly ops, infection and post-op pain reports and rates (monthly, rolling, excluding the current clinician); pink = above benchmark", "xl"),
("bench","00:06:43", WB, "Benchmarks", "Benchmarks tab: Herts — Failure rate less than 1 in 2000 (0.05%), Haematoma less than 1%, Chronic pain 3%, Infection less than 1%; SNEE — Infection less than 5%, Failure less than 1%; CTS NEE — Infection less than 5%. These differ from the limits used on Compliance Report", "xl"),
("vfp",  "00:06:45", WB, "Vas Failure Pivot", "Vas Failure Pivot: sum of VAS Failure by clinician and year", "xl"),
("cdt",  "00:06:54", WB, "Compliance Data Transfer", "Compliance Data Transfer: 8 rows (Bleeding, Haematoma, Infection, Pain, Sperm Granuloma, Swelling, Vas Failure, Dehiscence) for Provide Wellbeing, all Completed, Issue 10, “Within benchmark”, due 11/09/2026, Clinical › Complications, Weighting 1; operator selects rows to copy", "xl"),
("req",  "00:07:01", CD, "requirements_Final", "Compliance Data.xlsm opens with “UNABLE TO REFRESH – We couldn’t get updated values from a linked workbook”. requirements_Final table: Name, Compliance Type, Required, Core, Managed By, Unique Lookup across all areas", "xl"),
("cdd",  "00:07:07", CD, "Compliance Data", "The Compliance Data tab (the data store), last row 4268. The operator points to where the transfer rows are pasted; the paste itself is not performed on screen", "xl"),
("lu",   "00:07:12", CD, "Last Updated", "Last Updated table: Compliance Group Level 1/2, Updated, Unique Lookup; Clinical–Complications row 24 shows 27/07/2026", "xl"),
("ctt",  "00:07:22", CD, "compliance_Timeframes_Table", "compliance_Timeframes_Table (consolidated from all tools) filtered on Compliance Group 2; RTT Compliance rows with 0.25 months", "xl"),
("ctt2", "00:07:37", CD, "compliance_Timeframes_Table", "Unfiltered: Estates rows first (Pat Test 24, Fire Extinguishers 12 …), then staff types (PI Insurance …)", "xl"),
("end",  "00:07:47", CD, "(tab bar)", "Tab bar further right: staff_requirements_Table, estates_requirements_Table, estates_Compliance_Timeframe_Table (per-tool query outputs). Recording ends at 07:58", "xl"),
]
