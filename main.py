#!/usr/bin/env python3
import os
import sys
import tempfile
import glob
import shutil
from datetime import timedelta
import yt_dlp
import srt

# --- NEW: reportlab imports for PDF ---
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

def format_timestamp(td: timedelta):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    if hours:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"

def load_srt_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    return list(srt.parse(text))

def combine_subtitles_to_paragraph(subs):
    texts = []
    for sub in subs:
        t = sub.content.replace("\n", " ").strip()
        if t:
            texts.append(t)
    paragraph = " ".join(texts).strip()
    return paragraph

def save_as_text(filename, grouped):
    with open(filename, "w", encoding="utf-8") as out:
        out.write("Chapter\n")
        for g in grouped:
            ch_ts = format_timestamp(timedelta(seconds=int(g["start"])))
            out.write(f"{ch_ts}\n")
            out.write(f"{g['title']}\n")
            if g["subs"]:
                first_sub_ts = format_timestamp(g["subs"][0].start)
                out.write(f"{first_sub_ts}\n")
                paragraph = combine_subtitles_to_paragraph(g["subs"])
                out.write(paragraph + "\n\n")
            else:
                out.write("(No subtitle text for this chapter)\n\n")

def save_as_pdf(filename, grouped, title):
    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    heading = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        spaceBefore=12,
        spaceAfter=6
    )
    story = []

    story.append(Paragraph(f"<b>{title}</b>", styles["Title"]))
    story.append(Spacer(1, 0.25*inch))
    story.append(Paragraph("Chapter", heading))

    for g in grouped:
        ch_ts = format_timestamp(timedelta(seconds=int(g["start"])))
        story.append(Paragraph(f"<b>{ch_ts}</b>", heading))
        story.append(Paragraph(g['title'], styles["Heading3"]))
        if g["subs"]:
            first_sub_ts = format_timestamp(g["subs"][0].start)
            story.append(Paragraph(f"{first_sub_ts}", styles["Italic"]))
            paragraph = combine_subtitles_to_paragraph(g["subs"])
            story.append(Paragraph(paragraph, normal))
        else:
            story.append(Paragraph("(No subtitle text for this chapter)", normal))
        story.append(Spacer(1, 0.2*inch))

    doc = SimpleDocTemplate(filename, pagesize=A4)
    doc.build(story)

def main():
    url = input("Enter YouTube URL: ").strip()
    if not url:
        print("No URL provided. Exiting.")
        return

    tempdir = tempfile.mkdtemp(prefix="yt_subs_")
    try:
        outtmpl = os.path.join(tempdir, "%(id)s.%(ext)s")
        ydl_opts = {
            "outtmpl": outtmpl,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitlesformat": "srt",
            "skip_download": True,
            "quiet": True,
            "no_warnings": True,
        }
        print("Fetching metadata and downloading subtitles...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        video_id = info.get("id", "video")
        title = info.get("title", video_id).strip().replace("\n", " ").replace("\r", "")
        chapters = info.get("chapters", None)

        srt_files = glob.glob(os.path.join(tempdir, "*.srt"))
        if not srt_files:
            print("No subtitles (.srt) were downloaded.")
            return

        srt_path = srt_files[0]
        subtitles = load_srt_file(srt_path)
        if not subtitles:
            print("Subtitle file is empty.")
            return

        chapter_list = []
        if chapters:
            for ch in chapters:
                start = ch.get("start_time", 0.0)
                title_ch = ch.get("title", "").strip()
                chapter_list.append({"start": float(start), "title": title_ch})
        else:
            chapter_list.append({"start": 0.0, "title": "Chapter"})

        chapter_list = sorted(chapter_list, key=lambda x: x["start"])
        for i in range(len(chapter_list)):
            start = chapter_list[i]["start"]
            end = chapter_list[i+1]["start"] if i+1 < len(chapter_list) else None
            chapter_list[i]["end"] = end

        grouped = []
        for ch in chapter_list:
            ch_start = ch["start"]
            ch_end = ch["end"]
            ch_subs = []
            for sub in subtitles:
                sub_start_sec = sub.start.total_seconds()
                if sub_start_sec >= ch_start and (ch_end is None or sub_start_sec < ch_end):
                    ch_subs.append(sub)
            grouped.append({"start": ch_start, "title": ch["title"], "subs": ch_subs})

        safe_title = "".join(c if c.isalnum() or c in " ._-()" else "_" for c in title)[:200]
        txt_filename = f"{safe_title}_chapters_subtitles.txt"
        pdf_filename = f"{safe_title}_chapters_subtitles.pdf"

        save_as_text(txt_filename, grouped)
        save_as_pdf(pdf_filename, grouped, title)

        print(f"✅ Output saved to:\n- {os.path.abspath(txt_filename)}\n- {os.path.abspath(pdf_filename)}")
    except Exception as e:
        print("Error:", str(e))
    finally:
        try:
            shutil.rmtree(tempdir)
        except Exception:
            pass

if __name__ == "__main__":
    main()
