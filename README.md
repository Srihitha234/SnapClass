# SnapClass – AI-Powered Attendance System

SnapClass is an AI-powered attendance management system designed to simplify classroom attendance using **facial recognition and voice biometrics**. It provides a digital platform for teachers to manage courses, register students, record attendance, and maintain attendance records.

## Features

- **AI Face Recognition:** Identify students from classroom photos to automate attendance marking.
- **Voice-Based Attendance:** Use voice biometrics to verify students during attendance.
- **Student Enrollment:** Support student registration and biometric enrollment.
- **Course Management:** Create and manage subjects and student rosters.
- **Attendance Records:** Store and review attendance information.
- **QR-Based Enrollment:** Simplify student enrollment using course-related QR codes.
- **Cloud Database:** Use Supabase for database storage and related backend functionality.
- **Interactive Interface:** Built with Streamlit for an accessible user experience.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | User interface |
| OpenCV | Image processing and computer vision |
| Face Recognition / Dlib | Facial recognition |
| Resemblyzer | Voice embeddings |
| Librosa | Audio processing |
| Supabase | Database and cloud services |
| NumPy and Pandas | Data processing |
| Git and GitHub | Version control |

## Project Structure

```text
SnapClass/
├── app.py
├── src/
│   ├── components/
│   ├── pages/
│   └── ...
├── requirements.txt
├── .gitignore
└── README.md
```

*Note: The structure above is a simplified overview. The exact contents of `src/` may vary as the project develops.*

## Getting Started

### Prerequisites

- Python installed on your system
- Git
- A Supabase project and the required credentials, if using cloud database functionality

### 1. Clone the Repository

```bash
git clone https://github.com/Srihitha234/SnapClass.git
cd SnapClass
```

### 2. Create a Virtual Environment

On Windows:

```bash
python -m venv venv
```

Activate it in PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If activation is blocked, use Command Prompt instead:

```cmd
venv\Scripts\activate.bat
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

Some computer-vision and audio-processing dependencies may require additional system setup, depending on your Python version and operating system.

### 4. Configure Environment Variables

Configure the Supabase credentials required by the application. Use the variable names expected by your existing source code.

For example, if your application reads these names:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_key
```

Place them in a local `.env` file only if your code supports loading `.env` files. Otherwise, configure them using the environment-variable mechanism already implemented in your project.

**Security:** Never commit actual API keys, passwords, or other secrets to GitHub.

### 5. Run the Application

From the project root, run:

```bash
python -m streamlit run app.py
```

Streamlit will display a local URL in the terminal, usually:

```text
http://localhost:8501
```

Open that URL in your browser to access SnapClass.

## Deployment

The original SnapClass application is deployed on Streamlit Community Cloud:

**Live Application:** https://snapcl-main.streamlit.app/

Deployment requires the appropriate dependencies and securely configured secrets.

## Future Improvements

- Improve recognition accuracy under different lighting and audio conditions.
- Enhance attendance analytics and reporting.
- Strengthen biometric data security and access controls.
- Improve the user experience for teachers and students.
- Expand testing and error handling.

## Contributing

Contributions and suggestions are welcome. Fork the repository, create a branch for your changes, and submit a pull request.

## License

A license has not been specified yet. Please add an appropriate license file before distributing the project under an open-source license.

---

**SnapClass — Making classroom attendance smarter with AI.**
