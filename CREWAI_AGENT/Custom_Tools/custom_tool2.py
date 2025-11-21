from crewai.tools import tool
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


@tool("custom_tool2")
def tools2(school_name:str,examination:str) -> str:

    """A custom tool to send an email notification through an SMTP server"""
    institution_name = None 

    if "school" in school_name.lower():
        institution_name = "School"
    else:
        institution_name = "College"
        
    server = None
    try:
        path_name = "E:\\SCHOOL_EMAIL_SENDER\\CREWAI_AGENT\\Outputs\\pass_all_got_attendance_80.csv"
        
        if not os.path.exists(path_name):
            return f"ERROR: Input file not found at {path_name}"
        
        df = pd.read_csv(path_name)

        if df.empty:
            return "ERROR: DataFrame is empty - no students to email"
        
        store = {}
        Roll_no = student_name = email_id = Total = Attendance_percentage = None  # ✅ Fixed typo
        
        for cols in df.columns.tolist():
            col = cols.strip().lower()
            if "roll" in col or "no" in col or "number" in col:
                Roll_no = cols
                store[cols] = cols
            elif "student" in col or "name" in col:
                student_name = cols
                store[cols] = cols
            elif "email" in col or "parent" in col:
                email_id = cols
                store[cols] = cols
            elif "total" in col or "marks" in col:
                Total = cols
                store[cols] = cols
            elif "attendance" in col or "percentage" in col:
                Attendance_percentage = cols  # ✅ Fixed typo
                store[cols] = cols

        numeric_cols = df.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns.tolist()
        cols = [col for col in numeric_cols if col not in store.values()]
        subjects = cols

        # Validate required columns
        if not email_id or not student_name:
            return f"ERROR: Required columns not found. Email: {email_id}, Name: {student_name}"

        # --- Email setup ---
        SENDER_EMAIL = os.getenv("SENDER_EMAIL")
        if not SENDER_EMAIL:
            return "ERROR: SENDER_EMAIL not found in environment variables."
        
        SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
        if not SENDER_PASSWORD:
            return "ERROR: SENDER_PASSWORD not found in environment variables."

        # Create SMTP session
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # --- Send emails ---
        email_count = 0
        for i in range(len(df)):
            roll_no = df[Roll_no][i]
            name = df[student_name][i]
            email = df[email_id][i]
            attendance = df[Attendance_percentage][i] if Attendance_percentage else "N/A"  # ✅ Fixed typo
            total = df[Total][i] if Total else 0
            subject_marks = df[subjects].iloc[i].to_dict()
            average = total / len(subject_marks) if subject_marks else 0

            # Format marks as a string
            marks_str = "\n".join([f"{sub}: {mark}" for sub, mark in subject_marks.items()])

            # Email content
            message = f"""
            Dear Parent,

            {institution_name}: {school_name}
            Examination: {examination}

            Roll No: {roll_no}

            Mr. {name} has passed all subjects and maintained {attendance}% attendance.

            Marks Details:
            {marks_str}

            Total: {total}
            Average: {average:.2f}%

            Keep up the great performance!

            Best regards,
            {school_name} Administration
            """

            # Prepare email
            msg = MIMEMultipart()
            msg["From"] = SENDER_EMAIL
            msg["To"] = email
            msg["Subject"] = "Student Performance Report"
            msg.attach(MIMEText(message, "plain"))

            # Send
            server.sendmail(SENDER_EMAIL, email, msg.as_string())
            email_count += 1
            print(f"✅ Email sent successfully to {name} ({email})")

        return f"SUCCESS: Emails sent successfully to {email_count} passing students."  # ✅ String return
        
    except smtplib.SMTPAuthenticationError:
        return "ERROR: SMTP Authentication failed. Check your email and password."
    except smtplib.SMTPException as e:
        return f"ERROR: SMTP error occurred: {str(e)}"
    except Exception as e:
        return f"ERROR: {str(e)}"
    finally:
        if server:
            try:
                server.quit()
            except:
                pass  # Ignore errors when closing