# Report sources

Generator for `../../01_Staff_Management/Staff_Management_Compliance_Workflow_Specification.pdf`.

- `figures.py` – figure manifest: id, video timestamp, workbook, tab, caption, crop.
- `extract.py` – pulls each frame from the `.mp4` with ffmpeg at the exact timestamp and crops it (needs `git lfs pull` first).
- `content.py` – report text and tables (sections 0–6, appendices).
- `build.py` – ReportLab layout (title block, TOC, captions, tables).
- `build_prereq.py` – companion PDF `01_Staff_Management/Staff_Management_PreBuild_Client_Requirements.pdf`
  (files, sheets, VBA, rules and client decisions needed before build, with reasons and a sign-off checklist).
- `figures/` – the extracted, verified screenshots as embedded in the PDF.
- `asr_*.txt` – timestamped re-transcription of the video audio (Whisper small.en for 00:00–12:05, base.en after).
  The supplied `.srt` belongs to a different meeting (135933, Incidents), so it was not used for timing.

Rebuild: `pip install reportlab pillow pymupdf` then `python3 extract.py && python3 build.py out.pdf && python3 build_prereq.py prereq.pdf`
(`build.py` reads the `figs/` folder that `extract.py` creates next to it.)
