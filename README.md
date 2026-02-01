# 🚦 SAFE ROUTE - Road Safety Awareness & Accident Reporting Platform

A next-generation road safety platform for Coimbatore, Tamil Nadu, that enables real-time accident reporting, live incident tracking, and community-driven safety awareness.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![React](https://img.shields.io/badge/React-19.2.4-61dafb.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-000000.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5.8.2-3178c6.svg)

---

## 🌟 Features

### 🗺️ **Live Accident Map**
- Real-time visualization of accidents across Coimbatore
- OpenStreetMap integration with dark theme
- Color-coded severity indicators (High/Medium/Low)
- Interactive markers with detailed incident information
- 12+ accident-prone zones mapped

### 📱 **Accident Reporting**
- Quick incident reporting with image upload
- GPS location capture
- Severity classification
- Real-time status updates
- AI-powered incident analysis

### 🚨 **Emergency Services**
- Nearby hospital locator
- Police station finder
- Fire station directory
- Distance calculation using Haversine formula
- One-click emergency contact

### 📊 **Admin Dashboard**
- Real-time analytics and statistics
- Accident trend analysis
- Prone zone identification
- User activity monitoring
- Data visualization with charts

### 🎓 **Safety Awareness**
- Traffic rules and regulations
- Safety tips and best practices
- AI-powered safety Q&A (Google Gemini)
- Educational content management

### 🔐 **User Management**
- JWT-based authentication
- Role-based access control (Citizen, Admin, Authority)
- User activity tracking
- Leaderboard system

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** React 19.2.4 + TypeScript
- **Styling:** Tailwind CSS 3.4.1
- **Maps:** Leaflet + OpenStreetMap
- **Charts:** Recharts
- **Icons:** Lucide React
- **AI:** Google Gemini API
- **Build Tool:** Vite 6.2.0

### Backend
- **Framework:** Flask 3.0.0 (Python)
- **Database:** MySQL
- **Authentication:** JWT (PyJWT)
- **Image Processing:** Pillow
- **Geolocation:** Geopy
- **Email Validation:** email-validator

---

## 📁 Project Structure

```
Road Safety/
├── frontend/
│   ├── src/
│   │   ├── App.tsx                    # Main application component
│   │   ├── components/
│   │   │   └── InteractiveLiveMap.tsx # OpenStreetMap component
│   │   ├── services/
│   │   │   └── geminiService.ts       # AI service integration
│   │   ├── types.ts                   # TypeScript type definitions
│   │   ├── constants.ts               # Coimbatore accident data
│   │   ├── index.css                  # Global styles
│   │   └── main.tsx                   # Application entry point
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── vite.config.ts
│
└── backend/
    ├── app.py                         # Flask application entry
    ├── database.py                    # Database connection
    ├── models/                        # Data models (5 files)
    │   ├── user.py
    │   ├── accident.py
    │   ├── alert.py
    │   ├── emergency_service.py
    │   └── awareness.py
    ├── routes/                        # API endpoints (9 files)
    │   ├── auth.py
    │   ├── accidents.py
    │   ├── alerts.py
    │   ├── emergency.py
    │   ├── awareness.py
    │   ├── admin.py
    │   ├── export.py
    │   ├── stats.py
    │   └── backup.py
    ├── services/                      # Business logic (7 files)
    ├── middleware/                    # Auth & validation
    ├── utils/                         # Helper functions
    ├── schema.sql                     # Database schema
    ├── requirements.txt               # Python dependencies
    └── .env                          # Environment variables
```

---

## 🚀 Getting Started

### Prerequisites
- **Node.js** 18+ and npm
- **Python** 3.8+
- **MySQL** 8.0+
- **Google Gemini API Key** (optional, for AI features)

### Frontend Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure environment variables:**
   Create `.env.local` file:
   ```env
   VITE_GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

4. **Access the application:**
   Open [http://localhost:3000](http://localhost:3000)

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up MySQL database:**
   ```bash
   mysql -u root -p
   CREATE DATABASE safe_route;
   exit
   
   mysql -u root -p safe_route < schema.sql
   ```

3. **Configure environment variables:**
   Edit `backend/.env`:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=safe_route
   
   JWT_SECRET_KEY=your_secret_key_here
   JWT_ACCESS_TOKEN_EXPIRES=3600
   
   FLASK_ENV=development
   FLASK_DEBUG=True
   
   UPLOAD_FOLDER=uploads
   MAX_FILE_SIZE=5242880
   ```

4. **Start Flask server:**
   ```bash
   python app.py
   ```

5. **Access the API:**
   Backend runs on [http://localhost:5000](http://localhost:5000)

### Default Admin Credentials
```
Email: admin@saferoute.com
Password: admin123
```

---

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile

### Accidents
- `POST /api/accidents/report` - Report new accident
- `GET /api/accidents/live` - Get live accidents
- `GET /api/accidents/filter` - Filter accidents by criteria
- `PUT /api/accidents/<id>` - Update accident status
- `DELETE /api/accidents/<id>` - Delete accident (Admin)

### Alerts
- `GET /api/alerts/active` - Get active alerts
- `GET /api/alerts/nearby` - Get nearby alerts
- `POST /api/alerts/custom` - Create custom alert (Admin)

### Emergency Services
- `GET /api/emergency/nearby` - Find nearby services
- `GET /api/emergency/hospitals` - List all hospitals
- `GET /api/emergency/police` - List police stations

### Admin Analytics
- `GET /api/admin/dashboard` - Dashboard statistics
- `GET /api/admin/timeline` - Accident timeline
- `GET /api/admin/prone-zones` - Accident-prone zones
- `GET /api/admin/trends` - Trend analysis

### Export & Backup
- `GET /api/export/csv` - Export accidents as CSV
- `GET /api/export/heatmap` - Get heatmap data
- `POST /api/backup/create` - Create database backup (Admin)

---

## 🗺️ Coimbatore Coverage

The platform currently tracks accident-prone zones across Coimbatore:

**High-Risk Zones:**
- Gandhipuram Central
- RS Puram Junction
- Avinashi Road
- Sathy Road

**Medium-Risk Zones:**
- Trichy Road
- Peelamedu
- Mettupalayam Road
- Singanallur

**Low-Risk Zones:**
- Saibaba Colony
- Hopes College Area
- Pollachi Road
- Kalapatti

---

## 🎨 Features Showcase

### Real-Time Map
- Dark-themed OpenStreetMap
- Pulsing animations for critical incidents
- Click markers for detailed information
- Time-ago display (e.g., "30m ago")
- Total incident counter

### AI-Powered Safety Advisor
- Ask safety-related questions
- Get instant AI responses
- Powered by Google Gemini

### Analytics Dashboard
- Accident statistics
- Severity distribution charts
- Time-based trends
- Geographic heatmaps

---

## 🔒 Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- Role-based access control
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- Rate limiting
- Secure file uploads

---

## 📊 Database Schema

**Tables:**
- `users` - User accounts and profiles
- `accidents` - Accident reports
- `alerts` - Safety alerts
- `emergency_services` - Hospitals, police, fire stations
- `awareness_content` - Safety tips and rules
- `user_activity` - Activity tracking
- `backups` - Database backup records

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

**SAFE ROUTE Team**
- Road Safety Initiative for Coimbatore

---

## 🙏 Acknowledgments

- OpenStreetMap contributors
- CARTO for dark map tiles
- Google Gemini AI
- Coimbatore Traffic Police
- Road Safety Community

---

## 📞 Support

For support, email support@saferoute.com or open an issue in the repository.

---

## 🗓️ Roadmap

- [ ] Mobile app (React Native)
- [ ] Real-time notifications (WebSocket)
- [ ] Multi-language support
- [ ] Integration with government databases
- [ ] Predictive accident analysis
- [ ] Community reporting verification
- [ ] Gamification and rewards

---

**Made with ❤️ for safer roads in Coimbatore**
