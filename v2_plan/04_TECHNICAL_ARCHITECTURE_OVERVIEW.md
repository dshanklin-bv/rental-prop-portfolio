# Technical Architecture Overview

## System Design Philosophy

### Core Principles
- **Local-First**: Complete data control with no vendor lock-in
- **Modular Design**: Separation of concerns enabling future technology pivots  
- **API-First**: Headless core business logic independent of UI framework
- **Performance**: Sub-3-second load times for portfolios up to 50 properties
- **Scalability**: Architecture supports growth from 1 to 100+ properties

### Technology Strategy
- **Phase 1**: Streamlit for rapid prototyping and validation
- **Phase 2**: Separate API backend for improved performance and mobile support
- **Phase 3**: Cloud-optional architecture for team collaboration and backup

---

## System Architecture

### High-Level Components
```
┌─────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                          │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│ │   Streamlit UI  │ │  Mobile Web     │ │   API Clients   │   │
│ │   (Phase 1)     │ │  (Phase 2)      │ │   (Phase 3)     │   │
│ └─────────────────┘ └─────────────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                      API LAYER                                  │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│ │ Portfolio API   │ │ Analytics API   │ │ Notification    │   │
│ │                 │ │                 │ │ API             │   │
│ └─────────────────┘ └─────────────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                         │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│ │ Financial       │ │ Alert           │ │ Report          │   │
│ │ Engine          │ │ Engine          │ │ Engine          │   │
│ └─────────────────┘ └─────────────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                     DATA LAYER                                  │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│ │ PostgreSQL      │ │ File Storage    │ │ Cache Layer     │   │
│ │ (Core Data)     │ │ (Documents)     │ │ (Redis/Memory)  │   │
│ └─────────────────┘ └─────────────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Phase 1: MVP Stack (Streamlit-Based)
```
Frontend:
├── Streamlit 1.28+ (Web UI framework)
├── Plotly 5.14+ (Interactive charts)  
├── Folium (Geographic maps)
└── Custom CSS (Styling and branding)

Backend/Logic:
├── Python 3.11+ (Core language)
├── Pydantic 2.0+ (Data validation)
├── Pandas 2.0+ (Data manipulation)
├── NumPy Financial (Financial calculations)
└── SQLAlchemy 2.0+ (Database ORM)

Database:
├── PostgreSQL 15+ (Primary database)
├── Alembic (Database migrations)
└── Redis (Session caching - optional)

Infrastructure:
├── Docker (Containerization)
├── Docker Compose (Local development)
├── Git (Version control)
└── GitHub Actions (CI/CD pipeline)

External Services:
├── SMTP Server (Email notifications)
├── Twilio (SMS alerts - optional)  
└── AWS S3 or MinIO (Document storage)
```

### Phase 2: API-First Stack (Scalability Focus)
```
Additional Components:
├── FastAPI (REST API framework)
├── Celery (Background job processing)
├── APScheduler (Scheduled tasks)
├── Nginx (Reverse proxy and load balancing)
└── React/Vue.js (Alternative frontend - optional)
```

### Phase 3: Cloud-Native Stack (Team Collaboration)
```
Cloud Infrastructure:
├── AWS/GCP/Azure (Cloud hosting)
├── RDS/CloudSQL (Managed PostgreSQL)
├── ElastiCache (Managed Redis)
├── S3/GCS/Blob Storage (Document storage)
└── CloudFormation/Terraform (Infrastructure as Code)

DevOps:
├── Kubernetes (Container orchestration)
├── Helm (K8s package management)
├── Prometheus/Grafana (Monitoring)
└── ELK Stack (Logging and analytics)
```

---

## Data Architecture

### Database Design Strategy

#### Core Entities Schema
```sql
-- Portfolio Management
portfolios (id, name, owner_name, created_at, settings)
properties (id, portfolio_id, address, purchase_price, current_value, ...)
units (id, property_id, unit_number, bedrooms, bathrooms, sqft, ...)
leases (id, unit_id, tenant_name, start_date, end_date, base_rent, ...)

-- Financial Tracking  
loans (id, property_id, loan_type, original_amount, current_balance, rate, ...)
transactions (id, property_id, date, amount, category, description, ...)
cash_flows (id, property_id, month_year, gross_income, noi, cash_flow, ...)

-- Task & Alert Management
alerts (id, property_id, alert_type, priority, message, created_at, resolved_at, ...)
tasks (id, property_id, title, description, due_date, status, category, ...)

-- Acquisition Pipeline
deals (id, portfolio_id, address, asking_price, stage, score, created_at, ...)
deal_analyses (id, deal_id, analysis_date, cap_rate, cash_flow, irr, ...)

