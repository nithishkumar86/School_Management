from crewai.tools import tool
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


@tool("custom_tool3")
def tools3(school_name:str,examination:str) -> str:
    """A custom tool to send warning emails to parents of students who failed criteria"""

    institution_name = None 

    if "school" in school_name.lower():
        institution_name = "School"
    else:
        institution_name = "College"

    server = None
    try:
        path_name = "E:\\SCHOOL_EMAIL_SENDER\\CREWAI_AGENT\\Outputs\\fail_in_pass_or_attendance.csv"
        
        if not os.path.exists(path_name):
            return f"ERROR: Input file not found at {path_name}"
        
        df = pd.read_csv(path_name)

        if df.empty:
            return "INFO: No students failed the criteria. No warning emails to send."
        
        store = {}
        Roll_no = student_name = email_id = Total = Attendance_percentage = None
        
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
            elif "attendance" in col:
                Attendance_percentage = cols
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

        # Counters for report
        email_count = 0
        attendance_issues = 0
        marks_issues = 0
        both_issues = 0
        
        detailed_report = []

        # --- Send warning emails ---
        for i in range(len(df)):
            roll_no = df[Roll_no][i]
            name = df[student_name][i]
            email = df[email_id][i]
            attendance = df[Attendance_percentage][i] if Attendance_percentage else 0
            total = df[Total][i] if Total else 0
            subject_marks = df[subjects].iloc[i].to_dict()
            
            # Analyze failure reasons
            failed_subjects = {sub: mark for sub, mark in subject_marks.items() if mark < 35}
            attendance_low = attendance < 80
            
            # Determine issue type
            has_marks_issue = len(failed_subjects) > 0
            has_attendance_issue = attendance_low
            
            if has_marks_issue and has_attendance_issue:
                both_issues += 1
                issue_type = "BOTH ATTENDANCE AND ACADEMIC PERFORMANCE"
            elif has_marks_issue:
                marks_issues += 1
                issue_type = "ACADEMIC PERFORMANCE"
            else:
                attendance_issues += 1
                issue_type = "ATTENDANCE"

            # Build email body based on issues
            message_parts = [
                f"Dear Pareant or Guardian"
                f"",
                f"{institution_name}: {school_name}"
                f"",
                f"Examination: {examination}",
                f"",
                f"This is an important notice regarding your child, {name}.",
                f"",
                f"",
                f"Roll Number {roll_no}",
                f"",
                f"⚠️ WARNING: REQUIRES IMMEDIATE ATTENTION ⚠️",
                f"",
                f"Issue Category: {issue_type}",
                f"",
            ]

            # Attendance issue details
            if has_attendance_issue:
                message_parts.extend([
                    f"📊 ATTENDANCE CONCERN:",
                    f"Current Attendance: {attendance:.2f}% (Required: 80% minimum)",
                    f"Status: BELOW REQUIRED THRESHOLD",
                    f"",
                ])

            # Academic performance details
            if has_marks_issue:
                message_parts.extend([
                    f"📚 ACADEMIC PERFORMANCE CONCERN:",
                    f"The following subject(s) require immediate attention:",
                    f"",
                ])
                
                for subject, mark in failed_subjects.items():
                    message_parts.append(f"  • {subject}: {mark}/100 (Required: 35 minimum) - FAILED")
                
                message_parts.extend([
                    f"",
                    f"Total Marks: {total}",
                    f"",
                ])

            message_parts.extend([
                f"Complete Performance Report:",
            ])
            
            for subject, mark in subject_marks.items():
                status = "✓ PASS" if mark >= 35 else "✗ FAIL"
                message_parts.append(f"  • {subject}: {mark}/100 - {status}")
            
            message_parts.extend([
                    f"",
                    f"Total Marks: {total}",
                    f"",
                    f"Average Marks: {total / len(subject_marks):.2f}%",
                    f"",
                ])
            
            # Warning and consequences
            message_parts.extend([
                f"",
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
                f"",
                f"⚠️ IMPORTANT WARNING ⚠️",
                f"",
                f"If these issues are not addressed and improved in the upcoming evaluation period:",
                f"",
                f"1. The student may face academic probation",
                f"2. Promotion to the next grade may be at risk",
                f"3. The school will NOT take responsibility for any future academic consequences",
                f"4. Additional remedial classes may be mandated at extra cost",
                f"5. The student may be required to repeat the current academic year",
                f"",
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
                f"",
                f"IMMEDIATE ACTIONS REQUIRED:",
                f"",
            ])

            if has_attendance_issue:
                message_parts.extend([
                    f"• Ensure regular and punctual attendance",
                    f"• Provide valid medical certificates for any absences",
                    f"• Contact the school administration to discuss attendance improvement plan",
                ])

            if has_marks_issue:
                message_parts.extend([
                    f"• Schedule a meeting with subject teachers",
                    f"• Enroll in remedial/tutoring programs",
                    f"• Establish a structured study routine at home",
                    f"• Monitor homework and assignment completion daily",
                ])

            message_parts.extend([
                f"",
                f"Please contact the school office within 7 days to discuss an improvement plan.",
                f"",
                f"We are committed to your child's success, but we need your immediate cooperation.",
                f"",
                f"Best regards,",
                f"School Administration",
                f"",
                f"For queries, please contact the school office.",
            ])

            message_parts.extend([            
                f"Best regards",
                f"",
                f" {school_name} Administration"
            ])

            message = "\n".join(message_parts)

            # Prepare email
            msg = MIMEMultipart()
            msg["From"] = SENDER_EMAIL
            msg["To"] = email
            msg["Subject"] = f"⚠️ URGENT: Academic/Attendance Warning - {name}"
            msg.attach(MIMEText(message, "plain"))

            # Send
            server.sendmail(SENDER_EMAIL, email, msg.as_string())
            email_count += 1
            
            # Add to detailed report
            issue_summary = []
            if has_attendance_issue:
                issue_summary.append(f"Attendance: {attendance:.2f}%")
            if has_marks_issue:
                failed_list = ", ".join([f"{s}({m})" for s, m in failed_subjects.items()])
                issue_summary.append(f"Failed: {failed_list}")
            
            detailed_report.append(f"  {email_count}. {name} ({email}) - {' | '.join(issue_summary)}")
            
            print(f"⚠️ Warning email sent to {name} ({email}) - Issue: {issue_type}")

        # Build summary report
        result = f"""WARNING EMAILS SENT SUCCESSFULLY!

Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total warning emails sent: {email_count}

Breakdown by Issue Type:
- Attendance issues only: {attendance_issues}
- Academic performance issues only: {marks_issues}
- Both attendance and performance issues: {both_issues}

Detailed Report:
{chr(10).join(detailed_report)}

All parents have been notified about their child's performance concerns.
School administration should follow up within 7 days.
"""
        
        return result
        
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
                pass