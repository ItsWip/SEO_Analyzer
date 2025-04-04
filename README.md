# SEO Analysis Website

## Overview
This is a Python-based SEO analysis website that provides insights into on-page, off-page, and technical SEO factors. It allows users to analyze their website's SEO, compare metrics with competitors, and receive actionable improvement suggestions.

## Features
- **SEO Analysis**: Extracts key SEO metrics such as title tags, meta descriptions, keywords, speed, and mobile-friendliness.
- **Competitor Comparison**: Scrapes SEO data from competitor websites and generates comparative insights.
- **Improvement Suggestions**: Provides recommendations to enhance website rankings.
- **Responsive UI**: Clean and mobile-friendly interface.
- **Charts & Tables**: Displays SEO results in an easy-to-understand format.
- **Free APIs & Tools**: Uses only open-source libraries and free APIs.

## Tech Stack
### Backend:
- Python
- Flask / FastAPI

### Frontend:
- HTML, CSS, JavaScript

### SEO Analysis:
- BeautifulSoup
- Requests
- Google PageSpeed API

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ItsWip/SEO_Analyzer/seo-analysis-website.git
   cd SEO_Analyzer
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and visit:
   ```
   http://127.0.0.1:5000  # Flask Default Port
   ```

## Usage
1. Enter the URL of the website you want to analyze.
2. Click "Analyze" to extract SEO metrics.
3. View results in a structured format with suggestions.
4. Compare with competitor websites.

## Free APIs & Tools Used
- Google PageSpeed API
- BeautifulSoup (Web Scraping)
- Requests (HTTP Requests)

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`feature-branch-name`).
3. Commit your changes.
4. Push the branch and create a pull request.

## License
This project is open-source and available under the [MIT License](LICENSE).

## Contact
For any inquiries, feel free to reach out:
- GitHub: ItsWip(https://github.com/your-username)
- Email: pswaraj0614@gmail.com
