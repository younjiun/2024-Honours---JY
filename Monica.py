import streamlit as st
import re
import io
import zipfile

def separate_and_format_accounts(text):
    accounts = re.split(r'(?=P\d+\t)', text.strip())
    formatted_accounts = []
    
    for account in accounts:
        if account.strip():
            case_id_match = re.search(r'P\d+', account)
            case_id = case_id_match.group() if case_id_match else "Unknown"
            
            parts = account.split('\t')
            if len(parts) >= 5:
                username = parts[1]
                substance = parts[2]
                diagnosis = parts[3]
                account_text = parts[4]
            else:
                username = substance = diagnosis = "Unknown"
                account_text = account
            
            formatted_account = f"""CaseID: {case_id}
Username: {username}
Substance: {substance}
Diagnosis: {diagnosis}

{account_text.strip()}
"""
            formatted_accounts.append((case_id, username, substance, diagnosis, formatted_account))
    
    return formatted_accounts

st.title('NVivo Account Separator and Formatter')

input_text = st.text_area("Enter the long text containing multiple accounts:", height=300)

if st.button('Process Accounts'):
    if input_text:
        formatted_accounts = separate_and_format_accounts(input_text)
        
        # Create a BytesIO object to store the zip file
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for i, (case_id, username, substance, diagnosis, account) in enumerate(formatted_accounts, 1):
                st.subheader(f"Account {i}")
                st.text_area(f"Formatted Account {i}", account, height=200)
                
                # Create a filename based on case information
                filename = f"{case_id}_{username}_{substance}_{diagnosis}.txt"
                filename = re.sub(r'[^\w\-_\. ]', '_', filename)  # Replace invalid filename characters
                
                st.download_button(
                    label=f"Download {filename}",
                    data=account,
                    file_name=filename,
                    mime="text/plain"
                )
                
                # Add the file to the zip archive
                zip_file.writestr(filename, account)
        
        # Create a download button for the zip file
        zip_buffer.seek(0)
        st.download_button(
            label="Download All Accounts",
            data=zip_buffer,
            file_name="all_accounts.zip",
            mime="application/zip"
        )
    else:
        st.warning("Please enter some text to process.")

st.markdown("""
### Instructions:
1. Paste your long text containing multiple accounts into the text area above.
2. Click the 'Process Accounts' button.
3. The dashboard will separate and format each account.
4. You can review each formatted account and download them individually.
5. Use the 'Download All Accounts' button to get a zip file containing all formatted accounts.
""")
