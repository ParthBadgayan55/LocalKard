# 🛍️ LocalKard Phase 1 - Interactive Demo

**WhatsApp-Native Digital Catalog with Automated Reorder Reminders & Cross-Shop Discovery**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## 🎯 What is LocalKard?

LocalKard is a WhatsApp-native platform that helps local shops:
- 📱 Create digital catalogs accessible via WhatsApp
- 🛒 Accept orders through simple chat messages
- 🔔 Send automated reorder reminders to customers
- 🗺️ Enable cross-shop discovery for network effects
- 💰 **Zero payment complexity** - customers pay shops directly

---

## 🎬 Try the Live Demo

**[👉 Click here to access the live demo](https://your-deployed-url.streamlit.app)**

### Demo Credentials

**Fresh Mart Grocery**
- Phone: `9876543210`
- Password: `password123`

**Pet Paradise**
- Phone: `9876543211`
- Password: `password123`

---

## ✨ Features

### For Shop Owners
- ✅ Web dashboard for product management
- ✅ Add/edit/delete products with categories
- ✅ Track orders in real-time
- ✅ Manage stock availability
- ✅ View customer information

### For Customers
- ✅ Browse catalogs via WhatsApp
- ✅ Order with simple text: `1x5, 2x3`
- ✅ Get order confirmations instantly
- ✅ Receive reorder reminders automatically
- ✅ Discover nearby shops

### Advanced Features
- ✅ Geospatial cross-shop discovery
- ✅ Automated reorder reminders (daily cron)
- ✅ Frequency-based scheduling (7, 15, 30 days)
- ✅ One-tap reorder with YES
- ✅ WhatsApp Business API integration

---

## 🛠️ Technology Stack

**Backend:** Node.js + Express + MongoDB + WhatsApp Business API  
**Demo:** Streamlit + Python  
**Database:** MongoDB with geospatial queries  
**Authentication:** JWT + bcrypt  

---

## 🚀 Run Locally

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/localkard-demo.git
cd localkard-demo

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Opens at `http://localhost:8501`

---

## 📦 Project Structure

```
streamlit-demo/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml       # Theme configuration
├── README.md             # This file
└── DEPLOYMENT.md         # Deployment guide
```

---

## 🎨 Demo Sections

### 1. Overview
- System metrics and statistics
- Core features overview
- Technology stack
- Design philosophy

### 2. Shop Dashboard
- Product management
- Order tracking
- Real-time metrics
- Quick actions

### 3. Products
- Product CRUD operations
- Category organization
- Stock management
- Reorder settings

### 4. Orders
- Order list with filters
- Status updates
- Customer information
- Delivery tracking

### 5. WhatsApp Demo
- Interactive chat simulation
- Full customer flow
- Order placement
- Reorder reminders

### 6. Documentation
- API reference
- Quick start guide
- Technical specs

---

## 💡 Key Highlights

### Zero Payment Strategy
- No payment gateway integration
- No KYC requirements
- Customers pay shops directly (cash/UPI)
- Faster launch, zero regulatory burden

### WhatsApp-First Approach
- No app download required
- Familiar interface for all users
- High engagement rates
- Works on any phone

### Network Effect
- Cross-shop discovery
- Location-based recommendations
- Each shop brings value to others

---

## 📊 Full Product (Node.js)

This is a **demo interface**. The full LocalKard product includes:

**Backend API:** 10+ endpoints, JWT auth, MongoDB  
**WhatsApp Integration:** Business API webhook, message parsing  
**Reorder System:** Daily cron jobs, frequency-based scheduling  
**Discovery Engine:** Geospatial queries, 5km radius search  

**Repository:** [Link to full product repo]

---

## 🚀 Deploy Your Own

See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions to deploy on:
- Streamlit Cloud (free, recommended)
- Heroku
- AWS / DigitalOcean
- Docker

---

## 📈 Stats

- **26 files** in full product
- **13 JavaScript** source files
- **5 database models**
- **10+ API endpoints**
- **Zero payment** complexity

---

## 🤝 Contributing

This is a demo/prototype. For production implementation:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 📞 Contact

- **GitHub:** [@your-username](https://github.com/your-username)
- **Email:** your-email@example.com
- **Demo:** [Live Demo Link](https://your-demo-url.streamlit.app)

---

## 🙏 Acknowledgments

- Built for local businesses
- Powered by WhatsApp Business API
- Demo interface: Streamlit
- Full product: Node.js + MongoDB

---

**⭐ Star this repo if you find it useful!**

*Empowering local businesses with technology* 🛍️
