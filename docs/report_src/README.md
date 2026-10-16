# Report sources

One generator builds the reports for every recording. `REPORT_PROFILE` picks the recording:

| Profile | Recording | Output folder |
|---|---|---|
| `staff` (default) | `first/…131142…mp4` (Staff Management) | `01_Staff_Management/` |
| `incidents` | `second/…135933…mp4` (Incident Management / Datix) | `02_Incident_Management/` |
| `complications` | `third/…120551…mp4` (Complications) | `03_Complications/` |
| `training` | `fourth/…113314…mp4` (Mandatory Training) | `04_Mandatory_Training/` |
| `feedback` | `fifth/…111322…mp4` (Survey Feedback) | `05_Survey_Feedback/` |

- `figures.py`, `figures_incidents.py`: figure manifests (id, video timestamp, workbook, tab, caption, crop, optional redaction).
- `extract.py`: pulls each frame from the `.mp4` with ffmpeg at the exact timestamp, crops it and blurs redacted cells (needs `git lfs pull` first).
- `content.py`, `content_incidents.py`: specification text and tables (sections 0–7, appendices).
- `build.py`: ReportLab layout (title block, TOC, captions, tables).
- `build_prereq.py` + `prereq_staff.py` / `prereq_incidents.py`: the pre-build client requirements PDF (files, sheets, VBA, rules and decisions, with reasons and a sign-off checklist).
- `figures/`, `figures_incidents/`: the extracted, verified screenshots as embedded in the PDFs.
- `asr_*.txt`: timestamped re-transcriptions of the audio (offline Whisper).
  The `.srt` in `first/` belongs to the Incidents meeting (135933), so it was not used for timing there; it matches `second/`.

Datix screenshots have the Name and Description cells blurred, because they hold patient narratives and personal names.
Complications screenshots have NHS numbers, patient names (Appt Ref, Patient ID), clinical notes and NHS-number lookup keys blurred.
Training screenshots have staff email addresses blurred.
Feedback screenshots have free-text patient comments blurred.

Rebuild (from this folder):

```
pip install reportlab pillow pymupdf
python3 extract.py && python3 build.py spec.pdf && python3 build_prereq.py prereq.pdf
REPORT_PROFILE=incidents python3 extract.py
REPORT_PROFILE=incidents python3 build.py spec.pdf && REPORT_PROFILE=incidents python3 build_prereq.py prereq.pdf
```
(`build.py` reads the `figs/` or `figs_incidents/` folder that `extract.py` creates next to it.)
