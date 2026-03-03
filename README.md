# MemeStore

MemeStore is a social media platform for sharing and discovering meme templates. Users can create profiles, upload their own memes, follow other users, and engage with the community through likes, comments, and reposts and can create collections of memes.

Visit the [Memer.in](https://memer.in) to see, use the project in action.

### Project Status
-- Work in Progress

A project for social media for sharing Memes templates
contains frontend and backend

## Features

- User Authentication
- Meme Templates
- User Profiles
- User Uploads
- User Followers
- User Mentions
- Block User
- Report User
- Like Post
- Reply/Comments System (Nested like Twitter)
- Repost Post
- Bookmark Post
- Share Post
- Not interested in Post
- Report Post
- Post Privacy (Public, Private)
- Post likes, bookmarks and download count
- Collections (User can create, edit, delete and share collections of memes like Youtube playlist)
- Search Functionality
- Notifications

## Tech Stack
- Frontend: Html, Tailwind CSS, Vanilla JS
- Backend: Python, Flask, SQLAlchemy, Flask-CORS, Redis, Resend, Cloudinary
- Database: PostgreSQL
- Deployment: Vercel (Frontend, Backend)

## System Architecture
The system architecture of MemeStore is designed to be scalable and efficient, utilizing a microservices approach. The frontend is built using HTML, Tailwind CSS, and Vanilla JS, which communicates with the backend API built with Python and Flask. The backend handles user authentication, meme template management, user profiles, and other core functionalities. PostgreSQL is used as the primary database for storing user data, meme templates, and other related information. Redis is used for caching and session management to improve performance. Third-party services like Resend and Cloudinary are integrated for email delivery and media management, respectively. The application is deployed on Vercel, which provides a seamless deployment experience for both the frontend and backend components.


## Third-Party Services
- Resend is used for sending transactional emails such as account verification, password reset, and notifications to users. It provides a reliable and scalable email delivery service with features like email templates, analytics, and support for various email protocols.
- Cloudinary is used for storing and managing media assets such as meme images uploaded by users. It offers a cloud-based media management solution with features like image optimization, transformation, and delivery through a global content delivery network (CDN).
- Redis is used for caching and session management in the backend. It provides a fast and efficient in-memory data store that can be used to cache frequently accessed data, manage user sessions, and improve the overall performance of the application.


## Installation
 Go to [Docs](./docs/setup.md) folder and follow the instructions in the setup.md file to set up the project locally.
