import json
import streamlit as st

# Load library from file
def load_library():
    try:
        with open("library.txt", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save library to file
def save_library():
    with open("library.txt", "w") as file:
        json.dump(library, file)

# Initialize library
library = load_library()

# Streamlit UI
st.title("📚 Personal Library Manager")

menu = ["Add Book", "Remove Book", "Search Book", "View Library", "Statistics"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Have you read this book?")
    
    if st.button("Add Book"):
        book = {"title": title, "author": author, "year": year, "genre": genre, "read": read_status}
        library.append(book)
        save_library()
        st.success("📚 Book added successfully!")

elif choice == "Remove Book":
    st.subheader("🗑️ Remove a Book")
    titles = [book["title"] for book in library]
    book_to_remove = st.selectbox("Select Book to Remove", titles) if titles else None
    
    if book_to_remove and st.button("Remove Book"):
        library = [book for book in library if book["title"] != book_to_remove]
        save_library()
        st.success("✅ Book removed successfully!")

elif choice == "Search Book":
    st.subheader("🔎 Search for a Book")
    search_type = st.radio("Search by", ("Title", "Author"))
    search_query = st.text_input("Enter search term")
    
    if st.button("Search"):
        results = [book for book in library if book[search_type.lower()].lower() == search_query.lower()]
        if results:
            st.write("### 📚 Search Results")
            for book in results:
                st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
        else:
            st.warning("❌ No matching books found!")

elif choice == "View Library":
    st.subheader("📖 Your Library")
    if library:
        for book in library:
            st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
    else:
        st.info("📭 Your library is empty! Add some books first.")

elif choice == "Statistics":
    st.subheader("📊 Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    
    st.write(f"📚 **Total books:** {total_books}")
    st.write(f"✅ **Books read:** {read_books}")
    st.write(f"📖 **Percentage read:** {percentage_read:.2f}%")
