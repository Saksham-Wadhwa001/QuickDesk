6. Access the Application
Open your browser and go to: http://127.0.0.1:8000
7. Test Login Credentials

Admin: admin / admin123
End User: john_user / password123
Support Agent: jane_agent / password123

8. Admin Interface
Access Django admin at: http://127.0.0.1:8000/admin
Key Features Implemented
✅ Authentication System

User registration and login
Role-based access (End User, Support Agent, Admin)

✅ Ticket Management

Create, view, update tickets
Status workflow: Open → In Progress → Resolved → Closed
Priority levels and categories
File attachments

✅ Search & Filtering

Filter by status, category, priority
Search by subject/description
Sort by date, replies, priority

✅ Agent Features

Ticket assignment
View all or assigned tickets
Add comments and updates

✅ Admin Features

Category management
User role management
Full system access

✅ Engagement Features

Upvote/downvote tickets
Comment system
Email notifications

✅ Responsive Design

Mobile-friendly interface
Clean, modern UI
Intuitive navigation

Development Notes

Database: SQLite (for development)
Backend: Django REST Framework
Frontend: Vanilla JavaScript with modern CSS
Authentication: Session-based
File Uploads: Handled for attachments
Email: Console backend for development
