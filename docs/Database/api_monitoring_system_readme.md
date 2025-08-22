# API Monitoring System

A comprehensive, real-time monitoring system for the ALwrity backend API with beautiful charts, animations, and performance analytics.

## 🎯 Overview

The API Monitoring System provides real-time insights into API performance, error rates, cache efficiency, and system health through an intuitive dashboard with interactive charts and animations.

## ✨ Features

### 📊 Real-time Monitoring
- **Live API Statistics** - Track requests, errors, and response times
- **Performance Metrics** - Monitor cache hit rates and system health
- **Error Tracking** - Real-time error detection and reporting
- **Endpoint Analytics** - Individual endpoint performance analysis

### 🎨 Interactive Dashboard
- **Beautiful Charts** - Line charts, bar charts, pie charts, area charts, and radar charts
- **Smooth Animations** - Framer Motion powered transitions and effects
- **Responsive Design** - Works perfectly on all screen sizes
- **Real-time Updates** - Auto-refreshes every 10-30 seconds

### 🔧 Smart Monitoring
- **Self-Exclusion** - Monitoring endpoints excluded from being monitored
- **Database Persistence** - All metrics stored in SQLite database
- **Performance Optimized** - Lightweight API calls with caching
- **Error Handling** - Graceful fallbacks and error recovery

## 🚀 Quick Start

### Backend Setup

1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Create Database Tables**
   ```bash
   python scripts/create_monitoring_tables.py --action create
   python scripts/create_cache_table.py
   ```

3. **Generate Test Data** (Optional)
   ```bash
   python scripts/generate_test_monitoring_data.py --action generate
   ```

4. **Start Backend**
   ```bash
   python start_alwrity_backend.py
   ```

