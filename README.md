# Nature Preserve Reporting Tools

This repository contains a suite of tools designed to streamline the process of documenting site visits to nature reserves. It consists of a mobile-friendly field data collector and a desktop-based report generator with a Python backend.

## Components

### 1. Field Collector (`field collector.html`)
A mobile-first web application designed to be used in the field.

*   **Offline Capable**: Works in the browser without an active connection (after initial load).
*   **Data Entry**: Easily record trip details, observations, species lists (plants, animals, fungi), and notes.
*   **Autosave**: Progress is saved locally in the browser to prevent data loss.
*   **Export**: Exports collected data as a JSON file for use with the Report Generator.

### 2. Field Report Generator (`Field Report Generator.html`)
A desktop web application for compiling your visit data into a polished report.

*   **Import**: Load JSON data file exported from the Field Collector.
*   **Photo Management**: Drag and drop photos directly into the report.
*   **EXIF Data**: Automatically reads GPS and timestamp data from photos.
*   **Species Verification**: Cross-references observations against a local database.
*   **Export Options**:
    *   **PDF**: Generates a professional PDF report with a location map.
    *   **Word**: Exports an editable Microsoft Word (`.docx`) document.

## Setup

This tool uses a Python backend for generating reports and database lookups.

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Server**:
    ```bash
    python server.py
    ```
    The server works on `http://localhost:5000`.

## Workflow

1.  **Field Visit**: Open `field collector.html` on your mobile device. Fill in details as you observe them.
2.  **Export Data**: At the end of the visit, click "Export" to save your data as a `.json` file.
3.  **Start Server**: Ensure `server.py` is running on your computer.
4.  **Generate Report**: Open `Field Report Generator.html`.
5.  **Load Data**: Click "Load Data" and select the JSON file from your visit.
6.  **Add Photos**: Drag and drop your site photos into the photo grid area.
7.  **Generate**: Click "Generate Report" (PDF) or "Save as Word" (DOCX).
