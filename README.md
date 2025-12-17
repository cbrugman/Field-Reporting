# Nature Preserve Reporting Tools

This repository contains a suite of tools designed to streamline the process of documenting site visits to nature reserves. It consists of a mobile-friendly field data collector and a desktop-based report generator.

## Components

### 1. Field Collector (`field collector.html`)
A mobile-first web application designed to be used in the field.

*   **Offline Capable**: Works in the browser without an active connection (after initial load).
*   **Data Entry**: Easily record trip details, observations, species lists (plants, animals, fungi), and notes.
*   **Autosave**: Progress is saved locally in the browser to prevent data loss.
*   **Export**: Exports collected data as a JSON file for use with the Report Generator.

### 2. Field Report Generator (`Field Report Generator.html`)
A desktop web application for compiling your visit data into a polished PDF report.

*   **Import**: Load JSON data file exported from the Field Collector.
*   **Photo Management**: Drag and drop photos directly into the report.
*   **EXIF Data**: Automatically reads GPS and timestamp data from photos (requires `exif-js`).
*   **Customization**: Add captions, rearrange photos, and edit text fields.
*   **Export**: Designed to be "Printed to PDF" to create a final, professional-looking report.

## Workflow

1.  **Field Visit**: Open `field collector.html` on your mobile device. Fill in details as you observe them.
2.  **Export Data**: At the end of the visit, click "Export" to save your data as a `.json` file.
3.  **Generate Report**: On your desktop, open `Field Report Generator.html`.
4.  **Load Data**: Click "Load Data" and select the JSON file from your visit.
5.  **Add Photos**: Drag and drop your site photos into the photo grid area.
6.  **Review & Save**: Edit any text as needed. Use your browser's "Print" function and select "Save as PDF" to generate the final document.