### Frontend Setup

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install recharts framer-motion
   ```

2. **Start Development Server**
   ```bash
   npm start
   ```

## 📊 Dashboard Features

### System Status Indicator
- **Location**: Header of Content Planning Dashboard
- **Visual Status**: 🟢 Healthy, 🟡 Warning, 🔴 Critical, ⚪ Unknown
- **Click to Open**: Full monitoring dashboard
- **Auto-refresh**: Every 30 seconds

### Monitoring Dashboard
- **Access**: Click status icon or debug button (📊)
- **Charts**: Multiple chart types with real-time data
- **Metrics**: Performance cards with key statistics
- **Errors**: Recent error log with details

## 📈 Chart Types

### 1. Request Trends (Line Chart)
- **Purpose**: Track request volume and error patterns over time
- **Data**: Requests vs Errors timeline
- **Colors**: Blue (requests), Red (errors)

### 2. Response Times (Area Chart)
- **Purpose**: Monitor average response time trends
- **Data**: Response time in milliseconds
- **Colors**: Green gradient area

### 3. Endpoint Performance (Bar Chart)
- **Purpose**: Compare request volume and errors across endpoints
- **Data**: Top 5 endpoints by request count
- **Colors**: Blue (requests), Red (errors)

### 4. Cache Performance (Pie Chart)
- **Purpose**: Visualize cache hit vs miss distribution
- **Data**: Cache hits vs misses percentage
- **Colors**: Green (hits), Orange (misses)

### 5. System Health (Radar Chart)
- **Purpose**: Multi-dimensional performance overview
- **Metrics**: Performance, Reliability, Cache Hit Rate, Response Time, Error Rate
- **Scale**: 0-100% health score

## 🔧 Configuration

### Excluded Endpoints
The following endpoints are excluded from monitoring to prevent self-monitoring loops:
```python
EXCLUDED_ENDPOINTS = [
    "/api/content-planning/monitoring/lightweight-stats",
    "/api/content-planning/monitoring/api-stats",
    "/api/content-planning/monitoring/cache-stats",
    "/api/content-planning/monitoring/health"
]
```

### Database Tables
- `api_requests` - Individual API request logs
- `api_endpoint_stats` - Aggregated endpoint statistics
- `system_health` - System health snapshots
- `cache_performance` - Cache performance metrics
- `comprehensive_user_data_cache` - User data caching

## 📡 API Endpoints

### Monitoring Endpoints
- `GET /api/content-planning/monitoring/lightweight-stats` - Dashboard header stats
- `GET /api/content-planning/monitoring/api-stats` - Detailed API statistics
- `GET /api/content-planning/monitoring/cache-stats` - Cache performance data
- `GET /api/content-planning/monitoring/health` - Overall system health

### Response Format
```json
{
  "status": "success",
  "data": {
    "status": "healthy",
    "icon": "🟢",
    "recent_requests": 15,
    "recent_errors": 0,
    "error_rate": 0.0,
    "timestamp": "2025-08-21T18:30:00.000000"
  },
  "message": "Lightweight monitoring statistics retrieved successfully"
}
```

## 🎨 UI Components

### SystemStatusIndicator
- **Location**: `frontend/src/components/ContentPlanningDashboard/components/SystemStatusIndicator.tsx`
- **Features**: Status icon, clickable dashboard, tooltips, animations

### MonitoringCharts
- **Location**: `frontend/src/components/ContentPlanningDashboard/components/MonitoringCharts.tsx`
- **Features**: Multiple chart types, responsive design, animations

## 🔍 Troubleshooting

### Dashboard Not Opening
1. Check browser console for errors
2. Verify component is properly imported
3. Use debug button (📊) as alternative
4. Check if Dialog component is rendering

### No Monitoring Data
1. Verify database tables exist
2. Generate test data: `python scripts/generate_test_monitoring_data.py`
3. Check backend logs for errors
4. Verify middleware is active

### High Log Volume
1. Monitoring endpoints are excluded from logging
2. Only errors and critical issues are logged
3. Check excluded endpoints configuration

## 📊 Performance Benefits

### Before Monitoring System
- **Status Checks**: 2-3 seconds per check
- **API Calls**: Multiple expensive calls
- **No Historical Data**: No trend analysis
- **Basic Status**: Simple text indicators

### After Monitoring System
- **Status Checks**: <100ms per check
- **API Calls**: Single lightweight call
- **Historical Data**: Full trend analysis
- **Rich Dashboard**: Interactive charts and animations

## 🛠️ Development

### Adding New Metrics
1. Update database models in `backend/models/api_monitoring.py`
2. Modify middleware in `backend/middleware/monitoring_middleware.py`
3. Update API routes in `backend/api/content_planning/api/routes/monitoring.py`
4. Add chart components in `frontend/src/components/ContentPlanningDashboard/components/MonitoringCharts.tsx`

### Customizing Charts
- **Colors**: Modify `COLORS` array in MonitoringCharts
- **Animations**: Adjust Framer Motion parameters
- **Layout**: Modify Grid container spacing and sizing
- **Data**: Update chart data processing logic

## 📝 Scripts

### Database Management
```bash
# Create monitoring tables
python scripts/create_monitoring_tables.py --action create

# Create cache table
python scripts/create_cache_table.py

# Generate test data
python scripts/generate_test_monitoring_data.py --action generate

# Clear test data
python scripts/generate_test_monitoring_data.py --action clear
```

## 🎯 Success Metrics

- **90% faster** status checks
- **80% fewer** API calls
- **Real-time** monitoring with historical trends
- **Professional** dashboard with animations
- **Zero** self-monitoring loops
- **Clean** backend logs

## 🔮 Future Enhancements

- **Alert System** - Email/Slack notifications for critical issues
- **Custom Dashboards** - User-configurable chart layouts
- **Performance Baselines** - Automated performance thresholds
- **Export Features** - PDF/CSV report generation
- **Mobile App** - Native mobile monitoring dashboard

---

**Built with**: FastAPI, React, Material-UI, Recharts, Framer Motion, SQLAlchemy

**Last Updated**: August 2025
