import streamlit as st
import pywhatkit
import datetime
import time
from threading import Thread

# Initial list of contacts
contacts = {
    '1': '+919545883002',
    '2': '+917498157771',
    '3': '+918208805916'
}

# Function to send WhatsApp message
def send_whatsapp_message(num, message, delay_time):
    now = datetime.datetime.now()
    current_hour = now.hour
    current_minute = now.minute + 2  # Adding a 2-minute buffer

    # Adjust if minutes exceed 60
    if current_minute >= 60:
        current_minute -= 60
        current_hour += 1

    try:
        pywhatkit.sendwhatmsg(num, message, current_hour, current_minute, wait_time=10)
        st.success(f"Message scheduled to {num} at {current_hour}:{current_minute}")
    except Exception as e:
        st.error(f"Error sending message to {num}: {e}")

    # Wait for the specified delay between messages
    time.sleep(delay_time)

# Function to send message to all contacts
def send_to_all(message, delay=5):
    for num in contacts.values():
        send_whatsapp_message(num, message, delay)

# Streamlit app
def main():
    st.title("WhatsApp Automation App")

    # Sidebar options
    menu = ["Send Message to All", "Send Message to Specific Contact", "Add New Contact", "View Contacts"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Send Message to All":
        st.subheader("Send Message to All Contacts")
        message = st.text_area("Enter your message")
        delay = st.number_input("Enter delay (in seconds) between each message", min_value=1, value=5)

        if st.button("Send to All"):
            if message.strip():
                Thread(target=send_to_all, args=(message, delay)).start()
            else:
                st.error("Message cannot be empty.")

    elif choice == "Send Message to Specific Contact":
        st.subheader("Send Message to a Specific Contact")
        contact_list = {key: value for key, value in contacts.items()}

        contact = st.selectbox("Select a contact", list(contact_list.keys()))
        message = st.text_area("Enter your message")

        if st.button("Send Message"):
            if message.strip():
                Thread(target=send_whatsapp_message, args=(contacts[contact], message, 0)).start()
            else:
                st.error("Message cannot be empty.")

    elif choice == "Add New Contact":
        st.subheader("Add New Contact")
        name = st.text_input("Enter a name for the contact")
        number = st.text_input("Enter the contact number (in international format, e.g., +919XXXXXXXXX)")

        if st.button("Add Contact"):
            if name.strip() and number.strip():
                new_key = str(len(contacts) + 1)
                contacts[new_key] = number
                st.success(f"Contact {name} added successfully!")
            else:
                st.error("Both name and number are required.")

    elif choice == "View Contacts":
        st.subheader("View Contacts")
        if contacts:
            for key, value in contacts.items():
                st.write(f"{key}: {value}")
        else:
            st.info("No contacts available.")

if __name__ == '__main__':
    main()