-- System & Audit
users (id, email, name, preferences, created_at, ...)
audit_log (id, user_id, action, entity_type, entity_id, timestamp, ...)
```

#### Performance Optimization
```sql
-- Critical Indexes
CREATE INDEX idx_properties_portfolio ON properties(portfolio_id);
CREATE INDEX idx_transactions_property_date ON transactions(property_id, date DESC);
CREATE INDEX idx_alerts_priority_resolved ON alerts(priority, resolved_at) WHERE resolved_at IS NULL;
CREATE INDEX idx_leases_end_date ON leases(end_date) WHERE end_date > CURRENT_DATE;

-- Calculated Views for Performance
CREATE VIEW property_performance AS
SELECT 
    p.id,
    p.address,
    SUM(CASE WHEN t.amount > 0 THEN t.amount ELSE 0 END) as monthly_income,
    SUM(CASE WHEN t.amount < 0 THEN ABS(t.amount) ELSE 0 END) as monthly_expenses,
    SUM(t.amount) as monthly_cash_flow
FROM properties p
LEFT JOIN transactions t ON p.id = t.property_id 
    AND t.date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY p.id, p.address;
```

### Data Flow Architecture
```
User Input → Validation (Pydantic) → Business Logic → Database → Caching → API Response → UI Update
     ↓
File Uploads → Storage (S3/Local) → Metadata DB → Background Processing → Alert Generation
     ↓
External APIs → Rate Limiting → Validation → Cache → Core Data → Calculated Metrics
```

---

## API Design

### RESTful API Endpoints

#### Portfolio Management
```
GET    /api/v1/portfolios                    # List portfolios
POST   /api/v1/portfolios                    # Create portfolio
GET    /api/v1/portfolios/{id}               # Get portfolio details
PUT    /api/v1/portfolios/{id}               # Update portfolio
DELETE /api/v1/portfolios/{id}               # Delete portfolio

GET    /api/v1/portfolios/{id}/properties    # List properties
POST   /api/v1/portfolios/{id}/properties    # Add property
GET    /api/v1/properties/{id}               # Get property details  
PUT    /api/v1/properties/{id}               # Update property
DELETE /api/v1/properties/{id}               # Delete property
```

#### Financial Analytics
```
GET /api/v1/properties/{id}/performance      # Property performance metrics
GET /api/v1/properties/{id}/cash-flow        # Monthly cash flow data
GET /api/v1/properties/{id}/scenarios        # Scenario analysis results
POST /api/v1/properties/{id}/scenarios       # Run scenario analysis

GET /api/v1/portfolios/{id}/dashboard        # Dashboard KPIs
GET /api/v1/portfolios/{id}/comparison       # Property comparison data
```

#### Alert & Task Management
```
GET /api/v1/portfolios/{id}/alerts           # List alerts
POST /api/v1/alerts/{id}/resolve             # Mark alert resolved
GET /api/v1/portfolios/{id}/tasks            # List tasks
POST /api/v1/portfolios/{id}/tasks           # Create task
PUT /api/v1/tasks/{id}                       # Update task
```

### Data Models (Pydantic Schemas)
```python
class PropertyResponse(BaseModel):
    id: str
    address: str
    property_type: PropertyType
    purchase_price: Decimal
    current_value: Optional[Decimal]
    monthly_cash_flow: Decimal
    cap_rate: float
    created_at: datetime
    
class PerformanceMetrics(BaseModel):
    monthly_noi: Decimal
    monthly_cash_flow: Decimal
    cap_rate: float
    cash_on_cash_return: float
    dscr: Optional[float]
    occupancy_rate: float
    
class ScenarioAnalysis(BaseModel):
    scenario_name: str
    assumptions: Dict[str, Any]
    projected_irr: float
    projected_cash_flows: List[Decimal]
    sensitivity_analysis: Dict[str, float]
```

---

## Security Architecture

### Authentication & Authorization
```
Authentication Strategy (Phase 1):
├── Local authentication (email/password)
├── Session-based auth with Streamlit
├── Password hashing (bcrypt)
└── Basic rate limiting

Authentication Strategy (Phase 2+):
├── JWT-based authentication  
├── OAuth 2.0 integration (Google, Microsoft)
├── Multi-factor authentication (TOTP)
├── API key management for integrations
└── Role-based access control (RBAC)
```

### Data Security
```
Encryption:
├── Database: Encryption at rest (PostgreSQL TDE)
├── Transmission: HTTPS/TLS 1.3 for all communications
├── File Storage: Server-side encryption for documents
└── Local Storage: Encrypted connection strings and secrets

Data Privacy:
├── PII anonymization in logs and analytics
├── GDPR-compliant data export/deletion
├── Audit logging for all data access
└── Regular security assessments and penetration testing
```

---

## Performance & Scalability

### Performance Targets
```
Response Time Targets:
├── Dashboard Load: <3 seconds (up to 20 properties)
├── Property Detail: <2 seconds
├── Scenario Analysis: <5 seconds
├── Report Generation: <10 seconds
└── Chart Interactions: <500ms

