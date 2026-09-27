# Sports Booking System

A desktop sports-facility reservation application built with **Python, Tkinter/CustomTkinter and MongoDB**.

The application lets users:
- create a local account / log in through the desktop interface
- browse sports facilities
- create and view reservations
- detect reservation conflicts and suggest alternative slots
- choose reservation plans and optional services
- simulate a payment flow and export a PDF receipt
- view sports news and use a rule-based reservation assistant
- visualize reservation statistics with Pandas and Matplotlib
- export reservation statistics to Excel

## Project type

This is a **desktop GUI application**, not a Flask/web application. It starts a Tkinter window on the computer where Python is installed.

Because of that architecture, it cannot be deployed directly to services such as GitHub Pages, Vercel, or Render as a normal web app. A public demo would require either:
1. packaging the desktop application as an executable and distributing it, or
2. migrating/rebuilding the interface as a web application.

For the competition demo, running it locally is the simplest and most reliable option.

## Tech stack

- Python 3.10+ recommended
- Tkinter
- CustomTkinter
- Pillow
- Pandas
- Matplotlib
- PyMongo
- ReportLab
- OpenPyXL
- MongoDB Atlas
- CSV files for statistics/news data

## Project structure

```text
sports-booking-system/
├── login.py             # Login, registration and password-reset UI
├── home.py              # Main dashboard
├── reservation.py       # Facility selection and reservation workflow
├── payment.py           # Plan selection, payment simulation and PDF receipt
├── news.py              # News and reservation assistant
├── stats.py             # Reservation analytics and Excel export
├── reservations.csv     # Sample/local statistics data
├── news_data.csv        # Sample news data
├── pictures/            # Sports and background images
├── recu_paiement.pdf    # Example/generated payment receipt
├── requirements.txt
├── .env.example
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/manar09-code/sports-booking-system.git
cd sports-booking-system
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> Tkinter is normally included with standard Python installations on Windows. On some Linux distributions it must be installed separately.

## MongoDB configuration

The reservation module uses MongoDB through PyMongo.

**Security note:** the original project code contains a MongoDB connection string with credentials embedded in source code. Do not publish or reuse exposed database credentials. Rotate/revoke that credential in MongoDB Atlas and move the new connection string to an environment variable before sharing the repository publicly.

Recommended configuration:

```text
MONGODB_URI=your_mongodb_connection_string
```

The current application code will need to be updated to read this variable before the environment-file approach is active.

## Run the application

Start the login screen:

```bash
python login.py
```

The application then opens the desktop interface and navigates between the login, dashboard, reservation, payment, news and statistics modules.

## Important current code notes

Before presenting the project on another computer, check these existing path/configuration issues:

- `reservation.py` references `Pictures/`, while the repository directory is `pictures/`. On case-sensitive systems this can prevent the sports images from loading.
- `payment.py` looks for `payement.jpg` at the project root, but that image is not present in the repository listing.
- Login and registration are currently UI/demo flows rather than persistent user authentication.
- Payment is a simulation. It does not connect to a real payment gateway.
- The reservation module uses MongoDB Atlas, so an accessible database and valid connection credentials are required.
- Statistics use the repository's CSV data rather than exclusively querying MongoDB.
- The news assistant is rule/keyword based. It does not currently call an external generative-AI API.
- The application uses desktop windows, so browser-based hosting is not supported without architectural changes.

## Demo flow for a competition

A clean demo can follow this sequence:

1. Launch `login.py`.
2. Demonstrate login/registration.
3. Open the dashboard.
4. Show the available sports facilities.
5. Create a reservation.
6. Demonstrate a conflicting reservation and the alternative-slot suggestion.
7. Continue to the payment screen.
8. Select a plan and show the calculated price/discount.
9. Export the payment receipt as PDF.
10. Open Statistics and show the reservation charts.
11. Show the News / Assistant section.

This sequence demonstrates the project's main user journey without spending the demo explaining every implementation detail.

## Author

**Manar Degachi**

GitHub: https://github.com/manar09-code
