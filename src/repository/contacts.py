from datetime import timedelta, date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact
from src.schemas.contact import ContactSchema, ContactUpdateSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.e_mail = body.e_mail
        contact.birthday = body.birthday
        contact.add_data = body.add_data
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def get_firstname_contacts(firstname: str, limit: int, offset: int, db: AsyncSession):
    stmt = select(Contact).filter(Contact.firstname == firstname).offset(offset).limit(limit)
    contacts_firstname = await db.execute(stmt)
    return contacts_firstname.scalars().all()


async def get_birthdays_per_week(limit: int, offset: int, db: AsyncSession):
    date_today = date.today()
    date_delta = timedelta(days=6)
    date_end = date_today + date_delta

    stmt = select(Contact).filter(Contact.birthday >= date_today).filter(Contact.birthday <= date_end).offset(
        offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()
