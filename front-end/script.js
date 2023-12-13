// script.js

const url = 'http://localhost:8000/api/contacts/'

window.get_contacts = async function (skip = 0, limit = 100) {
  const response = await fetch(`${url}?skip=${skip}&limit=${limit}`)
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  const contacts = await response.json()
  return contacts
}

window.create_contact = async function (contact) {
  const response = await fetch(`${url}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(contact),
  })
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
}

window.update_contact = async function (contact) {
  const response = await fetch(`${url}${contact.id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(contact),
  })
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
}

window.delete_contact = async function (id) {
  const response = await fetch(`${url}${id}`, {
    method: 'DELETE',
  })
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
}