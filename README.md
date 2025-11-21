# School Management Automation System

A complete automation tool designed to simplify school-related workflows. This system helps administrators, teachers, and staff easily **send emails**, **manage communications**, and **generate automated reports** quickly and efficiently.

---

## 🚀 Features

### ✔ Email Automation

* Automatically send emails to students, parents, and staff.
* Supports bulk emailing.
* Customizable email templates.

### ✔ Environment-Based Configuration

* Uses a `.env` file for storing sensitive information.
* Supports API keys for external services securely.

### ✔ Clean Project Structure

```
SCHOOL_EMAIL_SENDER/
├── school/                  # Virtual environment
├── src/                     # Main application code
├── assets/                  # Any images, files, templates
├── .gitignore               # Ignored files
└── README.md                # Project documentation
```

---

## 📦 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/nithishkumar86/School_Management.git
cd School_Management
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv school
```

### 3️⃣ Activate Environment

**Windows:**

```bash
school\Scripts\activate
```

**Linux / macOS:**

```bash
source school/bin/activate
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
EMAIL_PASSWORD=your_email_password
```

Make sure `.env` is added to `.gitignore`.

---

## ▶ Running the Project

```bash
streamlit run frontend.py
```

---

## 🛡 Security

* `.env` file is ignored by Git.
* API keys must be rotated regularly.
* Never commit sensitive keys.

---

## 🤝 Contribution

Pull requests are welcome! Follow these steps:

* Fork the repo
* Create a feature branch
* Submit a PR

---

## 📄 License

This project is licensed under the MIT License.

---

## 💬 Support

For issues or feature requests:

* Open an issue on GitHub
* Contact the project maintainer

