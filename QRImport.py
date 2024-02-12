import pandas as pd
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
import qrcode
import re

def normalize_phone_number(phone):
    # Remove spaces and standardize phone numbers
    phone = re.sub(r'\s+', '', phone)
    if phone.startswith('91') and not phone.startswith('+91'):
        phone = '+' + phone
    elif len(phone) == 10:
        phone = '+91' + phone
    return phone

def get_contact_info(contact_name, contacts_simplified):
    # Extract contact info based on the selected name
    return contacts_simplified[contacts_simplified['Full Name'] == contact_name].iloc[0]

def create_vcf(contact_info):
    print(contact_info)
    # Extract relevant information
    first_name = contact_info['First Name']
    last_name = contact_info['Last Name']
    company_name = contact_info['Company Name']
    phone_number = normalize_phone_number(contact_info['Phone'])
    
    # Conditionally format the title part
    title = contact_info.get('Title', '').strip()
    title_part = f" {title}" if title else ""
    
    vcf_content = f"""
BEGIN:VCARD
VERSION:3.0
N:{last_name};{first_name}{title_part} {company_name};;;
FN:{first_name}{title_part} {company_name}
ORG:{company_name}
TEL;TYPE=WORK,VOICE:{phone_number}
END:VCARD
    """.strip()
    
    # Overwrite the same VCF file for each contact
    with open("contact.vcf", "w") as file:
        file.write(vcf_content)

def generate_qr_code():
    # Generate QR code from the VCF file content
    with open('contact.vcf', 'r') as file:
        qr_data = file.read()
    qr = qrcode.make(qr_data)
    qr.save('contact_qr.png')

def main():
    contacts_df = pd.read_csv('Contacts.csv')
    # Combine Phone and Mobile fields, giving priority to non-empty Phone
    contacts_df['Phone'] = contacts_df.apply(lambda x: x['Mobile'] if pd.isna(x['Phone']) else x['Phone'], axis=1)
    contacts_df['Full Name'] = contacts_df['First Name'].astype(str) + ' ' + contacts_df['Last Name'].astype(str)
    contacts_simplified = contacts_df[['First Name', 'Last Name', 'Company Name', 'Phone', 'Full Name', 'Title']].dropna(subset=['Phone'])

    contact_names = [str(name) for name in contacts_simplified['Full Name'].tolist()]
    completer = FuzzyWordCompleter(contact_names)

    while True:
        print("Enter contact name (or type 'done' to finish):")
        contact_name = prompt("Contact Name: ", completer=completer)
        if contact_name.lower() == 'done':
            break
        contact_info = get_contact_info(contact_name, contacts_simplified)
        create_vcf(contact_info)
        generate_qr_code()
        print(f"Generated QR code for {contact_name}. Scan 'contact_qr.png'.")

if __name__ == "__main__":
    main()
