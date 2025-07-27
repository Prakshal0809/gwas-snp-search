# GWAS SNP Search Web Application

A modern web application for searching and extracting genetic variants (SNPs) associated with specific traits from the GWAS Catalog database.

## Features

- 🔍 **Easy Search Interface**: Simple web form to search for SNPs by trait
- 📊 **Real-time Progress**: Live progress updates during scraping
- 📁 **Excel Export**: Download results as Excel files
- 🎨 **Modern UI**: Beautiful, responsive design
- ⚡ **Background Processing**: Non-blocking search operations
- 📱 **Mobile Friendly**: Works on all devices

## Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- ChromeDriver (will be automatically managed by Selenium)

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install ChromeDriver (if not already installed):**
   ```bash
   # On Windows (using chocolatey):
   choco install chromedriver
   
   # On macOS (using homebrew):
   brew install chromedriver
   
   # On Linux:
   sudo apt-get install chromium-chromedriver
   ```

## Usage

1. **Start the web application:**
   ```bash
   python app.py
   ```

2. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **Enter a search term** (e.g., "facial wrinkling", "dental caries", "diabetes")

4. **Click "Search SNPs"** and wait for the process to complete

5. **Download the Excel file** when the search is finished

## Example Search Terms

- `facial wrinkling`
- `dental caries`
- `diabetes`
- `obesity`
- `hypertension`
- `cardiovascular disease`
- `cancer`
- `alzheimer's disease`

## How It Works

1. **Search**: The application searches the GWAS Catalog for studies related to your search term
2. **Extract**: It extracts SNP data including:
   - Primary SNP identifier
   - Risk and non-risk alleles
   - P-values
   - Beta values
   - Associated traits
   - Study links
   - PubMed IDs
   - DOI links
3. **Filter**: Only SNPs with significant p-values (< 5e-8) are included
4. **Export**: Results are saved as an Excel file with timestamps

## File Structure

```
├── app.py                 # Main Flask application
├── gwas_scraper.py        # GWAS scraping logic
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface
├── downloads/            # Generated Excel files (created automatically)
└── README.md            # This file
```

## API Endpoints

- `GET /` - Main web interface
- `POST /api/search` - Start a new search
- `GET /api/status` - Get current search status
- `GET /api/download/<filename>` - Download result file

## Configuration

You can modify the following settings in `app.py`:

- `max_pages`: Maximum number of pages to scrape (default: 10)
- `UPLOAD_FOLDER`: Directory for saving files (default: 'downloads')
- `MAX_CONTENT_LENGTH`: Maximum file size (default: 16MB)

## Troubleshooting

### Common Issues

1. **ChromeDriver not found:**
   - Make sure Chrome browser is installed
   - Install ChromeDriver manually if automatic detection fails

2. **Search taking too long:**
   - Reduce `max_pages` in the scraper function
   - Check your internet connection

3. **No results found:**
   - Try different search terms
   - Check if the GWAS Catalog is accessible

4. **Permission errors:**
   - Ensure the application has write permissions to the downloads folder

### Error Messages

- **"A search is already in progress"**: Wait for the current search to complete
- **"Search term is required"**: Enter a valid search term
- **"File not found"**: The requested file doesn't exist or was deleted

## Development

To run in development mode with debugging:

```bash
python app.py
```

The application will be available at `http://localhost:5000` with debug information.

## Production Deployment

For production deployment, consider:

1. Using a production WSGI server (e.g., Gunicorn)
2. Setting up proper logging
3. Implementing rate limiting
4. Adding authentication if needed
5. Using environment variables for configuration

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## License

This project is for educational and research purposes. Please respect the terms of service of the GWAS Catalog database.

## Contributing

Feel free to submit issues and enhancement requests! 