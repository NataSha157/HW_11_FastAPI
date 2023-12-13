from datetime import timedelta, date

from sqlalchemy import select, and_
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


async def get_lastname_contacts(lastname: str, limit: int, offset: int, db: AsyncSession):
    stmt = select(Contact).filter(Contact.lastname == lastname).offset(offset).limit(limit)
    contacts_lastname = await db.execute(stmt)
    return contacts_lastname.scalars().all()


async def get_email_contacts(e_mail: str, limit: int, offset: int, db: AsyncSession):
    stmt = select(Contact).filter(Contact.e_mail == e_mail).offset(offset).limit(limit)
    contacts_email = await db.execute(stmt)
    return contacts_email.scalars().all()


async def get_birthdays_per_week(limit: int, offset: int, db: AsyncSession):
    date_today = date.today()
    date_delta = timedelta(days=6)
    date_end = date_today + date_delta
    now_month = date_today.month
    now_day = date_today.day
    end_month = date_end.month
    end_day = date_end.day

    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    res = contacts.scalars().all()

    get_res = []
    for i in res:
        if i.birthday.month >= now_month and i.birthday.month <= end_month and i.birthday.day >= now_day and i.birthday.day <= end_day:
            get_res.append(i)

    return get_res
