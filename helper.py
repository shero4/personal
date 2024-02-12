import pandas as pd
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter

def load_csv_files():
    pipelines_df = pd.read_csv('Pipelines.csv')
    notes_df = pd.read_csv('Notes.csv')
    contacts_df = pd.read_csv('Contacts.csv')
    return pipelines_df, notes_df, contacts_df

def get_main_and_other_contacts(deal_id, pipelines_df, contacts_df):
    # Find the company ID and main contact ID associated with the deal ID
    deal_row = pipelines_df[pipelines_df['Deal Id'] == deal_id].iloc[0]
    company_id = deal_row['Company Id']
    main_contact_id = deal_row['Contact Id']
    
    # Fetch the main contact details
    main_contact = contacts_df[contacts_df['Contact Id'] == main_contact_id]
    
    # Get all other contacts associated with the company, excluding the main contact
    other_contacts = contacts_df[(contacts_df['Company Id'] == company_id) & (contacts_df['Contact Id'] != main_contact_id)]
    
    return main_contact, other_contacts

def print_contacts(main_contact, other_contacts):
    print("Main Contact:")
    for index, contact in main_contact.iterrows():
        phone = contact['Phone'] if pd.notna(contact['Phone']) else "No phone number available"
        mobile = contact['Mobile'] if pd.notna(contact['Mobile']) else "No mobile number available"
        print(f"- {contact['First Name']} {contact['Last Name']}, {contact['Title']}, Email: {contact['Email']}, Phone: {phone}, Mobile: {mobile}\n")
    
    print("Other Contacts:")
    for index, contact in other_contacts.iterrows():
        phone = contact['Phone'] if pd.notna(contact['Phone']) else "No phone number available"
        mobile = contact['Mobile'] if pd.notna(contact['Mobile']) else "No mobile number available"
        print(f"- {contact['First Name']} {contact['Last Name']}, {contact['Title']}, Email: {contact['Email']}, Phone: {phone}, Mobile: {mobile}")

def get_contacts_and_notes_for_deal(deal_id, pipelines_df, contacts_df, notes_df):
    # Find the company ID and additional details associated with the deal ID
    company_row = pipelines_df[pipelines_df['Deal Id'] == deal_id].iloc[0]
    company_id = company_row['Company Id']
    
    # Additional details
    description = company_row['Description'] if 'Description' in company_row else "No Description"
    tag = company_row['Tag'] if 'Tag' in company_row else "No Tag"
    lead_source = company_row['Lead Source'] if 'Lead Source' in company_row else "No Lead Source"
    stage = company_row['Stage'] if 'Stage' in company_row else "No Stage"
    
    # Get the main contact and other contacts
    main_contact, other_contacts = get_main_and_other_contacts(deal_id, pipelines_df, contacts_df)
    
    # Get all notes for the deal
    notes = notes_df[notes_df['Parent Id'] == deal_id]
    
    return main_contact, other_contacts, notes, description, tag, lead_source, stage

def print_results(main_contact, other_contacts, notes, description, tag, lead_source, stage):
    print("Company Details:")
    print(f"Description: {description}, Tag: {tag}, Lead Source: {lead_source}, Stage: {stage}\n")
    
    print_contacts(main_contact, other_contacts)
    
    print("\nNotes:")
    for index, note in notes.iterrows():
        print(f"- Note Content: {note['Note Content']}")

def choose_deal(pipelines_df):
    deal_names = pipelines_df['Deal Name'].tolist()
    deal_ids = pipelines_df['Deal Id'].tolist()
    deal_dict = dict(zip(deal_names, deal_ids))
    
    completer = FuzzyWordCompleter(deal_names)
    selected_deal_name = prompt("Select a deal: ", completer=completer)
    
    return deal_dict[selected_deal_name]

def main():
    pipelines_df, notes_df, contacts_df = load_csv_files()
    deal_id = choose_deal(pipelines_df)
    main_contact, other_contacts, notes, description, tag, lead_source, stage = get_contacts_and_notes_for_deal(deal_id, pipelines_df, contacts_df, notes_df)
    print_results(main_contact, other_contacts, notes, description, tag, lead_source, stage)

if __name__ == "__main__":
    main()
