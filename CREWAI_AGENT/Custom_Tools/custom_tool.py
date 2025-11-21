from crewai.tools import tool
import pandas as pd
import os
import traceback


@tool("custom_tool1")
def tools1() -> str:
    """
    Tool to identify the data.csv in the Inputs dir and perform some analysis 
    and preprocessing, then save results to Outputs dir.
    """
    try:
        # Verify file exists first
        path = "E:/SCHOOL_EMAIL_SENDER/CREWAI_AGENT/Inputs/data.csv"
        if not os.path.exists(path):
            return f"ERROR: Input file not found at {path}"
        
        # Load data
        df = pd.read_csv(path)
        
        if df.empty:
            return "ERROR: CSV file is empty"
        
        # Debug: Show all columns
        all_columns = df.columns.tolist()
        
        stores = {}
        Roll_no = Name = Total = Attendance_Percentage = Activity = Email = None

        # Detect columns automatically with more flexible matching
        for cols in df.columns:
            col = cols.lower().strip()  # Also strip whitespace
            
            if "roll" in col or "serial" in col or "registration" in col or "reg" in col:
                Roll_no = cols
                stores[cols] = cols
            elif "student" in col or "name" in col:
                Name = cols
                stores[cols] = cols
            elif "total" in col or "marks" in col:
                Total = cols
                stores[cols] = cols
            elif "attendance" in col or col == "attendance_percentage":
                Attendance_Percentage = cols
                stores[cols] = cols
            elif "activity" in col or "act" in col:
                Activity = cols
                stores[cols] = cols
            elif "email" in col or "mail" in col or "parent" in col:
                Email = cols
                stores[cols] = cols

        # Debug output
        detected_info = f"""
Detected Columns:
- All columns: {all_columns}
- Roll_no: {Roll_no}
- Name: {Name}
- Attendance_Percentage: {Attendance_Percentage}
- Activity: {Activity}
- Email: {Email}
"""
        
        # Detect numeric subject columns
        numeric_cols = df.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns.tolist()
        
        # Remove non-subject columns
        cols = [col for col in numeric_cols if col not in stores.values()]
        subjects = cols
        
        if not subjects:
            return f"ERROR: No subject columns detected in the dataset\n{detected_info}"

        # Determine pass/fail (>= 35 in all subjects)
        df["pass_all"] = df[subjects].ge(35).all(axis=1)

        # Calculate total if not present
        if Total and Total in df.columns:
            pass
        else:
            df['Total'] = df[subjects].sum(axis=1)
            Total = 'Total'

        # Handle attendance/percentage logic with better error handling
        if Attendance_Percentage and Attendance_Percentage in df.columns:
            # Use existing percentage column
            df["p_ok"] = pd.to_numeric(df[Attendance_Percentage], errors='coerce') >= 80.0
        else:
            return f"ERROR: Cannot calculate attendance percentage\n{detected_info}"

        # Filter pass/fail
        pass_df = df[(df["pass_all"]) & (df["p_ok"])]
        fail_df = df[~((df["pass_all"]) & (df["p_ok"]))]

        # Save output files
        output_dir = "E:\\SCHOOL_EMAIL_SENDER\\CREWAI_AGENT\\Outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        path1 = os.path.join(output_dir, "pass_all_got_attendance_80.csv")
        path2 = os.path.join(output_dir, "fail_in_pass_or_attendance.csv")

        pass_df.to_csv(path1, index=False)
        fail_df.to_csv(path2, index=False)

        # Return string summary
        result = f"""Analysis completed successfully!

Summary:
- Total students: {len(df)}
- Students who passed all subjects with 80%+ attendance: {len(pass_df)}
- Students who failed criteria: {len(fail_df)}
- Subjects analyzed: {', '.join(subjects)}

Column Detection:
{detected_info}

Output files saved:
- Pass file: {path1}
- Fail file: {path2}
"""
        return result

    except FileNotFoundError as e:
        return f"ERROR: File not found - {str(e)}"
    except pd.errors.EmptyDataError:
        return "ERROR: CSV file is empty or corrupted"
    except KeyError as e:
        return f"ERROR: Missing expected column - {str(e)}"
    except Exception as e:
        error_details = traceback.format_exc()
        return f"ERROR: Unexpected error occurred:\n{str(e)}\n\nFull traceback:\n{error_details}"