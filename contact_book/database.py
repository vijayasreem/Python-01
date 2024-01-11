from typing import List
import datetime
from contact_book.model import Contact
from contact_book import db, ContactQuery


def create(contact: Contact) -> None:
    contact.position = len(db)+1
    new_contact = {
        'name': contact.name,
        'contact_number': contact.contact_number,
        'address': contact.address,  # Added new address field
        'position': contact.position,
        'date_created': contact.date_created,
        'date_updated': contact.date_updated
    }
    db.insert(new_contact)


def read() -> List[Contact]:
    results = db.all()
    contacts = []
    for result in results:
        new_contact = Contact(result['name'], result['contact_number'], result['address'],  # Updated to include address
                              result['position'], result['date_created'], result['date_updated'])
        contacts.append(new_contact)
    return contacts


def update(position: int, name: str, contact_number: str, address: str) -> None:  # Added address parameter
    if name is not None and contact_number is not None and address is not None:
        db.update({'name': name, 'contact_number': contact_number, 'address': address},
                  ContactQuery.position == position)
    elif name is not None and contact_number is not None:
        db.update({'name': name, 'contact_number': contact_number},
                  ContactQuery.position == position)
    elif name is not None and address is not None:
        db.update({'name': name, 'address': address},
                  ContactQuery.position == position)
    elif contact_number is not None and address is not None:
        db.update({'contact_number': contact_number, 'address': address},
                  ContactQuery.position == position)
    elif name is not None:
        db.update({'name': name}, ContactQuery.position == position)
    elif contact_number is not None:
        db.update({'contact_number': contact_number},
                  ContactQuery.position == position)
    elif address is not None:
        db.update({'address': address}, ContactQuery.position == position)


def delete(position) -> None:
    count = len(db)
    db.remove(ContactQuery.position == position)
    for pos in range(position+1, count):
        change_position(pos, pos-1)


def change_position(old_position: int, new_position: int) -> None:
    db.update({'position': new_position},
              ContactQuery.position == old_position)