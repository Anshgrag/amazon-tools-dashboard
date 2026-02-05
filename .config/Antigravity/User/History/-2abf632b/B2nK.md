# Implementation Plan - Luxe Jewellery E-commerce

## Goal Description
Build a premium, full-stack jewellery e-commerce platform with a NestJS backend and Next.js frontend. The design will focus on minimalism, elegance (ivory/gold), and detailed product presentation. The system will support multi-currency, international shipping, and a comprehensive admin dashboard.

## User Review Required
> [!IMPORTANT]
> - **Payment Gateway**: Using Razorpay for India as primary. Stripe-ready structure will be implemented but Razorpay will be the active provider for the demo/MVP.
> - **Database**: PostgreSQL is required. Ensure a local or cloud instance is available.
> - **Images**: Cloudinary will be used. API keys will be needed (placeholders will be used in code).

## Proposed Changes

### Project Structure
- `server/`: NestJS Backend
- `client/`: Next.js Frontend

### Backend (NestJS)
#### [NEW] Modules
- **Prisma Module**: Database connection and schema.
- **Auth Module**: JWT strategy for Admin.
- **Products Module**: CRUD for products, categories, inventory.
- **Orders Module**: Order processing, status updates.
- **Payment Module**: Integration with Razorpay.
- **Upload Module**: Cloudinary integration.

#### [NEW] Database Schema (Prisma)
- `User` (Admin mostly)
- `Product` (Name, Description, Price, Images, Stock, Category)
- `Category`
- `Order` (User details, Status, Total, PaymentInfo)
- `OrderItem`

### Frontend (Next.js)
#### [NEW] Tech Stack
- Next.js 14+ (App Router)
- Tailwind CSS
- Framer Motion
- Zustand (State Management)
- Lucide React (Icons)

#### [NEW] Pages
- `/`: Hero, Featured Collections.
- `/shop`: All products/collections.
- `/product/[slug]`: Product details.
- `/cart`: Shopping cart.
- `/checkout`: Payment flow.
- `/admin`: Dashboard (protected).

## Verification Plan

### Automated Tests
- Backend: Unit tests for Services (Jest).
- Frontend: Build verification.

### Manual Verification
- Verify Admin Login.
- Verify Product Creation & Image Upload.
- Verify Cart Add/Remove.
- Verify Checkout Flow (Test Mode).
- Verify Responsive Design.