Scalability Targets:
├── Properties per Portfolio: 100+
├── Transactions per Property: 1,000+ per year  
├── Concurrent Users: 50+ (Phase 2)
├── Data Retention: 10+ years of historical data
└── API Throughput: 1,000+ requests/minute (Phase 2)
```

### Caching Strategy
```
Cache Levels:
├── Application Cache (Redis): Calculated metrics, user sessions
├── Database Query Cache: Complex analytical queries
├── CDN Cache: Static assets (charts, reports, documents)
└── Browser Cache: UI components and API responses

Cache Invalidation:
├── Time-based: Financial metrics (1 hour), market data (daily)
├── Event-based: Property updates, transaction changes
├── Manual: Administrative changes, data corrections
└── Smart invalidation: Dependency-based cache clearing
```

### Database Optimization
```
Performance Strategies:
├── Read Replicas: Separate analytics queries from transactional
├── Partitioning: Monthly partitions for transactions table
├── Archival: Move old transactions to separate archive tables
├── Materialized Views: Pre-calculated portfolio metrics
└── Connection Pooling: Efficient database connection management

Monitoring:
├── Query Performance: Slow query logging and analysis
├── Index Usage: Regular index optimization
├── Resource Usage: CPU, memory, and I/O monitoring
└── Growth Planning: Capacity planning based on usage trends
```

---

## Deployment & DevOps

### Development Workflow
```
Local Development:
├── Docker Compose setup with all services
├── Hot reloading for rapid iteration
├── Pre-commit hooks for code quality
├── Local testing with sample data
└── Database seeding and migration scripts

CI/CD Pipeline:
├── GitHub Actions for automated testing
├── Code quality checks (flake8, mypy, black)
├── Security scanning (bandit, safety)
├── Database migration testing
├── Automated deployment to staging
└── Manual deployment approval for production
```

### Infrastructure as Code
```
Docker Configuration:
├── Multi-stage builds for optimal image size
├── Health checks for all services
├── Environment-based configuration
├── Volume mounting for persistent data
└── Network isolation for security

Deployment Options:
├── Phase 1: Single-server deployment (Docker Compose)
├── Phase 2: Container orchestration (Kubernetes)
├── Phase 3: Cloud-native (managed services)
└── Backup Strategy: Automated backups with point-in-time recovery
```

---

## Integration Architecture

### External Service Integration
```
Financial Data:
├── Interest Rate APIs (Fed rates, mortgage rates)
├── Market Data (Zillow, RentSpree for comparables)
├── Banking APIs (Plaid for transaction import)
└── Accounting Software (QuickBooks, Xero sync)

Communication Services:
├── Email (SMTP, SendGrid, or AWS SES)
├── SMS (Twilio for critical alerts)
├── Push Notifications (Firebase for mobile)
└── Calendar Integration (Google Calendar, Outlook)

Property Management:
├── AppFolio, Buildium APIs for data sync
├── Tenant Screening Services (RentPrep, TransUnion)
├── Maintenance Platforms (ServiceChannel, UpKeep)
└── Insurance Platforms (policy renewal automation)
```

### API Integration Patterns
```
Integration Strategy:
├── Event-Driven: Webhooks for real-time updates
├── Scheduled Sync: Daily/weekly batch imports
├── On-Demand: User-initiated data refresh
└── Caching Layer: Minimize external API calls

Error Handling:
├── Retry Logic: Exponential backoff for transient failures
├── Circuit Breakers: Prevent cascade failures
├── Graceful Degradation: Continue operation with reduced functionality
└── Alert System: Notify of integration failures
```

---

## Monitoring & Observability

### Application Monitoring
```
Metrics Collection:
├── Performance Metrics: Response times, throughput, error rates
├── Business Metrics: Portfolio growth, user engagement, feature usage
├── Infrastructure Metrics: CPU, memory, disk, network utilization
└── Security Metrics: Failed login attempts, API abuse patterns

Alerting Rules:
├── System Health: Response time >5s, error rate >5%
├── Business Critical: Failed calculations, data corruption
├── Security: Multiple failed logins, unusual access patterns
└── Resource: High CPU/memory usage, disk space warnings
```

### Logging Strategy
```
Log Levels and Usage:
├── ERROR: Application errors, integration failures
├── WARN: Performance degradation, validation warnings  
├── INFO: User actions, business events, system status
├── DEBUG: Detailed execution flow (development only)

Log Structure:
├── Structured Logging: JSON format for parsing
├── Correlation IDs: Track requests across services
├── User Context: User ID, session ID, IP address
├── Performance Context: Execution time, resource usage
└── Security Context: Authentication status, permissions
```

This architecture provides a solid foundation for building a scalable, maintainable real estate portfolio management system that can evolve from a simple local tool to a comprehensive cloud-based platform.