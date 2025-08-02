# Tathya - Case Management System

## Overview

Tathya is a comprehensive case management system built with Streamlit for managing legal/compliance cases within an organization. It provides role-based access control for Initiators, Reviewers, Approvers, Legal Reviewers, Action Closure Authorities (Actioners), and Administrators. The system manages the complete lifecycle of cases from creation to closure, including audit trails and document management. Tathya aims to streamline case workflows, enhance compliance, and provide robust analytics for organizational legal and risk management.

## User Preferences

Preferred communication style: Simple, everyday language.
Case display format: Simple plain text lists without any HTML formatting, styling, or tables.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application
- **UI/UX Decisions**:
    - Modern glassmorphism design with professional gradients, animations, and hover effects.
    - Consistent branding with logos and corporate color themes.
    - Professional iconography and typography (Aptos font family).
    - Customizable user dashboards with various widget types and layout options.
    - Expandable navigation panels and standardized, professional case display formats (card-based, grid layouts).
    - **Investigation Intelligence Branding**: Unified "🔎 Tathya Investigation Intelligence" header across all Investigation workflow pages with AI-styled gradient design.
- **UI Pattern**: Multi-page application with role-based navigation.
- **Layout**: Wide layout with responsive columns and tabs.
- **State Management**: Streamlit session state for authentication and user context.
- **Navigation**: Sidebar-based navigation with role-specific menu options, organized into logical sections (Case Management, Workflow Stages, Analytics, Utility). Main Investigation button rebranded to "🔎 Tathya Investigation Intelligence".

### Backend Architecture
- **Application Layer**: Python-based business logic with modular page structure.
- **Authentication**: Professional login page with secure authentication system, user ID/password login, session management, and flexible role-based access control (including "All Roles Access" for specific users). Features login attempt tracking and account lockout protection.
- **Authorization**: Role-based access control with decorators.
- **Database Layer**: SQLite database with context manager pattern, including login audit logging.
- **File Management**: Local file system for document uploads with organized directory structure.

### Technical Implementations & Feature Specifications
- **Case Entry**: Comprehensive forms for case registration, including demographic details, identity document image management (PAN, Aadhaar, Customer Photo), and other supporting documents (Business, Property, Additional). Features include auto-generated Case IDs, masked Aadhaar display, and a dedicated Identity Verification tab.
- **User Management**: Comprehensive user master system with detailed profiles, team assignments, and referral mappings. Admin users can view, add, edit, and soft-delete users, and manage "All Roles Access".
- **Case Management Workflow**:
    - **Workflow Sequence**: Initiator → Primary Review → Investigation → Final Review → Approver 1 → Approver 2 → Legal & Actioner (parallel processing).
    - **Investigation Panel**: Features case auto-fetch, detailed investigation forms (document/field verification), case assignment options (Closure, Regional, Agency), and PDF report generation. Includes risk score analysis.
    - **Reviewer/Approver Panels**: Standardized case details display, clear status transitions, and integration with the overall workflow.
    - **Final Review Panel**: Manages post-investigation review, including AI-powered summary generation, and separate actions for Legal and Actioner.
    - **Legal Panel**: Supports various legal action types (SCN, Reasoned Order, Legal Opinion, Recovery Notice) with sequential workflow.
    - **Actioner Panel**: Comprehensive action recommendations, risk level evaluation, and sequential action types (Recovery Closure, Settlement, Write-off, Transfer to Legal).
    - **Document Management**: Supports multiple document formats (PDF, JPG, PNG, DOCX, XLS, XLSX) with secure file handling and audit logging.

- **Smart Verification & Risk Detection Suite**: AI-driven platform with modules for Face Match Intelligence (dual-service: DeepFace AI with 6 models locally + Face++ Cloud API), Signature Verification, Document Consistency, OCR & Field Extraction, Bank Statement Analyzer, Anomaly Detection, ID Validation, Inter-Document Cross-Check, Suspicious Pattern Triggering, and Digital Identity DNA Mapping. All modules use Google Gemini AI for enhanced analysis. Includes a "One-Click Document Verification" workflow with bulk upload and automated categorization.
- **Enhanced Risk Assessment**: Comprehensive Risk Score & Speedometer with 25+ parameters across 5 categories (Personal, Financial, Property, Business, Advanced Risk Factors), featuring tabbed interface and multi-dimensional AI analysis.
- **MNRL Verification Enhancement**: Mobile Number Revocation List verification now extracts customer details (name, customer ID, registration date, plan details, KYC status) from API responses when available.
- **AI Integration**: Gemini-powered AI Assistant for smart case analysis, document generation, interactive chat, and auto-suggestions/completion in remarks fields. Includes "Enhance Description" feature in case entry forms.
- **Dashboard**: Customizable user dashboards with role-based widgets (Case Statistics, My Cases Summary, Status Distribution, Recent Activity, Priority Cases, Timeline View, Performance Metrics, Workflow Progress). Includes TAT metrics and interactive Plotly charts.
- **Audit System**: Comprehensive audit logging for all case modifications and user actions, including timestamps and user attribution.
- **Error Handling**: Comprehensive system with formatted error boxes, contextual emojis, and integrated logging for various error types (Database, File, Validation, Permission, API).

## External Dependencies

- **Core Libraries**:
    - **Streamlit**: Web application framework.
    - **SQLite3**: Database connectivity.
    - **Pandas**: Data manipulation.
    - **Plotly**: Interactive visualization charts.
    - **Hashlib**: Password security (SHA-256).
    - **ReportLab**: PDF report generation.
- **Third-Party Services/APIs**:
    - **Google Gemini API**: Primary provider for AI-powered case analysis, document generation, smart suggestions, and all verification/analysis tasks across the platform.
    - **DeepFace Library**: Fallback provider for facial recognition using multiple deep learning models (VGG-Face, Facenet, OpenFace, DeepFace, DeepID, ArcFace, Dlib, SFace).
    - **Google Vision API**: Additional fallback option for face verification.
    - **Twilio**: For SMS notifications (e.g., investigation assignment alerts).
- **Deep Learning Dependencies**:
    - **TensorFlow**: Backend for DeepFace neural network models.
    - **OpenCV-Python**: Computer vision library for image processing and face detection.
    - **DeepFace**: Advanced facial recognition library with multiple model support.
- **File System Dependencies**:
    - `uploads/`: Directory for case documents.
    - `exports/`: Directory for exported reports.
    - `case_management.db`: SQLite database file.